#!/usr/bin/env python3
"""
Process raw JSON results into analysis-ready DataFrames
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
from typing import Dict, List, Any

# Tier mapping
TIER_MAP = {
    "ave": "cinema",
    "finevideo": "web_ugc", 
    "produced_digital/commercials": "produced_digital",
    "produced_digital/musicvideos": "produced_digital",
}

def load_result(filepath: Path) -> Dict[str, Any]:
    """Load a single result JSON file"""
    with open(filepath) as f:
        return json.load(f)

def safe_mean(lst):
    """Safely compute mean of a list"""
    if not lst:
        return 0.0
    try:
        return float(np.nanmean(lst))
    except:
        return 0.0

def extract_metrics(data: Dict) -> Dict[str, Any]:
    """Extract key metrics from a result file"""
    
    scene = data.get('scene_signals', {}) or {}
    char = data.get('character_signals', {}) or {}
    visual = data.get('visual_signals', {}) or {}
    atmos = data.get('atmosphere_signals', {}) or {}
    action = data.get('action_signals', {}) or {}
    temporal = data.get('temporal_signals', {}) or {}
    meta = data.get('metadata', {}) or {}
    
    # Skip if missing critical metadata
    tier = meta.get('tier')
    dataset = meta.get('dataset')
    if not tier or not dataset:
        return None
    
    return {
        # Identifiers
        'video_id': data.get('video_id'),
        'fps': data.get('fps'),
        'frame_count': data.get('frame_count', 0),
        'duration': data.get('duration', 0),
        'dataset': dataset,
        'tier': tier,
        'study_type': meta.get('study_type', 'core'),
        'source_fps': meta.get('source_fps', 0),
        
        # Scene metrics
        'scene_count': scene.get('scene_count', 0) or 0,
        'transition_count': scene.get('transition_count', 0) or 0,
        'scene_duration_mean': scene.get('scene_duration_mean', 0) or 0,
        'scene_duration_std': scene.get('scene_duration_std', 0) or 0,
        
        # Character metrics
        'person_count_mean': char.get('person_count_mean', 0) or 0,
        'person_count_max': char.get('person_count_max', 0) or 0,
        'character_consistency': char.get('character_consistency', 0) or 0,
        'entry_exit_total': char.get('entry_exit_total', 0) or 0,
        
        # Visual metrics
        'unique_object_count': visual.get('unique_object_count', 0) or 0,
        'persistent_object_count': visual.get('persistent_object_count', 0) or 0,
        'objects_per_frame_mean': safe_mean(visual.get('objects_per_frame', [])),
        
        # Atmosphere metrics
        'brightness_mean': atmos.get('brightness_mean', 0) or 0,
        'brightness_std': atmos.get('brightness_std', 0) or 0,
        'contrast_mean': atmos.get('contrast_mean', 0) or 0,
        'dominant_colors': len(atmos.get('dominant_colors', []) or []),
        
        # Action metrics
        'intensity_mean': action.get('intensity_mean', 0) or 0,
        'intensity_max': action.get('intensity_max', 0) or 0,
        'peak_count': action.get('peak_count', 0) or 0,
        
        # Temporal metrics
        'change_score_mean': temporal.get('change_score_mean', 0) or 0,
        'temporal_density': temporal.get('temporal_density', 0) or 0,
    }

def process_all_results(base_path: str = "data/clean_results") -> pd.DataFrame:
    """Process all result files into a DataFrame"""
    
    base = Path(base_path)
    all_files = list(base.rglob("*.json"))
    
    print(f"Processing {len(all_files)} result files...")
    
    records = []
    skipped = 0
    
    for filepath in tqdm(all_files):
        try:
            data = load_result(filepath)
            metrics = extract_metrics(data)
            if metrics:
                records.append(metrics)
            else:
                skipped += 1
        except Exception as e:
            skipped += 1
    
    print(f"  Processed: {len(records)}, Skipped: {skipped}")
    
    df = pd.DataFrame(records)
    return df

def compute_fps_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregate metrics by FPS level and tier"""
    
    agg_funcs = {
        'frame_count': 'mean',
        'scene_count': 'mean',
        'transition_count': 'mean',
        'person_count_mean': 'mean',
        'unique_object_count': 'mean',
        'objects_per_frame_mean': 'mean',
        'intensity_mean': 'mean',
        'character_consistency': 'mean',
        'video_id': 'count',  # count of videos
    }
    
    grouped = df.groupby(['tier', 'fps']).agg(agg_funcs).reset_index()
    grouped = grouped.rename(columns={'video_id': 'video_count'})
    
    return grouped

def compute_signal_stability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute signal stability across FPS levels
    """
    
    metrics = [
        'scene_count', 'transition_count', 'unique_object_count',
        'person_count_mean', 'intensity_mean'
    ]
    
    results = []
    
    for tier in df['tier'].unique():
        tier_df = df[df['tier'] == tier]
        
        for video_id in tier_df['video_id'].unique():
            video_df = tier_df[tier_df['video_id'] == video_id].sort_values('fps')
            
            if len(video_df) < 2:
                continue
            
            for metric in metrics:
                values = video_df[metric].values
                fps_levels = video_df['fps'].values
                
                mean_val = np.mean(values)
                if mean_val > 0:
                    cv = np.std(values) / mean_val
                else:
                    cv = 0
                
                # Find stabilization point (where change < 5%)
                stable_fps = fps_levels[-1]
                for i in range(1, len(values)):
                    if values[i-1] > 0:
                        change = abs(values[i] - values[i-1]) / values[i-1]
                        if change < 0.05:
                            stable_fps = fps_levels[i]
                            break
                
                results.append({
                    'tier': tier,
                    'video_id': video_id,
                    'metric': metric,
                    'cv': cv,
                    'stable_fps': stable_fps,
                    'min_value': float(values.min()),
                    'max_value': float(values.max()),
                })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    print("=" * 60)
    print("PROCESSING RESULTS")
    print("=" * 60)
    
    df = process_all_results()
    
    print(f"\n=== Dataset Summary ===")
    print(f"Total records: {len(df)}")
    print(f"\nBy tier:")
    print(df.groupby('tier').size())
    print(f"\nBy FPS level:")
    print(df.groupby('fps').size().sort_index())
    print(f"\nBy dataset:")
    print(df.groupby('dataset').size())
    
    # Save processed data
    df.to_parquet("analysis/signals_df.parquet", index=False)
    print(f"\n✅ Saved: analysis/signals_df.parquet")
    
    # Compute aggregates
    agg_df = compute_fps_aggregates(df)
    agg_df.to_parquet("analysis/metrics_by_fps.parquet", index=False)
    print(f"✅ Saved: analysis/metrics_by_fps.parquet")
    
    # Compute stability
    stability_df = compute_signal_stability(df)
    stability_df.to_parquet("analysis/signal_stability.parquet", index=False)
    print(f"✅ Saved: analysis/signal_stability.parquet")
    
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
