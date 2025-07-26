import matplotlib.pyplot as plt
import numpy as np
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS, OUR_DATA_KEY, NEO4J_KEY
from data import GDB_TIME_NEIGHBORS_SINGLE, GDB_TIME_NEIGHBORS_TWO, GDB_TIME_FIXEDSIZE_PROPS, GDB_TIME_VARSIZE_PROPS

# Setup fonts
setup_matplotlib_fonts()

# Consistent color scheme
colors = {
    NEO4J_KEY: TECHNIQUE_COLORS['Neo4j'],
    OUR_DATA_KEY: TECHNIQUE_COLORS['Our']
}

def plot_comparison(data, title, filename):
    """Plot comparison between Neo4j and Our implementation."""
    datasets = sorted(list(data.keys()))
    techniques = [NEO4J_KEY, OUR_DATA_KEY]
    
    x = np.arange(len(datasets))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for i, technique in enumerate(techniques):
        values = [data[ds][technique] for ds in datasets]
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, values, width, label=technique, color=colors[technique])
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height > 0 and value > 0:  # Only annotate positive non-zero values
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + max(values) * 0.01,
                    f'{value:.0f}ns',
                    ha='center',
                    va='bottom',
                    fontsize=8,
                    rotation=90
                )
    
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Time (ns)')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    
    # Place legend outside and below the graph, expanding horizontally
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(techniques), 
              frameon=True, fancybox=True, shadow=False, fontsize=13)
    ax.set_yscale('log')  # Use log scale for better visualization of large differences
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for the legend below
    plt.savefig(f"{filename}.pdf", bbox_inches='tight')
    plt.show()

def plot_properties_comparison(fixed_data, varsize_data, title, filename):
    """
    Plot split bar chart with fixed-size properties (positive) and variable-size properties (negative).
    Uses different normalization scales for each property type.
    """
    datasets = sorted(list(fixed_data.keys()))
    techniques = [NEO4J_KEY, OUR_DATA_KEY]
    
    x = np.arange(len(datasets))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate normalization baselines for each property type
    fixed_baselines = {}
    varsize_baselines = {}
    
    for ds in datasets:
        fixed_baselines[ds] = fixed_data[ds][NEO4J_KEY]  # Normalize fixed-size to Neo4j
        varsize_baselines[ds] = varsize_data[ds][NEO4J_KEY]  # Normalize varsize to Neo4j
    
    for i, technique in enumerate(techniques):
        fixed_normalized = []
        varsize_normalized = []
        
        for ds in datasets:
            # Normalize fixed-size properties
            if fixed_baselines[ds] > 0:
                fixed_normalized.append(fixed_data[ds][technique] / fixed_baselines[ds])
            else:
                fixed_normalized.append(0)
            
            # Normalize variable-size properties (negative for display)
            if varsize_baselines[ds] > 0:
                varsize_normalized.append(-(varsize_data[ds][technique] / varsize_baselines[ds]))
            else:
                varsize_normalized.append(0)
        
        offset = (i - 0.5) * width
        
        # Plot fixed-size properties (positive values)
        fixed_bars = ax.bar(x + offset, fixed_normalized, width, 
                           label=f'{technique} - Fixed-size Properties',
                           color=colors[technique], alpha=0.8)
        
        # Plot variable-size properties (negative values)
        varsize_bars = ax.bar(x + offset, varsize_normalized, width,
                             label=f'{technique} - Variable-size Properties', 
                             color=colors[technique], alpha=0.5, hatch='//')
        
        # Add ratio labels for fixed-size properties
        for bar, norm_val in zip(fixed_bars, fixed_normalized):
            if norm_val > 0:
                from config import format_annotation_with_ratio
                annotation_text = format_annotation_with_ratio(0, norm_val, "")
                if annotation_text:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + max(fixed_normalized) * 0.02,
                        annotation_text,
                        ha='center',
                        va='bottom',
                        fontsize=6,
                        rotation=90
                    )
        
        # Add ratio labels for variable-size properties
        for bar, norm_val in zip(varsize_bars, varsize_normalized):
            if norm_val < 0:
                from config import format_annotation_with_ratio
                annotation_text = format_annotation_with_ratio(0, -norm_val, "")
                if annotation_text:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() - abs(min(varsize_normalized)) * 0.02,
                        annotation_text,
                        ha='center',
                        va='top',
                        fontsize=6,
                        rotation=90
                    )
    
    # Add horizontal lines
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)
    ax.axhline(y=-1.0, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)
    
    # Set labels and title
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Relative Time (Neo4j = 1.0)\n← Variable-size Properties | Fixed-size Properties →')
    ax.set_title(title, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=45, ha='right')
    
    # Create custom legend
    import matplotlib.patches as patches
    legend_elements = []
    for technique in techniques:
        # Fixed-size (solid)
        legend_elements.append(patches.Patch(color=colors[technique], alpha=0.8, 
                                           label=f'{technique} - Fixed-size'))
        # Variable-size (hatched)
        legend_elements.append(patches.Patch(color=colors[technique], alpha=0.5, 
                                           hatch='//', label=f'{technique} - Variable-size'))
    
    # Place legend outside and below the graph, expanding horizontally
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
              ncol=min(4, len(legend_elements)), frameon=True, fancybox=True, shadow=False, fontsize=12)
    
    # Set symmetric y-limits
    max_fixed = max(fixed_normalized) if fixed_normalized else 1
    max_varsize = abs(min(varsize_normalized)) if varsize_normalized else 1
    y_limit = max(max_fixed, max_varsize) * 1.3
    ax.set_ylim(-y_limit, y_limit)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # Make room for the legend below
    plt.savefig(f"{filename}.pdf", bbox_inches='tight')
    plt.show()

def plot_combined_gdb_neighbors_comparison(single_hop_data, two_hop_data, title, filename):
    """
    Plot combined single-hop (positive) and two-hop (negative) graph database comparison.
    Uses different normalization scales for each hop type.
    """
    datasets = sorted(list(single_hop_data.keys()))
    techniques = [NEO4J_KEY, OUR_DATA_KEY]
    
    x = np.arange(len(datasets))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate normalization baselines for each hop type
    single_baselines = {}
    two_baselines = {}
    
    for ds in datasets:
        single_baselines[ds] = single_hop_data[ds][NEO4J_KEY]  # Normalize single-hop to Neo4j
        two_baselines[ds] = two_hop_data[ds][NEO4J_KEY]  # Normalize two-hop to Neo4j
    
    for i, technique in enumerate(techniques):
        single_normalized = []
        two_normalized = []
        
        for ds in datasets:
            # Normalize single-hop
            if single_baselines[ds] > 0:
                single_normalized.append(single_hop_data[ds][technique] / single_baselines[ds])
            else:
                single_normalized.append(0)
            
            # Normalize two-hop (negative for display)
            if two_baselines[ds] > 0:
                two_normalized.append(-(two_hop_data[ds][technique] / two_baselines[ds]))
            else:
                two_normalized.append(0)
        
        offset = (i - 0.5) * width
        
        # Plot single-hop (positive values) - same color for both techniques
        single_bars = ax.bar(x + offset, single_normalized, width, 
                           color=colors[technique], alpha=0.8)
        
        # Plot two-hop (negative values) - same color, different pattern
        two_bars = ax.bar(x + offset, two_normalized, width,
                         color=colors[technique], alpha=0.5, hatch='//')
        
        # Add ratio labels for single-hop
        for bar, norm_val in zip(single_bars, single_normalized):
            if norm_val > 0.01:  # Only show labels for values > 0.01 to avoid 0.0x
                from config import format_annotation_with_ratio
                annotation_text = format_annotation_with_ratio(0, norm_val, "")
                if annotation_text and annotation_text != "0.0x":  # Double check to avoid 0.0x
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + max(single_normalized) * 0.02,
                        annotation_text,
                        ha='center',
                        va='bottom',
                        fontsize=6,
                        rotation=90
                    )
        
        # Add ratio labels for two-hop
        for bar, norm_val in zip(two_bars, two_normalized):
            if norm_val < -0.01:  # Only show labels for values < -0.01 to avoid 0.0x
                from config import format_annotation_with_ratio
                annotation_text = format_annotation_with_ratio(0, -norm_val, "")
                if annotation_text and annotation_text != "0.0x":  # Double check to avoid 0.0x
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() - abs(min(two_normalized)) * 0.02,
                        annotation_text,
                        ha='center',
                        va='top',
                        fontsize=6,
                        rotation=90
                    )
    
    # Add horizontal lines
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)
    ax.axhline(y=-1.0, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)
    
    # Set labels and title
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Relative Time (Neo4j = 1.0)\n← Two-hop | Single-hop →')
    ax.set_title(title, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=45, ha='right')
    
    # Create custom legend
    import matplotlib.patches as patches
    legend_elements = []
    for technique in techniques:
        # Single-hop (solid)
        legend_elements.append(patches.Patch(color=colors[technique], alpha=0.8, 
                                           label=f'{technique} - Single-hop'))
        # Two-hop (hatched)
        legend_elements.append(patches.Patch(color=colors[technique], alpha=0.5, 
                                           hatch='//', label=f'{technique} - Two-hop'))
    
    # Place legend outside and below the graph, expanding horizontally
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
              ncol=min(4, len(legend_elements)), frameon=True, fancybox=True, shadow=False, fontsize=12)
    
    # Set symmetric y-limits with minimum threshold for visibility
    max_single = max(single_normalized) if single_normalized else 1
    max_two = abs(min(two_normalized)) if two_normalized else 1
    y_limit = max(max_single, max_two, 0.1) * 1.3  # Ensure minimum scale of 0.1
    ax.set_ylim(-y_limit, y_limit)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # Make room for the legend below
    plt.savefig(f"{filename}.pdf", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_comparison(GDB_TIME_NEIGHBORS_SINGLE, "Single-hop Neighbor Query Performance", "gdb_neighbors_comparison")
    plot_comparison(GDB_TIME_NEIGHBORS_TWO, "Two-hop Neighbor Query Performance", "gdb_neighbors2_comparison")
    plot_comparison(GDB_TIME_FIXEDSIZE_PROPS, "Fixed-size Properties Query Performance", "gdb_fixedsize_props_comparison")
    plot_comparison(GDB_TIME_VARSIZE_PROPS, "Variable-size Properties Query Performance", "gdb_varsize_props_comparison")
    
    # Generate the split properties comparison
    plot_properties_comparison(GDB_TIME_FIXEDSIZE_PROPS, GDB_TIME_VARSIZE_PROPS, 
                              "Graph Database Properties Query Performance", "graphdb_properties_comparison")
    
    # Generate the combined neighbors comparison
    plot_combined_gdb_neighbors_comparison(GDB_TIME_NEIGHBORS_SINGLE, GDB_TIME_NEIGHBORS_TWO,
                                         "Graph Database Neighbor Query Performance", "graphdb_combined_neighbors_comparison")
