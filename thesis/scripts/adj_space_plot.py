'''
This script plots the space usage of the different graph representations.

It normalizes the space usage of the different graph representations to the CSR baseline.

'''

import matplotlib.pyplot as plt
import numpy as np
import copy # Used for deep copying data
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS, OUR_DATA_KEY, CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY, to_MB, format_annotation_with_ratio
from data import SPACE_DATA

# Setup fonts
setup_matplotlib_fonts()

def plot_normalized_with_annotation(data_to_plot, datasets_list, include_our_data=False):
    """
    Generates and saves a bar plot of graph storage sizes, normalized relative to CSR.

    Args:
        data_to_plot (dict): The dataset dictionary.
        datasets_list (list): List of dataset names (keys in data_to_plot).
        include_our_data (bool): If True, includes the 'Our' data series in the plot.
    """
    current_data = copy.deepcopy(data_to_plot) # Use a copy to avoid modifying original data

    base_formats = [CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY]
    base_format_colors = {
        CSR_BASELINE_KEY: TECHNIQUE_COLORS['CSR'],
        LOGGRAPH_KEY: TECHNIQUE_COLORS['LogGraph'],
        CGRAPHINDEX_KEY: TECHNIQUE_COLORS['CGraphIndex']
    }

    if include_our_data:
        current_formats = base_formats + [OUR_DATA_KEY]
        current_format_colors = {**base_format_colors, OUR_DATA_KEY: TECHNIQUE_COLORS['Our']} # Red color for 'Our' (standardized)
        file_suffix = "_with_our"
        title_suffix = ""
    else:
        current_formats = base_formats
        current_format_colors = base_format_colors
        # Remove OUR_DATA_KEY from data if it exists and we are not including it
        for ds_values in current_data.values():
            ds_values.pop(OUR_DATA_KEY, None)
        file_suffix = "_without_our"
        title_suffix = ""


    normalized_sizes = []
    absolute_sizes_MB = []

    for ds_name in datasets_list:
        if CSR_BASELINE_KEY not in current_data[ds_name]:
            print(f"Warning: {CSR_BASELINE_KEY} data missing for dataset {ds_name}. Skipping.")
            continue

        csr_size = current_data[ds_name][CSR_BASELINE_KEY]
        temp_normalized = []
        temp_absolute_MB = []

        for fmt in current_formats:
            if fmt in current_data[ds_name]:
                size = current_data[ds_name][fmt]
                temp_normalized.append(size / csr_size)
                temp_absolute_MB.append(to_MB(size))
            else:
                # Handle cases where a format might be missing for a dataset (e.g. 'Our' if include_our_data is False)
                # This shouldn't happen with the current logic for 'Our', but good for robustness
                temp_normalized.append(0) # Or np.nan, depending on how you want to handle
                temp_absolute_MB.append(0) # Or np.nan

        normalized_sizes.append(temp_normalized)
        absolute_sizes_MB.append(temp_absolute_MB)

    if not normalized_sizes: # If no data was processed
        print("No data to plot.")
        return

    normalized_sizes_np = np.array(normalized_sizes)
    absolute_sizes_MB_np = np.array(absolute_sizes_MB)

    x = np.arange(len(datasets_list))
    num_formats = len(current_formats)
    total_width_for_bars = 0.8 # Total width allocated for all bars for a single dataset
    width_per_bar = total_width_for_bars / num_formats

    # Adjust starting position for centering bars
    start_offset = - (total_width_for_bars - width_per_bar) / 2


    fig, ax = plt.subplots(figsize=(12, 7)) # Adjusted figure size for potentially more bars

    for i, fmt in enumerate(current_formats):
        # positions = x + (i - (num_formats -1) / 2) * width_per_bar # Centering logic
        positions = x + start_offset + i * width_per_bar
        bars = ax.bar(positions, normalized_sizes_np[:, i], width=width_per_bar, label=fmt, color=current_format_colors.get(fmt, '#808080'))

        for bar_idx, bar in enumerate(bars):
            # Ensure we don't try to access out of bounds if a format was missing
            if bar_idx < absolute_sizes_MB_np.shape[0] and i < absolute_sizes_MB_np.shape[1]:
                size_mb = absolute_sizes_MB_np[bar_idx, i]
                height = bar.get_height()
                if size_mb > 0: # Only annotate if there's actual data
                    # Show both absolute size and normalization ratio
                    annotation_text = format_annotation_with_ratio(size_mb, height, "MB")
                    
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        height + 0.03,
                        annotation_text,
                        ha='center',
                        va='bottom',
                        fontsize=8,
                        rotation=90
                    )

    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, label=f'{CSR_BASELINE_KEY} baseline')
    ax.set_xlabel('Dataset')
    ax.set_ylabel(f'Relative Size ({CSR_BASELINE_KEY} = 1.0)')
    ax.set_title(f'Graph Storage Relative to {CSR_BASELINE_KEY}{title_suffix}')
    ax.set_xticks(x)
    ax.set_xticklabels(datasets_list)

    # Adjust y-limit to ensure annotations are visible
    max_normalized_val = np.nanmax(normalized_sizes_np) if normalized_sizes_np.size > 0 else 1
    ax.set_ylim(0, max_normalized_val * 1.5) # Increased multiplier for more space

    # Place legend outside and below the graph, expanding horizontally
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(current_formats) + 1, 
              frameon=True, fancybox=True, shadow=False, fontsize=13)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for the legend below

    # --- Export ---
    base_filename = "graph_size_normalized_annotated"
    plt.savefig(f"{base_filename}{file_suffix}.pdf", bbox_inches='tight')
    print(f"Saved plot: {base_filename}{file_suffix}.pdf")
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    datasets = sorted(list(SPACE_DATA.keys()))

    print("--- Generating plot WITHOUT 'Our' data ---")
    plot_normalized_with_annotation(SPACE_DATA, datasets, include_our_data=False)

    print("\n--- Generating plot WITH 'Our' data ---")
    plot_normalized_with_annotation(SPACE_DATA, datasets, include_our_data=True)