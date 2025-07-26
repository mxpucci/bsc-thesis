import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from config import setup_matplotlib_fonts, TECHNIQUE_COLORS, OUR_DATA_KEY, CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY, to_MB
from data import SPACE_DATA, TIME_NEIGHBORS_SINGLE_HOP, TIME_NEIGHBORS_TWO_HOP

# Setup fonts
setup_matplotlib_fonts()

def pareto_frontier(points):
    """
    Computes the Pareto frontier for a set of points.
    A point is on the Pareto frontier if it is not dominated by any other point.
    """
    sorted_points = sorted(points, key=lambda p: (p[0], p[1]))
    pareto_front = []
    min_y = float('inf')
    for x, y in sorted_points:
        if y < min_y:
            pareto_front.append((x, y))
            min_y = y
    return pareto_front

def plot_pareto_for_datasets(space_data, time_data_map, base_path="plots/pareto"):
    """
    Generates and saves Pareto frontier plots for each dataset and query type.
    """
    representations = [CSR_BASELINE_KEY, LOGGRAPH_KEY, CGRAPHINDEX_KEY, OUR_DATA_KEY]
    colors = {
        CSR_BASELINE_KEY: TECHNIQUE_COLORS['CSR'],
        LOGGRAPH_KEY: TECHNIQUE_COLORS['LogGraph'],
        CGRAPHINDEX_KEY: TECHNIQUE_COLORS['CGraphIndex'],
        OUR_DATA_KEY: TECHNIQUE_COLORS['Our']
    }
    markers = {
        CSR_BASELINE_KEY: 'o', LOGGRAPH_KEY: 's', CGRAPHINDEX_KEY: '^', OUR_DATA_KEY: 'D'
    }

    for query_type, time_data in time_data_map.items():
        output_dir = f"{base_path}/{query_type}"
        os.makedirs(output_dir, exist_ok=True)
        
        for dataset in space_data.keys():
            fig, ax = plt.subplots(figsize=(8, 6))
            
            points_for_pareto = []
            
            for rep in representations:
                if dataset in space_data and rep in space_data[dataset] and \
                   dataset in time_data and rep in time_data[dataset]:
                    
                    space_mb = to_MB(space_data[dataset][rep])
                    time_ns = time_data[dataset][rep]
                    
                    points_for_pareto.append((space_mb, time_ns))
                    
                    ax.plot(space_mb, time_ns, marker=markers[rep], color=colors[rep], 
                            linestyle='None', markersize=10, label=rep)

            # Calculate and plot Pareto frontier
            if len(points_for_pareto) > 1:
                frontier = pareto_frontier(points_for_pareto)
                if len(frontier) > 1:
                    frontier.sort()
                    x_pareto, y_pareto = zip(*frontier)
                    ax.plot(x_pareto, y_pareto, color='black', linestyle='-', marker='', zorder=1)

            # Format query type for better display
            query_display = {
                'single_hop': '1-hop neighbors',
                'two_hop': '2-hop neighbors'
            }.get(query_type, query_type.replace("_", " "))
            
            ax.set_title(f'Pareto Frontier for {dataset} ({query_display})')
            ax.set_xlabel('Space (MB)')
            ax.set_ylabel('Time per Query (ns)')
            ax.grid(True, which='both', linestyle='--', linewidth=0.5)
            
            # Create legend
            legend_elements = [
                Line2D([0], [0], marker=markers[rep], color=colors[rep], label=rep,
                       linestyle='None', markersize=10) for rep in representations
            ]
            # Place legend outside and below the graph, expanding horizontally
            ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1), 
                      ncol=len(representations), frameon=True, fancybox=True, shadow=False, 
                      fontsize=13, title="Representations")

            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)  # Make room for the legend below
            plot_filename = f"{output_dir}/{dataset}.pdf"
            plt.savefig(plot_filename, bbox_inches='tight')
            print(f"Saved plot: {plot_filename}")
            plt.close(fig)

if __name__ == "__main__":
    time_data_map = {
        'single_hop': TIME_NEIGHBORS_SINGLE_HOP,
        'two_hop': TIME_NEIGHBORS_TWO_HOP
    }
    plot_pareto_for_datasets(SPACE_DATA, time_data_map) 