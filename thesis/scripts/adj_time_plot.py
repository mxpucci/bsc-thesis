'''
This script plots the time taken by the different graph representations on the different datasets to run neighborhood queries.

It normalizes the space usage of the different graph representations to the CSR baseline.

'''

import matplotlib.pyplot as plt
import numpy as np
import copy # Used for deep copying data
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS, OUR_DATA_KEY, CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY, format_annotation_with_ratio
from data import TIME_NEIGHBORS_SINGLE_HOP, TIME_NEIGHBORS_TWO_HOP

# Setup fonts
setup_matplotlib_fonts()

# Consistent colors matching other scripts
colors = {
    CSR_BASELINE_KEY: TECHNIQUE_COLORS['CSR'],
    LOGGRAPH_KEY: TECHNIQUE_COLORS['LogGraph'],
    CGRAPHINDEX_KEY: TECHNIQUE_COLORS['CGraphIndex'],
    OUR_DATA_KEY: TECHNIQUE_COLORS['Our']
}

def plot_time_comparison_normalized(data, title, filename, normalize_to=CSR_BASELINE_KEY):
    """Plot time comparison normalized to CSR baseline."""
    datasets = sorted(list(data.keys()))
    techniques = [CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY, OUR_DATA_KEY]
    
    # Filter out techniques with all zero values (like CGraphIndex for some datasets)
    available_techniques = []
    for tech in techniques:
        has_data = any(data[ds][tech] > 0 for ds in datasets if tech in data[ds])
        if has_data:
            available_techniques.append(tech)
    
    x = np.arange(len(datasets))
    width = 0.8 / len(available_techniques)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for i, technique in enumerate(available_techniques):
        normalized_values = []
        absolute_values = []
        
        for ds in datasets:
            if technique in data[ds] and normalize_to in data[ds]:
                base_value = data[ds][normalize_to]
                current_value = data[ds][technique]
                
                if base_value > 0:
                    normalized_values.append(current_value / base_value)
                    absolute_values.append(current_value)
                else:
                    normalized_values.append(0)
                    absolute_values.append(0)
            else:
                normalized_values.append(0)
                absolute_values.append(0)
        
        offset = (i - (len(available_techniques) - 1) / 2) * width
        bars = ax.bar(x + offset, normalized_values, width, label=technique, color=colors[technique])
        
        # Add annotations with both absolute time and normalization ratio
        for bar, abs_val, norm_val in zip(bars, absolute_values, normalized_values):
            height = bar.get_height()
            if height > 0:  # Only annotate non-zero values
                annotation_text = format_annotation_with_ratio(abs_val, norm_val, "ms")
                
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + max(normalized_values) * 0.02,
                    annotation_text,
                    ha='center',
                    va='bottom',
                    fontsize=7,
                    rotation=90
                )
    
    # Add baseline line
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, label=f'{normalize_to} baseline (1.0)')
    
    ax.set_xlabel('Dataset')
    ax.set_ylabel(f'Relative Time ({normalize_to} = 1.0)')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    
    # Place legend outside and below the graph, expanding horizontally
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(available_techniques) + 1, 
              frameon=True, fancybox=True, shadow=False, fontsize=13)
    
    # Set reasonable y-limits with extra space for annotations
    if normalized_values:
        max_val = max(normalized_values)
        ax.set_ylim(0, max_val * 1.8)  # Increased from 1.5 to 1.8 to accommodate labels
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for the legend below
    plt.savefig(f"{filename}.pdf", bbox_inches='tight')
    plt.show()

def plot_combined_neighbors_comparison(single_hop_data, two_hop_data, title, filename, normalize_to=CSR_BASELINE_KEY):
    """Plot combined single-hop (top) and two-hop (bottom) neighbor comparison."""
    datasets = sorted(list(single_hop_data.keys()))
    techniques = [CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY, OUR_DATA_KEY]
    
    # Filter out techniques with all zero values
    available_techniques = []
    for tech in techniques:
        has_single_data = any(single_hop_data[ds][tech] > 0 for ds in datasets if tech in single_hop_data[ds])
        has_two_data = any(two_hop_data[ds][tech] > 0 for ds in datasets if tech in two_hop_data[ds])
        if has_single_data or has_two_data:
            available_techniques.append(tech)
    
    x = np.arange(len(datasets))
    width = 0.8 / len(available_techniques)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for i, technique in enumerate(available_techniques):
        # Single-hop data (positive values)
        single_normalized = []
        two_normalized = []
        
        for ds in datasets:
            # Single-hop normalization
            if technique in single_hop_data[ds] and normalize_to in single_hop_data[ds]:
                base_value = single_hop_data[ds][normalize_to]
                current_value = single_hop_data[ds][technique]
                single_normalized.append(current_value / base_value if base_value > 0 else 0)
            else:
                single_normalized.append(0)
            
            # Two-hop normalization (negative for display)
            if technique in two_hop_data[ds] and normalize_to in two_hop_data[ds]:
                base_value = two_hop_data[ds][normalize_to]
                current_value = two_hop_data[ds][technique]
                two_normalized.append(-(current_value / base_value) if base_value > 0 else 0)
            else:
                two_normalized.append(0)
        
        offset = (i - (len(available_techniques) - 1) / 2) * width
        
        # Plot single-hop (positive) - same color for each technique
        single_bars = ax.bar(x + offset, single_normalized, width, 
                           color=colors[technique], alpha=0.8)
        
        # Plot two-hop (negative) - same color, different pattern
        two_bars = ax.bar(x + offset, two_normalized, width,
                         color=colors[technique], alpha=0.5, hatch='//')
        
        # Add annotations for single-hop
        for bar, norm_val in zip(single_bars, single_normalized):
            if norm_val > 0.01:  # Only show labels for values > 0.01 to avoid 0.0x
                annotation_text = format_annotation_with_ratio(0, norm_val, "")
                if annotation_text and annotation_text != "0.0x":  # Only add if not empty and not 0.0x
                    ax.text(bar.get_x() + bar.get_width() / 2,
                           bar.get_height() + max(single_normalized) * 0.02,
                           annotation_text, ha='center', va='bottom', fontsize=6, rotation=90)
        
        # Add annotations for two-hop
        for bar, norm_val in zip(two_bars, two_normalized):
            if norm_val < -0.01:  # Only show labels for values < -0.01 to avoid 0.0x
                annotation_text = format_annotation_with_ratio(0, -norm_val, "")
                if annotation_text and annotation_text != "0.0x":  # Only add if not empty and not 0.0x
                    ax.text(bar.get_x() + bar.get_width() / 2,
                           bar.get_height() - abs(min(two_normalized)) * 0.02,
                           annotation_text, ha='center', va='top', fontsize=6, rotation=90)
    
    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)
    ax.axhline(y=-1.0, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)
    
    ax.set_xlabel('Dataset')
    ax.set_ylabel(f'Relative Time ({normalize_to} = 1.0)\n← Two-hop | Single-hop →')
    ax.set_title(title, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=45, ha='right')
    
    # Set symmetric y-limits with extra space for annotations
    max_single = max(single_normalized) if single_normalized else 1
    max_two = abs(min(two_normalized)) if two_normalized else 1
    y_limit = max(max_single, max_two, 0.1) * 1.6  # Increased from 1.3 to 1.6 to accommodate labels
    ax.set_ylim(-y_limit, y_limit)
    
    # Create custom legend
    import matplotlib.patches as patches
    legend_elements = []
    for technique in available_techniques:
        legend_elements.append(patches.Patch(color=colors[technique], alpha=0.8, 
                                           label=f'{technique} - Single-hop'))
        legend_elements.append(patches.Patch(color=colors[technique], alpha=0.5, 
                                           hatch='//', label=f'{technique} - Two-hop'))
    
    # Place legend outside and below the graph, expanding horizontally
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
              ncol=min(4, len(legend_elements)), frameon=True, fancybox=True, shadow=False, fontsize=12)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # Make room for the legend below
    plt.savefig(f"{filename}.pdf", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_time_comparison_normalized(TIME_NEIGHBORS_SINGLE_HOP, "Single-hop Neighbor Query Time (Normalized to CSR)", "adj_neighbors_time_normalized")
    plot_time_comparison_normalized(TIME_NEIGHBORS_TWO_HOP, "Two-hop Neighbor Query Time (Normalized to CSR)", "adj_neighbors2_time_normalized")
    plot_combined_neighbors_comparison(TIME_NEIGHBORS_SINGLE_HOP, TIME_NEIGHBORS_TWO_HOP, 
                                     "Neighbor Query Performance Comparison", "adj_combined_neighbors_comparison")