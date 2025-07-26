# Thesis Plotting Scripts

This directory contains all the plotting scripts for the thesis, organized with shared configurations and data.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate all plots:**
   ```bash
   python plot_all.py
   ```

3. **Find your plots:**
   All plots will be saved to the `/plots` directory as PDF files.

## Generated Plots

The `plot_all.py` script generates the following plots:

### Adjacency List Comparisons
- `adj_size_preliminary.pdf` - Space comparison (CSR, LogGraph, CGraphIndex)
- `adj_size_comparison.pdf` - Space comparison including Our method
- `adj_neighbors_comparison.pdf` - Single-hop neighbor query times
- `adj_2neighbors_comparison.pdf` - Two-hop neighbor query times
- `pareto_neighbors_[dataset].pdf` - Pareto curves for each dataset (neighbors)
- `pareto_2neighbors_[dataset].pdf` - Pareto curves for each dataset (2-neighbors)

### Graph Database Comparisons
- `graphdb_size_comparison.pdf` - Size comparison (Neo4j, ArangoDB, Our, raw files)
- `graphdb_neighbors_comparison.pdf` - Single-hop neighbor query performance
- `graphdb_2neighbors_comparison.pdf` - Two-hop neighbor query performance
- `graphdb_properties_comparison.pdf` - Properties query performance (split chart)

### Memory Analysis
- `graph_db_memory_breakdown.pdf` - Memory breakdown by component

## Individual Scripts

Each plotting script can also be run individually:

- `adj_size_plot.py` - Adjacency list space comparisons
- `adj_time_plot.py` - Adjacency list time comparisons and Pareto curves
- `memory.py` - Memory breakdown visualization
- `gdb_size_comparison.py` - Graph database size comparisons
- `gdb_time_comparison.py` - Graph database time comparisons

## Shared Files

- `config.py` - Font setup, color schemes, and plotting configurations
- `data.py` - All shared datasets and benchmarking data
- `requirements.txt` - Python package dependencies

## Configuration

All plots use:
- **Font:** TeX Gyre Termes (mathpazo equivalent)
- **Colors:** Consistent color scheme across all plots
- **Format:** PDF output only
- **Normalization:** Ratios shown for normalized data (e.g., "1.2x")

## Customization

To modify colors, fonts, or other settings, edit `config.py`.
To update data, edit `data.py`. 