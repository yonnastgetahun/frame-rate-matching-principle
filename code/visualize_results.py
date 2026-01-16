#!/usr/bin/env python3
"""
Visualize FPS signal extraction results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_data():
    """Load processed data"""
    df = pd.read_parquet("analysis/signals_df.parquet")
    agg_df = pd.read_parquet("analysis/metrics_by_fps.parquet")
    stability_df = pd.read_parquet("analysis/signal_stability.parquet")
    return df, agg_df, stability_df

def plot_signal_by_fps(df: pd.DataFrame, output_dir: Path):
    """Plot signal metrics across FPS levels by tier"""
    
    metrics = [
        ('scene_count', 'Scene Transitions Detected'),
        ('unique_object_count', 'Unique Objects Detected'),
        ('person_count_mean', 'Average Persons per Frame'),
        ('intensity_mean', 'Motion Intensity'),
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for ax, (metric, title) in zip(axes, metrics):
        # Aggregate by tier and fps
        agg = df.groupby(['tier', 'fps'])[metric].mean().reset_index()
        
        for tier in ['web_ugc', 'produced_digital', 'cinema']:
            tier_data = agg[agg['tier'] == tier]
            ax.plot(tier_data['fps'], tier_data[metric], 
                   marker='o', linewidth=2, markersize=6, label=tier.replace('_', ' ').title())
        
        ax.set_xlabel('FPS', fontsize=11)
        ax.set_ylabel(title, fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xscale('log')
        ax.set_xticks([0.5, 1, 2, 5, 10, 15, 24, 30, 60, 120, 240])
        ax.set_xticklabels(['0.5', '1', '2', '5', '10', '15', '24', '30', '60', '120', '240'])
        ax.legend(loc='best')
    
    plt.suptitle('Signal Extraction Quality vs FPS by Content Tier', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'signal_by_fps.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'signal_by_fps.png'}")

def plot_diminishing_returns(df: pd.DataFrame, output_dir: Path):
    """Plot diminishing returns analysis"""
    
    metrics = ['scene_count', 'unique_object_count', 'person_count_mean']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    fps_pairs = [(0.5, 1), (1, 5), (5, 10), (10, 15), (15, 24), (24, 30), (30, 60), (60, 120), (120, 240)]
    
    for ax, metric in zip(axes, metrics):
        for tier in ['web_ugc', 'produced_digital', 'cinema']:
            tier_df = df[df['tier'] == tier]
            gains = []
            labels = []
            
            for fps_low, fps_high in fps_pairs:
                low_val = tier_df[tier_df['fps'] == fps_low][metric].mean()
                high_val = tier_df[tier_df['fps'] == fps_high][metric].mean()
                
                if low_val > 0:
                    pct_gain = (high_val - low_val) / low_val * 100
                else:
                    pct_gain = 0
                
                gains.append(pct_gain)
                labels.append(f"{fps_low}→{fps_high}")
            
            ax.plot(range(len(gains)), gains, marker='o', label=tier.replace('_', ' ').title())
        
        ax.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='5% threshold')
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel('% Change')
        ax.set_title(metric.replace('_', ' ').title())
        ax.legend(loc='best', fontsize=8)
    
    plt.suptitle('Diminishing Returns: Signal Gain Between FPS Levels', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'diminishing_returns.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'diminishing_returns.png'}")

def plot_stability_heatmap(stability_df: pd.DataFrame, output_dir: Path):
    """Plot stabilization FPS heatmap"""
    
    # Compute median stable FPS per tier/metric
    pivot = stability_df.groupby(['tier', 'metric'])['stable_fps'].median().unstack()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, 
                cbar_kws={'label': 'Median Stabilization FPS'})
    ax.set_title('Signal Stabilization FPS by Tier and Metric', fontsize=14, fontweight='bold')
    ax.set_xlabel('Metric')
    ax.set_ylabel('Content Tier')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'stability_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'stability_heatmap.png'}")

def plot_tier_comparison(df: pd.DataFrame, output_dir: Path):
    """Compare tiers at key FPS thresholds"""
    
    key_fps = [1, 10, 24, 60, 120]
    metrics = ['scene_count', 'unique_object_count', 'intensity_mean']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for ax, metric in zip(axes, metrics):
        plot_data = df[df['fps'].isin(key_fps)].groupby(['tier', 'fps'])[metric].mean().unstack()
        plot_data.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title(metric.replace('_', ' ').title())
        ax.set_xlabel('Content Tier')
        ax.set_ylabel('Mean Value')
        ax.legend(title='FPS', bbox_to_anchor=(1.02, 1))
        ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle('Tier Comparison at Key FPS Levels', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'tier_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'tier_comparison.png'}")

def generate_summary_stats(df: pd.DataFrame, output_dir: Path):
    """Generate summary statistics table"""
    
    # Summary by tier
    tier_summary = df.groupby('tier').agg({
        'video_id': 'nunique',
        'scene_count': ['mean', 'std'],
        'unique_object_count': ['mean', 'std'],
        'person_count_mean': ['mean', 'std'],
        'intensity_mean': ['mean', 'std'],
    }).round(2)
    
    tier_summary.to_csv(output_dir / 'tier_summary.csv')
    print(f"✅ Saved: {output_dir / 'tier_summary.csv'}")
    
    # Summary by FPS
    fps_summary = df.groupby('fps').agg({
        'video_id': 'count',
        'scene_count': 'mean',
        'unique_object_count': 'mean',
        'person_count_mean': 'mean',
    }).round(2)
    
    fps_summary.to_csv(output_dir / 'fps_summary.csv')
    print(f"✅ Saved: {output_dir / 'fps_summary.csv'}")
    
    return tier_summary, fps_summary

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    output_dir = Path("analysis/figures")
    output_dir.mkdir(exist_ok=True)
    
    df, agg_df, stability_df = load_data()
    
    print(f"\nLoaded {len(df)} records")
    print(f"Tiers: {df['tier'].unique().tolist()}")
    print(f"FPS levels: {sorted(df['fps'].unique().tolist())}")
    
    print("\n--- Generating Plots ---")
    plot_signal_by_fps(df, output_dir)
    plot_diminishing_returns(df, output_dir)
    plot_stability_heatmap(stability_df, output_dir)
    plot_tier_comparison(df, output_dir)
    
    print("\n--- Generating Summary Stats ---")
    tier_summary, fps_summary = generate_summary_stats(df, output_dir)
    
    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETE")
    print("=" * 60)
    print(f"\nOutput: {output_dir}/")
