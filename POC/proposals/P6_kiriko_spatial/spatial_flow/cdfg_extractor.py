"""
Control-Data Flow Graph (CDFG) Extractor for Spatial Hardware Synthesis from MLIR Affine.
Extracts computational dataflow nodes, pipeline stages, and memory buffer requirements.
"""

import re
from typing import Dict, Any, List, Tuple


class CDFGExtractor:
    """Extracts spatial hardware dataflow graphs from MLIR Affine text."""

    @staticmethod
    def extract_from_mlir(mlir_text: str) -> Dict[str, Any]:
        """Analyzes arithmetic operations, memory ports, and loop unrolling depth."""
        n_mulf = len(re.findall(r"arith\.mulf", mlir_text))
        n_addf = len(re.findall(r"arith\.addf", mlir_text))
        n_loads = len(re.findall(r"affine\.load|memref\.load", mlir_text))
        n_stores = len(re.findall(r"affine\.store|memref\.store", mlir_text))
        n_loops = len(re.findall(r"affine\.for", mlir_text))

        # Critical path length (stages of dependent operations)
        critical_path_stages = max(2, (n_mulf + n_addf) // max(1, n_stores))

        return {
            "num_multipliers": max(1, n_mulf),
            "num_adders": max(1, n_addf),
            "memory_read_ports": max(1, n_loads),
            "memory_write_ports": max(1, n_stores),
            "loop_nest_depth": n_loops,
            "pipeline_depth_stages": critical_path_stages + 4  # +4 for memory load/store registers
        }
