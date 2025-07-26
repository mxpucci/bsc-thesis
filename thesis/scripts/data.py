"""
Shared data used across multiple plotting scripts.
Contains datasets for space usage, time measurements, and other experimental data.
"""

# Space usage data (used in adj_space_plot.py and pareto_frontier.py)
SPACE_DATA = {
    'prime': {
        'CSR': 17473954,
        'LogGraph': 9924656,
        'CGraphIndex': 15733715,
        'Our': 10057280,
    },
    'dblp': {
        'CSR': 228825326,
        'LogGraph': 225081476,
        'CGraphIndex': 431141622,
        'Our': 164349996,
    },
    'mag': {
        'CSR': 107695702,
        'LogGraph': 80142194,
        'CGraphIndex': 112866678,
        'Our': 83332724,
    },
    'patents': {
        'CSR': 150278772,
        'LogGraph': 144335227,
        'CGraphIndex': 180056813,
        'Our': 130629362,
    },
    'amazon': {
        'CSR': 21035422,
        'LogGraph': 17773226,
        'CGraphIndex': 29950426,
        'Our': 14362964,
    }
}

# Single-hop neighbor query times (used in adj_time_plot.py and pareto_frontier.py)
TIME_NEIGHBORS_SINGLE_HOP = {
    'prime': {
        'CSR': 6.281,
        'LogGraph': 17.099,
        'CGraphIndex': 5.981,
        'Our': 12.049,
    },
    'dblp': {
        'CSR': 147.752,
        'LogGraph': 602.897,
        'CGraphIndex': 6.335,
        'Our': 259.453,
    },
    'mag': {
        'CSR': 33.087,
        'LogGraph': 82.871,
        'CGraphIndex': 23.239,
        'Our': 52.554,
    },
    'patents': {
        'CSR': 35.426,
        'LogGraph': 121.755,
        'CGraphIndex': 3.771,
        'Our': 88.395,
    },
    'amazon': {
        'CSR': 42.191,
        'LogGraph': 270.697,
        'CGraphIndex': 38.077,
        'Our': 56.458,
    }
}

# Two-hop neighbor query times (used in adj_time_plot.py and pareto_frontier.py)
TIME_NEIGHBORS_TWO_HOP = {
    'prime': {
        'CSR': 2.327,
        'LogGraph': 2.400,
        'CGraphIndex': 3.796,
        'Our': 8.233,
    },
    'dblp': {
        'CSR': 396.352,
        'LogGraph': 11.440,
        'CGraphIndex': 6.759,
        'Our': 490.184,
    },
    'mag': {
        'CSR': 16.930,
        'LogGraph': 2.200,
        'CGraphIndex': 12.621,
        'Our': 30.391,
    },
    'patents': {
        'CSR': 34.353,
        'LogGraph': 8.610,
        'CGraphIndex': 4.45527,
        'Our': 54.404,
    },
    'amazon': {
        'CSR': 8.829,
        'LogGraph': 2.398,
        'CGraphIndex': 6.626,
        'Our': 15.788,
    }
}

# Graph database comparison data (used in gdb_time_comparison.py)
GDB_TIME_NEIGHBORS_SINGLE = {
    'prime': {
        'Neo4j': 10582.535,
        'Our': 12.049,
    },
    'dblp': {
        'Neo4j': 1332.026,
        'Our': 259.453,
    },
    'mag': {
        'Neo4j': 3046.213,
        'Our': 52.554,
    },
    'patents': {
        'Neo4j': 2696.320,
        'Our': 88.395,
    },
    'amazon': {
        'Neo4j': 2422.875,
        'Our': 56.458,
    }
}

GDB_TIME_NEIGHBORS_TWO = {
    'prime': {
        'Neo4j': 616453.587,
        'Our': 8.233,
    },
    'dblp': {
        'Neo4j': 2541.058,
        'Our': 490.184,
    },
    'mag': {
        'Neo4j': 4541.722,
        'Our': 30.391,
    },
    'patents': {
        'Neo4j': 14689.665,
        'Our': 54.404,
    },
    'amazon': {
        'Neo4j': 13777.436,
        'Our': 15.788,
    }
}

GDB_TIME_FIXEDSIZE_PROPS = {
    'prime': {
        'Neo4j': 4504.673,
        'Our': 186.302,
    },
    'dblp': {
        'Neo4j': 5511.505,
        'Our': 415.153,
    },
    'mag': {
        'Neo4j': 5214.581,
        'Our': 364.545,
    },
    'patents': {
        'Neo4j': 6040.178,
        'Our': 322.145,
    },
    'amazon': {
        'Neo4j': 4618.831,
        'Our': 360.545,
    }
}

GDB_TIME_VARSIZE_PROPS = {
    'prime': {
        'Neo4j': 0,
        'Our': 0,
    },
    'dblp': {
        'Neo4j': 12369.007,
        'Our': 4936170.225,
    },
    'mag': {
        'Neo4j': 10847.752,
        'Our': 5251040.767,
    },
    'patents': {
        'Neo4j': 11280.983,
        'Our': 3277537.579,
    },
    'amazon': {
        'Neo4j': 8149.593,
        'Our': 4248512.699,
    }
}

# Graph database space comparison data (used in gdb_space_comparison.py)
GDB_SPACE_DATA = {
    'prime': {
        'Our': 13725696,
        'Neo4j': 327155712,
        'ArangoDB': 597724981,
        'zipped': 29644676,
        'unzipped': 260029594
    },
    'dblp': {
        'Our': 591323136,
        'Neo4j': 4617089843,
        'ArangoDB': 5595838451,
        'zipped': 946959092,
        'unzipped': 3461480607
    },
    'mag': {
        'Our': 28874752,
        'Neo4j': 2061123584,
        'ArangoDB': 2087764522,
        'zipped': 407781263,
        'unzipped': 1799829557
    },
    'patents': {
        'Our': 201961472,
        'Neo4j': 2040109465,
        'ArangoDB': 2840802617,
        'zipped': 245210043,
        'unzipped': 1304864323
    },
    'amazon': {
        'Our': 186363904,
        'Neo4j': 1395864371,
        'ArangoDB': 756251906,
        'zipped': 218967442,
        'unzipped': 795215172
    }
}

# Relabeling technique data (used in relabelling.py)
RELABEL_DATA = {
    'prime': {
        'CSV': 11858144,
        'random': 13723984,
        'topsort': 9674928,
        'BFS': 10186344,
        'CM': 10057280,
        'DM': 9865320
    },
    'dblp': {
        'CSV': 218427364,
        'random': 223423772,
        'topsort': 162679972,
        'BFS': 164785396,
        'CM': 164349996,
        'DM': 198937796
    },
    'patents': {
        'CSV': 145541474,
        'random': 146298938,
        'topsort': 136975290,
        'BFS': 130156730,
        'CM': 130629362,
        'DM': 140558682
    },
    'mag': {
        'CSV': 95939756,
        'random': 97043980,
        'topsort': 87752244,
        'BFS': 87470956,
        'CM': 83332724,
        'DM': 83504356
    },
    'amazon': {
        'CSV': 18847540,
        'random': 19234092,
        'topsort': 16985468,
        'BFS': 14389860,
        'CM': 14362964,
        'DM': 16053916
    }
}