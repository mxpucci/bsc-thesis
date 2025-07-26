import matplotlib.pyplot as plt
import numpy as np
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS, to_MB, format_annotation_with_ratio
from data import RELABEL_DATA

# Setup fonts
setup_matplotlib_fonts()

# --- Constants for Plot Configuration ---
# Master list of all techniques in their desired default order for plotting
MASTER_TECHNIQUES_ORDER = ['CSV', 'random', 'topsort', 'BFS', 'CM', 'DM']

# Colors for all defined techniques (now using shared config)
ALL_TECHNIQUE_COLORS = {
    'CSV': TECHNIQUE_COLORS['CSV'],
    'random': TECHNIQUE_COLORS['random'],
    'topsort': TECHNIQUE_COLORS['topsort'],
    'BFS': TECHNIQUE_COLORS['BFS'],
    'CM': TECHNIQUE_COLORS['CM'],
    'DM': TECHNIQUE_COLORS['DM']
}

# Define the baseline technique, which will be used for normalization (CSR = 1.0 style)
BASELINE_TECHNIQUE_NAME = 'CSV'
if BASELINE_TECHNIQUE_NAME not in MASTER_TECHNIQUES_ORDER:
    raise ValueError(f"Baseline technique '{BASELINE_TECHNIQUE_NAME}' must be in MASTER_TECHNIQUES_ORDER.")
if BASELINE_TECHNIQUE_NAME not in ALL_TECHNIQUE_COLORS:
    raise ValueError(f"Baseline technique '{BASELINE_TECHNIQUE_NAME}' must have a color defined in ALL_TECHNIQUE_COLORS.")

# --- User Configuration: Select techniques to plot ---
# Set to a list of technique names from MASTER_TECHNIQUES_ORDER.
# Example: CHOSEN_TECHNIQUES_TO_PLOT = ['CSV', 'BFS', 'CM']
# Set to None to plot all techniques defined in MASTER_TECHNIQUES_ORDER.
# The baseline technique (BASELINE_TECHNIQUE_NAME) will always be included in the plot.
CHOSEN_TECHNIQUES_TO_PLOT = ['CSV', 'topsort', 'CM', 'BFS', 'random', 'DM']
# CHOSEN_TECHNIQUES_TO_PLOT = None # Uncomment to plot all techniques
# CHOSEN_TECHNIQUES_TO_PLOT = ['random', 'BFS'] # Example where baseline might not be initially chosen by user
# --- End User Configuration ---

# Determine the actual techniques to plot based on user's choice
if CHOSEN_TECHNIQUES_TO_PLOT is None:
    # Plot all techniques from the master list
    techniques_for_plot_final = MASTER_TECHNIQUES_ORDER[:]
else:
    # Start with user's chosen techniques, ensuring they are valid (exist in MASTER_TECHNIQUES_ORDER)
    selected_techniques_set = {tech for tech in CHOSEN_TECHNIQUES_TO_PLOT if tech in MASTER_TECHNIQUES_ORDER}

    # Ensure the baseline technique is always included
    selected_techniques_set.add(BASELINE_TECHNIQUE_NAME)

    # Order the final list of techniques according to MASTER_TECHNIQUES_ORDER
    techniques_for_plot_final = [tech for tech in MASTER_TECHNIQUES_ORDER if tech in selected_techniques_set]

# Filter the color map to include only the selected techniques
active_technique_colors_final = {
    tech: ALL_TECHNIQUE_COLORS[tech]
    for tech in techniques_for_plot_final
    if tech in ALL_TECHNIQUE_COLORS
}

# Datasets to plot (derived from data keys, can be made configurable if needed)
datasets_to_plot = sorted(list(RELABEL_DATA.keys()))

# Modified plotting function (the function itself doesn't need changes for this feature)
def plot_data_normalized_with_annotation(data_dict, datasets_order, items_order, item_colors_map,
                                         baseline_item_name, plot_title, y_label_base):
    normalized_values = []
    absolute_sizes_MB = []

    for ds_name in datasets_order:
        if baseline_item_name not in data_dict[ds_name]:
            raise ValueError(f"Baseline item '{baseline_item_name}' not found in dataset '{ds_name}'.")

        baseline_val = data_dict[ds_name][baseline_item_name]
        if baseline_val == 0:
            print(f"Warning: Baseline value for '{baseline_item_name}' in dataset '{ds_name}' is 0. Normalization will result in NaNs or Infs.")
            # Assign NaN to prevent division by zero errors and allow plotting of other data
            baseline_val = np.nan

        current_ds_item_sizes_bytes = []
        for item_name in items_order:
            if item_name not in data_dict[ds_name]:
                raise ValueError(f"Item '{item_name}' not found in dataset '{ds_name}'. Ensure all datasets have all items for selected techniques.")
            current_ds_item_sizes_bytes.append(data_dict[ds_name][item_name])

        # Handle potential division by zero/NaN gracefully if baseline_val is NaN
        with np.errstate(divide='ignore', invalid='ignore'):
            normalized_values.append([s / baseline_val for s in current_ds_item_sizes_bytes])
        absolute_sizes_MB.append([to_MB(s) for s in current_ds_item_sizes_bytes])

    normalized_np = np.array(normalized_values)
    abs_MB_np = np.array(absolute_sizes_MB)

    x_positions = np.arange(len(datasets_order))

    num_items_per_group = len(items_order)
    if num_items_per_group == 0:
        print("No items to plot. Aborting plot generation.")
        return

    group_total_width_on_axis = 0.8
    individual_bar_width = group_total_width_on_axis / num_items_per_group

    fig, ax = plt.subplots(figsize=(14, 7.5))

    for i, item_name in enumerate(items_order):
        bar_center_offsets = (i - (num_items_per_group - 1) / 2.0) * individual_bar_width
        current_item_bar_positions = x_positions + bar_center_offsets

        bars = ax.bar(current_item_bar_positions, normalized_np[:, i],
                      width=individual_bar_width, label=item_name, color=item_colors_map.get(item_name, '#808080')) # Default to gray if color missing

        for bar, size_mb in zip(bars, abs_MB_np[:, i]):
            height = bar.get_height()
            if np.isnan(height): continue
            # Show both absolute size and normalization ratio
            annotation_text = format_annotation_with_ratio(size_mb, height, "MB")
            
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.03,
                annotation_text,
                ha='center',
                va='bottom',
                fontsize=7,
                rotation=90
            )

    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, label=f'{baseline_item_name} baseline (1.0)')
    ax.set_xlabel('Dataset', fontsize=12)
    ax.set_ylabel(f'Relative Size ({y_label_base} = 1.0)', fontsize=12)
    ax.set_title(plot_title, fontsize=14, pad=20 + (num_items_per_group > 3) * 20 )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(datasets_order, fontsize=10)
    ax.tick_params(axis='y', labelsize=10)

    max_normalized_val = 0
    # Calculate max ignoring NaNs
    if normalized_np[~np.isnan(normalized_np)].size > 0 :
        max_normalized_val = np.max(normalized_np[~np.isnan(normalized_np)])

    effective_max_y_for_ylim = max_normalized_val + 0.15
    y_upper_limit = max(1.25, effective_max_y_for_ylim * 1.2)
    ax.set_ylim(0, y_upper_limit)

    # Place legend outside and below the graph, expanding horizontally
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), 
              ncol=min(6, num_items_per_group), frameon=True, fancybox=True, shadow=False, fontsize=13)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for the legend below

    plt.savefig("relabelled_graph_size_normalized_annotated.pdf", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_title = f'Storage Size of Relabelling Techniques Relative to "{BASELINE_TECHNIQUE_NAME.capitalize()}"'
    y_label_base_text = BASELINE_TECHNIQUE_NAME

    if not techniques_for_plot_final:
        print("Warning: No techniques selected or valid for plotting. Please check MASTER_TECHNIQUES_ORDER and CHOSEN_TECHNIQUES_TO_PLOT.")
    else:
        plot_data_normalized_with_annotation(
            RELABEL_DATA,
            datasets_to_plot,
            techniques_for_plot_final, # Use the dynamically determined list
            active_technique_colors_final, # Use the filtered colors
            BASELINE_TECHNIQUE_NAME,
            plot_title,
            y_label_base_text
        )