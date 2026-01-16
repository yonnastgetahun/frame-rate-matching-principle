#!/usr/bin/env python3
"""
Fix the gap analysis:
1. Normalize validation comparison by duration
2. Fix AD tier mapping logic
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

plt.style.use('seaborn-v0_8-whitegrid')

def load_data():
    df = pd.read_parquet("analysis/signals_df.parquet")
    return df

# =============================================================================
# FIX 1: AD TIER MAPPING - Use percentile-based thresholds
# =============================================================================

def map_ad_tiers_fixed(df: pd.DataFrame, output_dir: Path):
    """
    Map signal thresholds to AD tiers using INCREASING signals only
    and reasonable threshold logic
    """
    
    # Only use signals that INCREASE with FPS (meaningful for quality)
    increasing_signals = {
        'Compliance AD': {
            'description': 'Basic: scene boundaries, character presence, key objects',
            'signals': ['scene_count', 'unique_object_count'],
            'threshold': 0.80,  # 80% of plateau value
        },
        'Enhanced AD': {
            'description': 'Rich: above + transitions, temporal flow',
            'signals': ['scene_count', 'unique_object_count', 'transition_count', 'temporal_density'],
            'threshold': 0.90,  # 90% of plateau value
        },
        'Audio Cinema': {
            'description': 'Full: all signals at maximum fidelity',
            'signals': ['scene_count', 'unique_object_count', 'transition_count', 'temporal_density'],
            'threshold': 0.95,  # 95% of plateau value
        }
    }
    
    results = []
    fps_levels = sorted(df['fps'].unique())
    
    for tier_name, config in increasing_signals.items():
        for content_tier in ['cinema', 'produced_digital', 'web_ugc']:
            tier_df = df[df['tier'] == content_tier]
            
            signal_fps = []
            for signal in config['signals']:
                if signal not in tier_df.columns:
                    continue
                
                # Get mean value at each FPS
                fps_means = tier_df.groupby('fps')[signal].mean()
                
                # Find plateau value (use value at 60fps as reference, not max)
                # This avoids noise at very high FPS
                plateau_fps = 60.0 if 60.0 in fps_means.index else fps_means.index[-1]
                plateau_val = fps_means[plateau_fps]
                min_val = fps_means.min()
                
                # Target value based on threshold
                target = min_val + config['threshold'] * (plateau_val - min_val)
                
                # Find first FPS that meets target
                for fps in fps_levels:
                    if fps_means.get(fps, 0) >= target:
                        signal_fps.append(fps)
                        break
                else:
                    signal_fps.append(60.0)  # Default to 60 if never reached
            
            # Required FPS is the max across all signals
            required_fps = max(signal_fps) if signal_fps else 60.0
            
            results.append({
                'ad_tier': tier_name,
                'content_tier': content_tier,
                'required_fps': required_fps,
                'threshold': config['threshold'],
            })
    
    results_df = pd.DataFrame(results)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    
    pivot = results_df.pivot(index='content_tier', columns='ad_tier', values='required_fps')
    pivot = pivot[['Compliance AD', 'Enhanced AD', 'Audio Cinema']]
    
    x = np.arange(len(pivot.index))
    width = 0.25
    
    colors = {'Compliance AD': '#27ae60', 'Enhanced AD': '#3498db', 'Audio Cinema': '#8e44ad'}
    
    for i, (tier, color) in enumerate(colors.items()):
        offset = (i - 1) * width
        bars = ax.bar(x + offset, pivot[tier], width, label=tier, color=color)
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Minimum Required FPS', fontsize=12)
    ax.set_xlabel('Content Tier', fontsize=12)
    ax.set_title('Recommended FPS by Audio Description Tier', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([t.replace('_', ' ').title() for t in pivot.index])
    ax.legend(loc='upper right')
    
    # Reference lines
    ax.axhline(y=24, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.text(2.5, 25, 'Film (24fps)', fontsize=9, color='gray')
    ax.axhline(y=30, color='gray', linestyle=':', alpha=0.5, linewidth=1)
    ax.text(2.5, 31, 'Broadcast (30fps)', fontsize=9, color='gray')
    
    ax.set_ylim(0, 70)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'ad_tier_fps_requirements.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'ad_tier_fps_requirements.png'}")
    
    # Save CSV
    results_df.to_csv(output_dir / 'ad_tier_fps_mapping.csv', index=False)
    print(f"✅ Saved: {output_dir / 'ad_tier_fps_mapping.csv'}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("AD TIER FPS REQUIREMENTS (FIXED)")
    print("=" * 60)
    print(pivot.to_string())
    
    return results_df

# =============================================================================
# FIX 2: VALIDATION ANALYSIS - Normalize by duration
# =============================================================================

def analyze_validation_normalized(df: pd.DataFrame, output_dir: Path):
    """Compare validation vs core with duration normalization"""
    
    core_df = df[df['study_type'] == 'core'].copy()
    val_df = df[df['study_type'] == 'validation'].copy()
    
    print(f"\nCore study: {len(core_df)} records ({core_df['video_id'].nunique()} videos, ~30s each)")
    print(f"Validation: {len(val_df)} records ({val_df['video_id'].nunique()} videos, ~120s each)")
    
    # Normalize count-based metrics by duration
    count_metrics = ['scene_count', 'unique_object_count', 'transition_count']
    
    for metric in count_metrics:
        if metric in core_df.columns:
            core_df[f'{metric}_per_sec'] = core_df[metric] / core_df['duration']
            val_df[f'{metric}_per_sec'] = val_df[metric] / val_df['duration']
    
    # Compare normalized metrics
    metrics_to_compare = [
        ('scene_count_per_sec', 'Scenes per Second'),
        ('unique_object_count_per_sec', 'Objects per Second'),
        ('person_count_mean', 'Avg Persons (no normalization needed)'),
        ('intensity_mean', 'Motion Intensity (no normalization needed)')
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for ax, (metric, title) in zip(axes, metrics_to_compare):
        if metric not in core_df.columns:
            continue
            
        core_means = core_df.groupby('fps')[metric].mean()
        core_std = core_df.groupby('fps')[metric].std()
        
        val_means = val_df.groupby('fps')[metric].mean()
        val_std = val_df.groupby('fps')[metric].std()
        
        ax.errorbar(core_means.index, core_means.values, yerr=core_std.values/2, 
                   marker='o', label='Core (30s clips)', capsize=3, linewidth=2)
        ax.errorbar(val_means.index, val_means.values, yerr=val_std.values/2,
                   marker='s', label='Validation (120s clips)', capsize=3, linewidth=2)
        
        ax.set_xlabel('FPS')
        ax.set_ylabel(title)
        ax.set_title(title, fontweight='bold')
        ax.set_xscale('log')
        ax.legend()
    
    plt.suptitle('Core vs. Validation: Duration-Normalized Comparison', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'validation_comparison_normalized.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'validation_comparison_normalized.png'}")
    
    # Statistical comparison on normalized metrics
    comparison_results = []
    
    for fps in [1, 10, 24, 60]:
        core_fps = core_df[core_df['fps'] == fps]
        val_fps = val_df[val_df['fps'] == fps]
        
        for metric, _ in metrics_to_compare:
            if metric not in core_df.columns:
                continue
                
            core_vals = core_fps[metric].dropna()
            val_vals = val_fps[metric].dropna()
            
            if len(core_vals) > 1 and len(val_vals) > 1:
                t_stat, p_val = stats.ttest_ind(core_vals, val_vals)
                
                comparison_results.append({
                    'fps': fps,
                    'metric': metric,
                    'core_mean': core_vals.mean(),
                    'val_mean': val_vals.mean(),
                    'pct_diff': (val_vals.mean() - core_vals.mean()) / core_vals.mean() * 100 if core_vals.mean() != 0 else 0,
                    'p_value': p_val,
                    'significant': p_val < 0.05
                })
    
    comparison_df = pd.DataFrame(comparison_results)
    comparison_df.to_csv(output_dir / 'validation_comparison_normalized.csv', index=False)
    print(f"✅ Saved: {output_dir / 'validation_comparison_normalized.csv'}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION COMPARISON (Normalized)")
    print("=" * 60)
    
    sig_diffs = comparison_df[comparison_df['significant'] == True]
    print(f"Significant differences: {len(sig_diffs)} out of {len(comparison_df)}")
    
    if len(sig_diffs) > 0:
        print("\nSignificant differences found:")
        print(sig_diffs[['fps', 'metric', 'pct_diff', 'p_value']].round(3).to_string(index=False))
    else:
        print("\n✅ No significant differences after normalization!")
        print("   Validation confirms core study findings generalize to longer content.")
    
    return comparison_df

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("FIXING ANALYSIS GAPS")
    print("=" * 60)
    
    output_dir = Path("analysis/figures")
    df = load_data()
    
    # Fix 1: AD Tier Mapping
    print("\n--- FIX 1: AD Tier Mapping (using plateau-based thresholds) ---")
    ad_mapping = map_ad_tiers_fixed(df, output_dir)
    
    # Fix 2: Validation with normalization
    print("\n--- FIX 2: Validation Analysis (duration-normalized) ---")
    validation = analyze_validation_normalized(df, output_dir)
    
    print("\n" + "=" * 60)
    print("GAPS ANALYSIS COMPLETE")
    print("=" * 60)
