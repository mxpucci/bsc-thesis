#!/usr/bin/env python3
"""
Comprehensive plotting script that generates all required plots for the thesis.
This script creates a /plots directory and generates all visualizations.
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import all plotting modules
from adj_space_plot import plot_normalized_with_annotation
from adj_time_plot import plot_time_comparison_normalized, plot_combined_neighbors_comparison
from pareto_frontier import plot_pareto_for_datasets
from gdb_space_comparison import plot_storage_normalized
from gdb_time_comparison import plot_comparison, plot_properties_comparison, plot_combined_gdb_neighbors_comparison
from relabelling import plot_data_normalized_with_annotation
from config import setup_matplotlib_fonts
from data import (
    SPACE_DATA, TIME_NEIGHBORS_SINGLE_HOP, TIME_NEIGHBORS_TWO_HOP,
    GDB_SPACE_DATA,
    GDB_TIME_NEIGHBORS_SINGLE, GDB_TIME_NEIGHBORS_TWO,
    GDB_TIME_FIXEDSIZE_PROPS, GDB_TIME_VARSIZE_PROPS,
    RELABEL_DATA
)

def create_plots_directory():
    """Create the plots directory if it doesn't exist."""
    plots_dir = Path(__file__).parent.parent / "plots"
    plots_dir.mkdir(exist_ok=True)
    return plots_dir

def generate_all_plots():
    """Generate all required plots and save them to the plots directory."""
    
    # Setup matplotlib fonts globally
    setup_matplotlib_fonts()
    
    # Create plots directory
    plots_dir = create_plots_directory()
    
    # Change to plots directory for saving files
    original_cwd = os.getcwd()
    os.chdir(plots_dir)
    
    try:
        print("🎨 Generating all plots...")
        
        # 1. Adjacency list space comparisons
        print("📊 Generating adjacency space plots...")
        datasets = sorted(list(SPACE_DATA.keys()))  # Alphabetical order
        plot_normalized_with_annotation(SPACE_DATA, datasets, include_our_data=False)
        # Rename the generated file to match expected name
        if os.path.exists("graph_size_normalized_annotated_without_our.pdf"):
            os.rename("graph_size_normalized_annotated_without_our.pdf", "adj_size_preliminary.pdf")
        
        plot_normalized_with_annotation(SPACE_DATA, datasets, include_our_data=True)
        # Rename the generated file to match expected name
        if os.path.exists("graph_size_normalized_annotated_with_our.pdf"):
            os.rename("graph_size_normalized_annotated_with_our.pdf", "adj_size_comparison.pdf")
        
        # 2. Memory breakdown
        print("🧠 Generating memory breakdown plot...")
        # Load memory data and generate plot
        import json
        memory_json_path = script_dir / "memory-breakdown.json"
        if memory_json_path.exists():
            from memory import load_memory_stats, plot_memory_breakdown_stacked
            memory_data = load_memory_stats(str(memory_json_path))
            plot_memory_breakdown_stacked(memory_data, ".")
            # Rename to expected filename
            if os.path.exists("memory_breakdown_stacked.pdf"):
                os.rename("memory_breakdown_stacked.pdf", "graph_db_memory_breakdown.pdf")
        
        # 3. Adjacency list time comparisons
        print("⏱️  Generating adjacency time plots...")
        # Generate individual plots
        plot_time_comparison_normalized(TIME_NEIGHBORS_SINGLE_HOP, 
                                      "Single-hop Neighbor Query Performance", 
                                      "adj_neighbors_comparison")
        plot_time_comparison_normalized(TIME_NEIGHBORS_TWO_HOP, 
                                      "Two-hop Neighbor Query Performance", 
                                      "adj_2neighbors_comparison")
        
        # Generate combined plot
        plot_combined_neighbors_comparison(TIME_NEIGHBORS_SINGLE_HOP, TIME_NEIGHBORS_TWO_HOP,
                                         "Combined Neighbor Query Performance", 
                                         "adj_combined_neighbors_comparison")
        
        # 4. Pareto curves for each dataset
        print("📈 Generating Pareto curves...")
        time_data_map = {
            'neighbors': TIME_NEIGHBORS_SINGLE_HOP,
            '2neighbors': TIME_NEIGHBORS_TWO_HOP
        }
        plot_pareto_for_datasets(SPACE_DATA, time_data_map, ".")
        
        # 5. Graph database size comparison
        print("💾 Generating graph database size comparison...")
        plot_storage_normalized(GDB_SPACE_DATA, normalize_by='unzipped')
        # Rename to expected filename
        if os.path.exists("graphdb_storage_normalized_by_unzipped.pdf"):
            os.rename("graphdb_storage_normalized_by_unzipped.pdf", "graphdb_size_comparison.pdf")
        
        # 6. Graph database time comparisons
        print("🏃 Generating graph database time plots...")
        # Generate combined plot (replaces individual single/two-hop plots)
        plot_combined_gdb_neighbors_comparison(GDB_TIME_NEIGHBORS_SINGLE, GDB_TIME_NEIGHBORS_TWO,
                                             "Graph Database Neighbor Query Performance", 
                                             "graphdb_neighbors_comparison")
        
        # 7. Graph database properties comparison (split chart)
        print("🔧 Generating graph database properties comparison...")
        plot_properties_comparison(GDB_TIME_FIXEDSIZE_PROPS, GDB_TIME_VARSIZE_PROPS, 
                                 "Graph Database Properties Query Performance", 
                                 "graphdb_properties_comparison")
        
        # 8. Relabelling comparison
        print("🏷️  Generating relabelling comparison...")
        from config import TECHNIQUE_COLORS
        datasets_order = sorted(list(RELABEL_DATA.keys()))
        items_order = ['CSV', 'random', 'topsort', 'BFS', 'CM', 'DM']
        item_colors_map = {item: TECHNIQUE_COLORS[item] for item in items_order}
        plot_data_normalized_with_annotation(RELABEL_DATA, datasets_order, items_order, 
                                           item_colors_map, 'CSV', 
                                           "Relabelling Techniques Comparison", 
                                           "CSV")
        # Rename to expected filename
        if os.path.exists("relabelled_graph_size_normalized_annotated.pdf"):
            os.rename("relabelled_graph_size_normalized_annotated.pdf", "relabelling.pdf")
        
        print("✅ All plots generated successfully!")
        print(f"📁 Plots saved to: {plots_dir.absolute()}")
        
        # List all generated files
        print("\n📋 Generated files:")
        pdf_files = sorted(plots_dir.glob("*.pdf"))
        for pdf_file in pdf_files:
            print(f"   - {pdf_file.name}")
            
        if not pdf_files:
            print("   ⚠️  No PDF files found!")
        
    except Exception as e:
        print(f"❌ Error generating plots: {e}")
        raise
    finally:
        # Return to original directory
        os.chdir(original_cwd)

def verify_all_expected_plots():
    """Verify that all expected plots were generated."""
    plots_dir = Path(__file__).parent.parent / "plots"
    expected_files = [
        "adj_size_preliminary.pdf",
        "adj_size_comparison.pdf", 
        "graph_db_memory_breakdown.pdf",
        "adj_neighbors_comparison.pdf",
        "adj_2neighbors_comparison.pdf",
        "adj_combined_neighbors_comparison.pdf",
        "graphdb_size_comparison.pdf",
        "graphdb_neighbors_comparison.pdf",
        "graphdb_properties_comparison.pdf",
        "relabelling.pdf"
    ]
    
    # Add Pareto curve files for each dataset
    datasets = sorted(list(TIME_NEIGHBORS_SINGLE_HOP.keys()))
    for dataset in datasets:
        expected_files.append(f"neighbors/{dataset}.pdf")
        expected_files.append(f"2neighbors/{dataset}.pdf")
    
    missing_files = []
    for expected_file in expected_files:
        if not (plots_dir / expected_file).exists():
            missing_files.append(expected_file)
    
    if missing_files:
        print(f"\n⚠️  Missing expected files:")
        for missing_file in missing_files:
            print(f"   - {missing_file}")
    else:
        print(f"\n✅ All {len(expected_files)} expected files generated successfully!")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    print("🚀 Starting comprehensive plot generation...")
    print("=" * 60)
    
    try:
        generate_all_plots()
        verify_all_expected_plots()
        print("\n🎉 Plot generation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⛔ Plot generation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1) 