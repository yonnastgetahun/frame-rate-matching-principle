#!/usr/bin/env python3
"""
Statistical Analysis and Temporal Signal Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from itertools import combinations

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_data():
    df = pd.read_parquet("analysis/signals_df.parquet")
    return df

# =============================================================================
# TEMPORAL ANALYSIS
# =============================================================================

def analyze_temporal_signals(df: pd.DataFrame, output_dir: Path):
    """Analyze temporal signals across FPS levels"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Change Score Mean (frame-to-frame visual change)
    ax = axes[0, 0]
    for tier in ['web_ugc', 'produced_digital', 'cinema']:
        tier_data = df[df['tier'] == tier].groupby('fps')['change_score_mean'].mean()
        ax.plot(tier_data.index, tier_data.values, marker='o', label=tier.replace('_', ' ').title())
    ax.set_xlabel('FPS')
    ax.set_ylabel('Mean Change Score')
    ax.set_title('Frame-to-Frame Visual Change vs FPS', fontweight='bold')
    ax.set_xscale('log')
    ax.legend()
    
    # 2. Temporal Density
    ax = axes[0, 1]
    for tier in ['web_ugc', 'produced_digital', 'cinema']:
        tier_data = df[df['tier'] == tier].groupby('fps')['temporal_density'].mean()
        ax.plot(tier_data.index, tier_data.values, marker='o', label=tier.replace('_', ' ').title())
    ax.set_xlabel('FPS')
    ax.set_ylabel('Temporal Density')
    ax.set_title('Temporal Event Density vs FPS', fontweight='bold')
    ax.set_xscale('log')
    ax.legend()
    
    # 3. Scene Duration Mean
    ax = axes[1, 0]
    for tier in ['web_ugc', 'produced_digital', 'cinema']:
        tier_data = df[df['tier'] == tier].groupby('fps')['scene_duration_mean'].mean()
        ax.plot(tier_data.index, tier_data.values, marker='o', label=tier.replace('_', ' ').title())
    ax.set_xlabel('FPS')
    ax.set_ylabel('Mean Scene Duration (sec)')
    ax.set_title('Average Scene Duration vs FPS', fontweight='bold')
    ax.set_xscale('log')
    ax.legend()
    
    # 4. Transition Count
    ax = axes[1, 1]
    for tier in ['web_ugc', 'produced_digital', 'cinema']:
        tier_data = df[df['tier'] == tier].groupby('fps')['transition_count'].mean()
        ax.plot(tier_data.index, tier_data.values, marker='o', label=tier.replace('_', ' ').title())
    ax.set_xlabel('FPS')
    ax.set_ylabel('Transition Count')
    ax.set_title('Scene Transitions Detected vs FPS', fontweight='bold')
    ax.set_xscale('log')
    ax.legend()
    
    plt.suptitle('Temporal Signal Analysis Across FPS Levels', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'temporal_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'temporal_analysis.png'}")

def analyze_frame_level_patterns(df: pd.DataFrame, output_dir: Path):
    """Analyze how signals change with frame count"""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Frame count vs various metrics
    metrics = [
        ('frame_count', 'unique_object_count', 'Objects vs Frame Count'),
        ('frame_count', 'scene_count', 'Scenes vs Frame Count'),
        ('frame_count', 'change_score_mean', 'Change Score vs Frame Count'),
    ]
    
    for ax, (x_col, y_col, title) in zip(axes, metrics):
        for tier in ['web_ugc', 'produced_digital', 'cinema']:
            tier_df = df[df['tier'] == tier]
            ax.scatter(tier_df[x_col], tier_df[y_col], alpha=0.3, label=tier.replace('_', ' ').title(), s=10)
        ax.set_xlabel('Frame Count')
        ax.set_ylabel(y_col.replace('_', ' ').title())
        ax.set_title(title, fontweight='bold')
        ax.legend()
    
    plt.suptitle('Signal Detection vs Frame Count', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'frame_level_patterns.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'frame_level_patterns.png'}")

# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def run_anova_tests(df: pd.DataFrame, output_dir: Path):
    """Run ANOVA tests comparing tiers at each FPS level"""
    
    metrics = ['scene_count', 'unique_object_count', 'person_count_mean', 
               'intensity_mean', 'change_score_mean', 'temporal_density']
    
    fps_levels = sorted(df['fps'].unique())
    
    results = []
    
    for fps in fps_levels:
        fps_df = df[df['fps'] == fps]
        
        for metric in metrics:
            groups = [fps_df[fps_df['tier'] == t][metric].dropna().values 
                     for t in ['cinema', 'produced_digital', 'web_ugc']]
            
            # Filter out empty groups
            groups = [g for g in groups if len(g) > 0]
            
            if len(groups) >= 2:
                try:
                    f_stat, p_value = stats.f_oneway(*groups)
                    
                    # Effect size (eta-squared)
                    all_values = np.concatenate(groups)
                    grand_mean = np.mean(all_values)
                    ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
                    ss_total = sum((v - grand_mean)**2 for v in all_values)
                    eta_squared = ss_between / ss_total if ss_total > 0 else 0
                    
                    results.append({
                        'fps': fps,
                        'metric': metric,
                        'f_statistic': f_stat,
                        'p_value': p_value,
                        'eta_squared': eta_squared,
                        'significant': p_value < 0.05,
                        'effect_size': 'large' if eta_squared > 0.14 else ('medium' if eta_squared > 0.06 else 'small')
                    })
                except Exception as e:
                    pass
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_dir / 'anova_results.csv', index=False)
    print(f"✅ Saved: {output_dir / 'anova_results.csv'}")
    
    # Summary visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    
    pivot = results_df.pivot(index='fps', columns='metric', values='eta_squared')
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax,
                cbar_kws={'label': 'Effect Size (η²)'})
    ax.set_title('ANOVA Effect Sizes: Tier Differences by FPS Level', fontsize=14, fontweight='bold')
    ax.set_xlabel('Metric')
    ax.set_ylabel('FPS Level')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'anova_effect_sizes.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'anova_effect_sizes.png'}")
    
    return results_df

def run_pairwise_comparisons(df: pd.DataFrame, output_dir: Path):
    """Run pairwise t-tests between tiers"""
    
    metrics = ['scene_count', 'unique_object_count', 'person_count_mean', 'intensity_mean']
    tier_pairs = [('cinema', 'produced_digital'), ('cinema', 'web_ugc'), ('produced_digital', 'web_ugc')]
    
    # Test at key FPS levels
    key_fps = [1, 10, 24, 60]
    
    results = []
    
    for fps in key_fps:
        fps_df = df[df['fps'] == fps]
        
        for metric in metrics:
            for tier1, tier2 in tier_pairs:
                g1 = fps_df[fps_df['tier'] == tier1][metric].dropna().values
                g2 = fps_df[fps_df['tier'] == tier2][metric].dropna().values
                
                if len(g1) > 1 and len(g2) > 1:
                    t_stat, p_value = stats.ttest_ind(g1, g2)
                    
                    # Cohen's d effect size
                    pooled_std = np.sqrt(((len(g1)-1)*np.std(g1)**2 + (len(g2)-1)*np.std(g2)**2) / (len(g1)+len(g2)-2))
                    cohens_d = (np.mean(g1) - np.mean(g2)) / pooled_std if pooled_std > 0 else 0
                    
                    results.append({
                        'fps': fps,
                        'metric': metric,
                        'comparison': f'{tier1} vs {tier2}',
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'cohens_d': cohens_d,
                        'significant': p_value < 0.05,
                        'mean_diff': np.mean(g1) - np.mean(g2)
                    })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_dir / 'pairwise_comparisons.csv', index=False)
    print(f"✅ Saved: {output_dir / 'pairwise_comparisons.csv'}")
    
    return results_df

def analyze_fps_thresholds(df: pd.DataFrame, output_dir: Path):
    """Determine optimal FPS thresholds for each metric and tier"""
    
    metrics = ['scene_count', 'unique_object_count', 'person_count_mean', 
               'intensity_mean', 'change_score_mean']
    
    results = []
    
    for tier in df['tier'].unique():
        tier_df = df[df['tier'] == tier]
        
        for metric in metrics:
            # Get mean values by FPS
            fps_means = tier_df.groupby('fps')[metric].mean().sort_index()
            
            if len(fps_means) < 2:
                continue
            
            # Find the FPS where 90% of max value is reached
            max_val = fps_means.max()
            min_val = fps_means.min()
            
            if max_val > min_val:
                threshold_90 = min_val + 0.9 * (max_val - min_val)
                
                # Find first FPS that exceeds threshold
                for fps, val in fps_means.items():
                    if val >= threshold_90:
                        optimal_fps_90 = fps
                        break
                else:
                    optimal_fps_90 = fps_means.index[-1]
            else:
                optimal_fps_90 = fps_means.index[0]
            
            # Find FPS where gains drop below 5%
            fps_list = list(fps_means.index)
            optimal_fps_diminishing = fps_list[-1]
            
            for i in range(1, len(fps_list)):
                prev_val = fps_means[fps_list[i-1]]
                curr_val = fps_means[fps_list[i]]
                
                if prev_val > 0:
                    pct_change = abs(curr_val - prev_val) / prev_val
                    if pct_change < 0.05:
                        optimal_fps_diminishing = fps_list[i]
                        break
            
            results.append({
                'tier': tier,
                'metric': metric,
                'optimal_fps_90pct': optimal_fps_90,
                'optimal_fps_diminishing': optimal_fps_diminishing,
                'max_value': max_val,
                'min_value': min_val,
                'range': max_val - min_val
            })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_dir / 'fps_thresholds.csv', index=False)
    print(f"✅ Saved: {output_dir / 'fps_thresholds.csv'}")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 90% threshold
    pivot_90 = results_df.pivot(index='tier', columns='metric', values='optimal_fps_90pct')
    sns.heatmap(pivot_90, annot=True, fmt='.0f', cmap='viridis', ax=axes[0],
                cbar_kws={'label': 'FPS'})
    axes[0].set_title('FPS to Reach 90% of Max Signal', fontsize=12, fontweight='bold')
    
    # Diminishing returns threshold
    pivot_dim = results_df.pivot(index='tier', columns='metric', values='optimal_fps_diminishing')
    sns.heatmap(pivot_dim, annot=True, fmt='.0f', cmap='viridis', ax=axes[1],
                cbar_kws={'label': 'FPS'})
    axes[1].set_title('FPS Where Gains Drop Below 5%', fontsize=12, fontweight='bold')
    
    plt.suptitle('Optimal FPS Thresholds by Tier and Metric', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'fps_thresholds.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'fps_thresholds.png'}")
    
    return results_df

# =============================================================================
# ADDITIONAL VISUALIZATIONS
# =============================================================================

def plot_variance_analysis(df: pd.DataFrame, output_dir: Path):
    """Analyze within-tier variance at different FPS levels"""
    
    metrics = ['scene_count', 'unique_object_count', 'intensity_mean']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for ax, metric in zip(axes, metrics):
        variance_data = df.groupby(['tier', 'fps'])[metric].std().reset_index()
        
        for tier in ['web_ugc', 'produced_digital', 'cinema']:
            tier_data = variance_data[variance_data['tier'] == tier]
            ax.plot(tier_data['fps'], tier_data[metric], marker='o', 
                   label=tier.replace('_', ' ').title())
        
        ax.set_xlabel('FPS')
        ax.set_ylabel('Standard Deviation')
        ax.set_title(f'{metric.replace("_", " ").title()} Variance', fontweight='bold')
        ax.set_xscale('log')
        ax.legend()
    
    plt.suptitle('Signal Variance Across FPS Levels', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'variance_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'variance_analysis.png'}")

def plot_correlation_matrix(df: pd.DataFrame, output_dir: Path):
    """Plot correlation between different signals"""
    
    signal_cols = ['scene_count', 'transition_count', 'unique_object_count', 
                   'person_count_mean', 'intensity_mean', 'change_score_mean',
                   'temporal_density', 'brightness_mean']
    
    # Filter to available columns
    signal_cols = [c for c in signal_cols if c in df.columns]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for ax, tier in zip(axes, ['cinema', 'produced_digital', 'web_ugc']):
        tier_df = df[df['tier'] == tier][signal_cols]
        corr = tier_df.corr()
        
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                   ax=ax, vmin=-1, vmax=1, center=0)
        ax.set_title(f'{tier.replace("_", " ").title()}', fontweight='bold')
    
    plt.suptitle('Signal Correlations by Content Tier', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'correlation_matrix.png'}")

def plot_box_comparisons(df: pd.DataFrame, output_dir: Path):
    """Box plots comparing distributions at key FPS levels"""
    
    key_fps = [1, 10, 24, 60]
    metrics = ['scene_count', 'unique_object_count', 'intensity_mean']
    
    fig, axes = plt.subplots(len(metrics), len(key_fps), figsize=(16, 12))
    
    for i, metric in enumerate(metrics):
        for j, fps in enumerate(key_fps):
            ax = axes[i, j]
            fps_df = df[df['fps'] == fps]
            
            sns.boxplot(data=fps_df, x='tier', y=metric, ax=ax, 
                       order=['cinema', 'produced_digital', 'web_ugc'])
            ax.set_xlabel('')
            ax.set_ylabel(metric.replace('_', ' ').title() if j == 0 else '')
            ax.set_title(f'{fps} FPS' if i == 0 else '')
            ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle('Signal Distributions by Tier at Key FPS Levels', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'box_comparisons.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {output_dir / 'box_comparisons.png'}")

def generate_summary_table(df: pd.DataFrame, anova_df: pd.DataFrame, threshold_df: pd.DataFrame, output_dir: Path):
    """Generate a publication-ready summary table"""
    
    # Key findings summary
    summary = []
    
    for tier in ['cinema', 'produced_digital', 'web_ugc']:
        tier_thresholds = threshold_df[threshold_df['tier'] == tier]
        
        avg_90pct = tier_thresholds['optimal_fps_90pct'].mean()
        avg_diminishing = tier_thresholds['optimal_fps_diminishing'].mean()
        
        tier_df = df[df['tier'] == tier]
        n_videos = tier_df['video_id'].nunique()
        n_records = len(tier_df)
        
        summary.append({
            'Tier': tier.replace('_', ' ').title(),
            'Videos': n_videos,
            'Records': n_records,
            'Avg 90% Threshold FPS': f'{avg_90pct:.1f}',
            'Avg Diminishing Returns FPS': f'{avg_diminishing:.1f}',
            'Recommended FPS': f'{max(avg_90pct, avg_diminishing):.0f}'
        })
    
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(output_dir / 'publication_summary.csv', index=False)
    print(f"✅ Saved: {output_dir / 'publication_summary.csv'}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PUBLICATION SUMMARY")
    print("=" * 60)
    print(summary_df.to_string(index=False))
    
    return summary_df

if __name__ == "__main__":
    print("=" * 60)
    print("STATISTICAL ANALYSIS & ADDITIONAL VISUALIZATIONS")
    print("=" * 60)
    
    output_dir = Path("analysis/figures")
    output_dir.mkdir(exist_ok=True)
    
    df = load_data()
    print(f"\nLoaded {len(df)} records")
    
    # Temporal Analysis
    print("\n--- Temporal Signal Analysis ---")
    analyze_temporal_signals(df, output_dir)
    analyze_frame_level_patterns(df, output_dir)
    
    # Statistical Tests
    print("\n--- Statistical Tests ---")
    anova_df = run_anova_tests(df, output_dir)
    pairwise_df = run_pairwise_comparisons(df, output_dir)
    threshold_df = analyze_fps_thresholds(df, output_dir)
    
    # Additional Visualizations
    print("\n--- Additional Visualizations ---")
    plot_variance_analysis(df, output_dir)
    plot_correlation_matrix(df, output_dir)
    plot_box_comparisons(df, output_dir)
    
    # Summary
    print("\n--- Generating Summary ---")
    summary_df = generate_summary_table(df, anova_df, threshold_df, output_dir)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nAll outputs saved to: {output_dir}/")
