import matplotlib.pyplot as plt
import numpy as np
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS, INPUT_FILE_STYLES, to_MB, format_annotation_with_ratio
from data import GDB_SPACE_DATA

# Setup fonts
setup_matplotlib_fonts()

datasets = sorted(list(GDB_SPACE_DATA.keys()))
formats = ['Our', 'Neo4j', 'ArangoDB'] # Database formats
format_colors = {
    'Our': TECHNIQUE_COLORS['Our'],
    'Neo4j': TECHNIQUE_COLORS['Neo4j'],
    'ArangoDB': TECHNIQUE_COLORS['ArangoDB']
}

def plot_storage_normalized(data, normalize_by='unzipped'):
    assert normalize_by in ('zipped', 'unzipped'), "normalize_by must be 'zipped' or 'unzipped'"

    plot_elements = []
    max_normalized_value = 0

    # Prepare data for database formats
    db_formats_prepared_data = []
    for fmt in formats:
        norm_vals = []
        abs_vals_mb = []
        for ds_name in datasets:
            ds_data = data[ds_name]
            val = ds_data[fmt]
            base_val = ds_data[normalize_by]

            if val == 0 or base_val == 0: # Handle zero values to avoid division by zero or meaningless ratios
                norm_vals.append(np.nan)
                abs_vals_mb.append(np.nan)
            else:
                norm_vals.append(val / base_val)
                abs_vals_mb.append(to_MB(val))

        db_formats_prepared_data.append({
            'label': fmt,
            'normalized_values': np.array(norm_vals),
            'absolute_MB_values': np.array(abs_vals_mb),
            'color': format_colors[fmt],
            'hatch': None
        })
        if len(norm_vals) > 0:
            current_max = np.nanmax(norm_vals) if not all(np.isnan(norm_vals)) else 0
            if current_max > max_normalized_value:
                max_normalized_value = current_max


    if normalize_by == 'zipped':
        # Add "Uncompressed Input" as the first element to plot
        uncomp_norm_vals = []
        uncomp_abs_vals_mb = []
        for ds_name in datasets:
            ds_data = data[ds_name]
            val = ds_data['unzipped']
            base_val = ds_data['zipped']
            if base_val == 0:
                uncomp_norm_vals.append(np.nan)
            else:
                uncomp_norm_vals.append(val / base_val)
            uncomp_abs_vals_mb.append(to_MB(val))

        plot_elements.append({
            'label': 'Uncompressed Input',
            'normalized_values': np.array(uncomp_norm_vals),
            'absolute_MB_values': np.array(uncomp_abs_vals_mb),
            **INPUT_FILE_STYLES['Uncompressed Input']
        })
        if len(uncomp_norm_vals) > 0:
            current_max = np.nanmax(uncomp_norm_vals) if not all(np.isnan(uncomp_norm_vals)) else 0
            if current_max > max_normalized_value:
                max_normalized_value = current_max

        plot_elements.extend(db_formats_prepared_data)
        plot_title = 'Graph DB Storage Normalized to Zipped Input Size'
        y_axis_label = 'Relative Size (Zipped Input = 1.0)'
        baseline_label = 'Zipped Input (baseline)'

    elif normalize_by == 'unzipped':
        # Add "Zipped Input" as the first element to plot
        zip_norm_vals = []
        zip_abs_vals_mb = []
        for ds_name in datasets:
            ds_data = data[ds_name]
            val = ds_data['zipped']
            base_val = ds_data['unzipped']
            if base_val == 0:
                zip_norm_vals.append(np.nan)
            else:
                zip_norm_vals.append(val / base_val)
            zip_abs_vals_mb.append(to_MB(val))

        plot_elements.append({
            'label': 'Zipped Input',
            'normalized_values': np.array(zip_norm_vals),
            'absolute_MB_values': np.array(zip_abs_vals_mb),
            **INPUT_FILE_STYLES['Zipped Input']
        })
        if len(zip_norm_vals) > 0:
            current_max = np.nanmax(zip_norm_vals) if not all(np.isnan(zip_norm_vals)) else 0
            if current_max > max_normalized_value:
                max_normalized_value = current_max

        plot_elements.extend(db_formats_prepared_data)
        plot_title = 'Graph DB Storage Normalized to Original Dataset Size'
        y_axis_label = 'Relative Size (Original Dataset = 1.0)'
        baseline_label = 'Original Dataset (baseline)'

    # Plotting
    x = np.arange(len(datasets))
    n_bars_per_group = len(plot_elements)
    width = 0.8 / n_bars_per_group # Adjust bar width based on number of bars

    fig, ax = plt.subplots(figsize=(12, 7)) # Slightly wider for more bars

    for i, element in enumerate(plot_elements):
        offset = (i - (n_bars_per_group - 1) / 2.0) * width
        positions = x + offset
        bars = ax.bar(
            positions,
            element['normalized_values'],
            width=width * 0.9, # Small gap between bars in a group
            label=element['label'],
            color=element['color'],
            hatch=element['hatch'],
            edgecolor='black' if element['hatch'] else None # Add edgecolor for hatched bars
        )

        # Annotate with MB sizes and normalization ratios
        for bar_idx, bar in enumerate(bars):
            abs_size = element['absolute_MB_values'][bar_idx]
            norm_ratio = element['normalized_values'][bar_idx]
            if not np.isnan(abs_size) and norm_ratio > 0:  # Only annotate non-zero values
                height = bar.get_height()
                if not np.isnan(height) and height > 0: # Only annotate if height is not NaN and > 0
                    annotation_text = format_annotation_with_ratio(abs_size, norm_ratio, "MB")
                    if annotation_text:  # Only add if annotation is not empty
                        ax.text(
                            bar.get_x() + bar.get_width() / 2,
                            height + 0.05 * max_normalized_value, # Dynamic offset for text
                            annotation_text,
                            ha='center',
                            va='bottom',
                            fontsize=7, # Standardized font size
                            rotation=90
                        )

    # Baseline at 1.0
    ax.axhline(y=1.0, color='dimgray', linestyle='--', linewidth=1.2, label=baseline_label)

    ax.set_xlabel('Dataset')
    ax.set_ylabel(y_axis_label)
    ax.set_title(plot_title, fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=0, ha='center') # Horizontal labels for datasets

    # Adjust Y limit to ensure visibility of annotations and baseline
    ax.set_ylim(0, max_normalized_value * 1.3 if max_normalized_value > 0 else 1.5)

    # Place legend outside and below the plot, expanding horizontally
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=min(4, len(plot_elements) + 1), 
              frameon=True, fancybox=True, shadow=False, fontsize=13, title="Storage Type")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for the legend below

    suffix = normalize_by
    plt.savefig(f"graphdb_storage_normalized_by_{suffix}.pdf", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_storage_normalized(GDB_SPACE_DATA, normalize_by='unzipped')