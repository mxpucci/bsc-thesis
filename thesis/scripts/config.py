"""
Configuration file for consistent plotting across all scripts.
Contains colors, fonts, and other shared plotting parameters.
"""

from matplotlib import rcParams

# Font configuration - mathpazo for all plots
def setup_matplotlib_fonts():
    """Setup matplotlib to use mathpazo font consistently."""
    rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "text.latex.preamble": r"\usepackage{mathpazo}"  # Palatino via mathpazo
    })

# Standardized color scheme for techniques/databases
TECHNIQUE_COLORS = {
    # Core techniques
    'Our': '#d62728',           # Red (standardized across all scripts)
    'CSR': '#1f77b4',           # Blue
    'LogGraph': '#ff7f0e',      # Orange
    'CGraphIndex': '#2ca02c',   # Green
    
    # Graph databases
    'Neo4j': '#1f77b4',         # Blue
    'ArangoDB': '#ff7f0e',      # Orange
    
    # Relabeling techniques
    'CSV': '#1f77b4',           # Blue (baseline)
    'random': '#ff7f0e',        # Orange
    'topsort': '#2ca02c',       # Green
    'BFS': '#d62728',           # Red
    'CM': '#9467bd',            # Purple
    'DM': '#8c564b',            # Brown
}

# Input file styles for gdb_space_comparison
INPUT_FILE_STYLES = {
    'Zipped Input': {'color': 'dimgray', 'hatch': '//'},
    'Uncompressed Input': {'color': 'silver', 'hatch': '..'}
}

# Common constants
OUR_DATA_KEY = 'Our'
CSR_BASELINE_KEY = 'CSR'
NEO4J_KEY = 'Neo4j'
LOGGRAPH_KEY = 'LogGraph'
CGRAPHINDEX_KEY = 'CGraphIndex'
ARANGODB_KEY = 'ArangoDB'

# Common plotting parameters
DEFAULT_FIGURE_SIZE = (12, 7)
DEFAULT_BAR_WIDTH = 0.8
DEFAULT_FONT_SIZE_ANNOTATION = 7
DEFAULT_FONT_SIZE_LABEL = 8
DEFAULT_FONT_SIZE_TITLE = 14

# Helper functions
def to_MB(byte_val):
    """Convert bytes to megabytes."""
    return byte_val / (1024 * 1024)

def format_annotation_with_ratio(absolute_value, normalized_value, unit="MB", show_ratio=True):
    """
    Format annotation text with only the normalization ratio.
    
    Args:
        absolute_value: The absolute value (not used anymore)
        normalized_value: The normalized value (ratio)
        unit: Unit for the absolute value (not used anymore)
        show_ratio: Whether to show the ratio (e.g., "2.1x")
    
    Returns:
        Formatted string for annotation (only ratio)
    """
    if show_ratio and normalized_value != 1.0:
        return f'{normalized_value:.1f}x'
    else:
        return '' 