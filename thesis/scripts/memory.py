import json
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS

# Setup fonts
setup_matplotlib_fonts()

def load_memory_stats(json_file):
    """Load memory statistics from a JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def group_components(detailed_data):
    """
    Group raw component data into meaningful categories aligned with thesis terminology.
    
    Args:
        detailed_data (dict): Raw component data from JSON
        
    Returns:
        dict: Grouped components with meaningful names
    """
    grouped = {}
    
    # Adjacency Lists - Forward traversal structures
    adj_lists = 0
    if 'nodeAdjLists' in detailed_data:
        adj_lists += detailed_data['nodeAdjLists']
    if 'edgeAdjLists' in detailed_data:
        adj_lists += detailed_data['edgeAdjLists']
    if adj_lists > 0:
        grouped['Adjacency Lists'] = adj_lists
    
    # Parent Lists - Backward traversal structures  
    if 'nodeParentLists' in detailed_data and detailed_data['nodeParentLists'] > 0:
        grouped['Parent Lists'] = detailed_data['nodeParentLists']
    
    # Fixed-size Properties - Integer, date, double, enum properties for nodes and edges
    fixed_props = 0
    fixed_components = ['nodeIntLikeProperties', 'edgeIntLikeProperties', 
                       'nodeDoubleProperties', 'edgeDoubleProperties']
    for comp in fixed_components:
        if comp in detailed_data:
            fixed_props += detailed_data[comp]
    if fixed_props > 0:
        grouped['Fixed-size Properties'] = fixed_props
    
    # Variable-size Properties - String properties and other variable-length data
    if 'varSize' in detailed_data and detailed_data['varSize'] > 0:
        grouped['Variable-size Properties'] = detailed_data['varSize']
    
    # Type System - Node/edge type management and labels
    type_system = 0
    if 'typesSystemOverhead' in detailed_data:
        type_system += detailed_data['typesSystemOverhead']
    if 'labels' in detailed_data:
        type_system += detailed_data['labels']
    if type_system > 0:
        grouped['Type System'] = type_system
    
    # Node Primary Key Index - Mapping between User Node IDs and Internal Node IDs
    if 'nodePkToId' in detailed_data and detailed_data['nodePkToId'] > 0:
        grouped['Node ID Mapping'] = detailed_data['nodePkToId']
    
    # Other - Any remaining components
    accounted_components = {
        'nodeAdjLists', 'edgeAdjLists', 'nodeParentLists',
        'nodeIntLikeProperties', 'edgeIntLikeProperties', 
        'nodeDoubleProperties', 'edgeDoubleProperties',
        'varSize', 'typesSystemOverhead', 'labels', 'nodePkToId'
    }
    
    other_total = 0
    other_components = []
    for comp, size in detailed_data.items():
        if comp not in accounted_components and size > 0:
            other_total += size
            other_components.append(f"{comp}({size//(1024*1024):.1f}MB)")
    
    if other_total > 0:
        grouped['Other'] = other_total
        # Store component details for debugging
        grouped['_other_details'] = other_components
    
    return grouped

def plot_memory_breakdown_stacked(memory_data, output_dir):
    """
    Create a stacked bar chart showing memory usage proportions by component for each dataset.
    Each bar represents 100% of memory usage, split proportionally by components.
    
    Args:
        memory_data (dict): Dictionary with datasets as keys, each containing component sizes
        output_dir (str): Directory to save the plot
    """
    datasets = sorted(list(memory_data.keys()))
    
    # Group components meaningfully and extract all unique categories
    grouped_data = {}
    all_components = set()
    
    for dataset, dataset_data in memory_data.items():
        if 'detailed' in dataset_data:
            grouped = group_components(dataset_data['detailed'])
            # Remove debug info from plotting
            if '_other_details' in grouped:
                del grouped['_other_details']
            grouped_data[dataset] = grouped
            all_components.update(grouped.keys())
    
    # Define preferred order for components (thesis-aligned)
    preferred_order = [
        'Adjacency Lists', 'Parent Lists', 'Fixed-size Properties', 
        'Variable-size Properties', 'Type System', 'Node ID Mapping', 'Other'
    ]
    
    # Sort components according to preferred order, then alphabetically
    all_components = sorted(list(all_components), 
                           key=lambda x: (preferred_order.index(x) if x in preferred_order else len(preferred_order), x))
    
    # Define colors for components (darker colors for better white text contrast)
    component_colors = {
        'Adjacency Lists': '#1f77b4',           # Blue (dark enough for white text)
        'Parent Lists': '#d62728',              # Red (dark enough for white text)  
        'Fixed-size Properties': '#2ca02c',     # Green (dark enough for white text)
        'Variable-size Properties': '#ff7f0e',  # Orange (dark enough for white text)
        'Type System': '#9467bd',               # Purple (dark enough for white text)
        'Node ID Mapping': '#8c564b',           # Brown (dark enough for white text)
        'Other': '#7f7f7f'                      # Gray (dark enough for white text)
    }
    
    # Fallback colors for any unexpected components
    fallback_colors = ['#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    fallback_idx = 0
    for component in all_components:
        if component not in component_colors:
            component_colors[component] = fallback_colors[fallback_idx % len(fallback_colors)]
            fallback_idx += 1
    
    # Calculate proportions for each dataset using grouped data
    proportions_data = {}
    for dataset in datasets:
        if dataset not in grouped_data:
            continue
            
        grouped = grouped_data[dataset]
        total_size = sum(grouped.values())
        
        if total_size == 0:
            continue
            
        proportions = {}
        for component in all_components:
            size = grouped.get(component, 0)
            proportions[component] = (size / total_size) * 100  # Convert to percentage
        
        proportions_data[dataset] = proportions
    
    if not proportions_data:
        print("No valid data found for plotting.")
        return
    
    # Create the stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    datasets_to_plot = sorted(list(proportions_data.keys()))
    x_pos = np.arange(len(datasets_to_plot))
    
    # Create stacked bars
    bottom = np.zeros(len(datasets_to_plot))
    
    for component in all_components:
        values = [proportions_data[dataset][component] for dataset in datasets_to_plot]
        
        # Only plot components that have non-zero values in at least one dataset
        if max(values) > 0:
            bars = ax.bar(x_pos, values, bottom=bottom, label=component, 
                         color=component_colors[component], edgecolor='white', linewidth=0.5)
            
            # Add percentage labels for components that take > 5% of space
            for i, (bar, value) in enumerate(zip(bars, values)):
                if value > 5:  # Only label if > 5%
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., 
                           bottom[i] + height/2.,
                           f'{value:.1f}',
                           ha='center', va='center',
                           fontsize=11, fontweight='bold',
                           color='white')
            
            bottom += values
    
    # Customize the plot
    ax.set_xlabel('Dataset', fontsize=12)
    ax.set_ylabel('Memory Usage (\%)', fontsize=12)
    ax.set_title('Memory Usage Breakdown by Component', fontsize=14, pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(datasets_to_plot, rotation=45, ha='right')
    ax.set_ylim(0, 100)
    
    # Add horizontal grid lines
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Place legend outside and below the graph, expanding horizontally
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=min(4, len(all_components)), 
              frameon=True, fancybox=True, shadow=False, fontsize=12, title="Memory Components")
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # Make room for the legend below
    
    # Save the plot
    output_file = os.path.join(output_dir, 'memory_breakdown_stacked.pdf')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Saved stacked memory breakdown plot: {output_file}")
    plt.show()

def print_memory_summary(memory_data):
    """Print a summary of memory usage for each dataset."""
    print("\n" + "="*80)
    print("MEMORY USAGE SUMMARY (Grouped by Thesis Categories)")
    print("="*80)
    
    for dataset, data in memory_data.items():
        if 'detailed' not in data:
            continue
            
        # Group components meaningfully
        grouped = group_components(data['detailed'])
        other_details = grouped.pop('_other_details', [])
        
        total_size = sum(grouped.values())
        total_mb = total_size / (1024 * 1024)
        
        print(f"\nDataset: {dataset}")
        print(f"Total Memory: {total_mb:.2f} MB ({total_size:,} bytes)")
        print("-" * 50)
        
        # Sort components by size (descending)
        sorted_components = sorted(grouped.items(), key=lambda x: x[1], reverse=True)
        
        for component, size in sorted_components:
            size_mb = size / (1024 * 1024)
            percentage = (size / total_size) * 100
            print(f"  {component:<25}: {size_mb:>8.2f} MB ({percentage:>5.1f}%)")
        
        # Show details for "Other" category if present
        if other_details:
            print(f"    └─ Other details: {', '.join(other_details)}")
            
        print(f"\nRaw component breakdown for {dataset}:")
        print("-" * 30)
        detailed = data['detailed']
        raw_sorted = sorted(detailed.items(), key=lambda x: x[1], reverse=True)
        for component, size in raw_sorted:
            size_mb = size / (1024 * 1024)
            percentage = (size / sum(detailed.values())) * 100
            print(f"  {component:<25}: {size_mb:>6.2f} MB ({percentage:>4.1f}%)")

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Visualize graph database memory usage breakdown')
    parser.add_argument('json_file', help='Path to the JSON file with memory statistics')
    parser.add_argument('--output', '-o', default='./plots', help='Output directory for plots')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Load statistics
    memory_data = load_memory_stats(args.json_file)
    
    # Print summary
    print_memory_summary(memory_data)
    
    # Generate stacked bar chart
    plot_memory_breakdown_stacked(memory_data, args.output)

if __name__ == "__main__":
    main()