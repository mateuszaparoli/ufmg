"""
Search Space definition for MLIR Affine Dialect Autotuning.
Defines parameters for multi-level tiling, unrolling, vectorization,
and affine pass permutations.
"""

import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


@dataclass
class AffineTuningConfig:
    """Represents a concrete point in the compiler optimization search space."""
    tile_size_l1: int = 32
    tile_size_l2: int = 64
    tile_size_k: int = 16
    unroll_factor: int = 4
    enable_fusion: bool = True
    enable_scalrep: bool = True
    enable_coalescing: bool = True
    enable_super_vectorize: bool = True
    vector_width: int = 256  # 128, 256 (AVX2), 512 (AVX-512)
    pass_order: List[str] = field(default_factory=lambda: [
        "canonicalize", "cse", "mem2reg", "tile", "fusion", "unroll", "scalrep", "vectorize"
    ])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tile_size_l1": self.tile_size_l1,
            "tile_size_l2": self.tile_size_l2,
            "tile_size_k": self.tile_size_k,
            "unroll_factor": self.unroll_factor,
            "enable_fusion": self.enable_fusion,
            "enable_scalrep": self.enable_scalrep,
            "enable_coalescing": self.enable_coalescing,
            "enable_super_vectorize": self.enable_super_vectorize,
            "vector_width": self.vector_width,
            "pass_order": self.pass_order,
        }

    def generate_mlir_opt_flags(self) -> List[str]:
        """Translates the configuration into concrete mlir-opt command line arguments."""
        flags = []
        pass_mapping = {
            "canonicalize": ["-canonicalize"],
            "cse": ["-cse"],
            "mem2reg": ["-mem2reg"],
            "tile": [f"-affine-loop-tile=tile-size={self.tile_size_l1}"],
            "fusion": ["-affine-loop-fusion"] if self.enable_fusion else [],
            "unroll": [f"-affine-loop-unroll=unroll-factor={self.unroll_factor}"] if self.unroll_factor > 1 else [],
            "coalescing": ["-affine-loop-coalescing"] if self.enable_coalescing else [],
            "scalrep": ["-affine-scalrep"] if self.enable_scalrep else [],
            "vectorize": [f"-affine-super-vectorize=virtual-vector-size={self.vector_width // 64}"] if self.enable_super_vectorize else []
        }

        for pass_name in self.pass_order:
            if pass_name in pass_mapping:
                flags.extend(pass_mapping[pass_name])
        return flags


class TuningSearchSpace:
    """Manages parameter bounds and discrete choices for compiler autotuning."""

    TILE_SIZES = [4, 8, 16, 32, 64, 128, 256]
    UNROLL_FACTORS = [1, 2, 4, 8, 16]
    VECTOR_WIDTHS = [128, 256, 512]
    PASS_NAMES = ["tile", "fusion", "unroll", "scalrep", "coalescing", "vectorize"]

    @classmethod
    def get_search_space_dimensions(cls) -> Dict[str, Any]:
        return {
            "tile_size_l1": cls.TILE_SIZES,
            "tile_size_k": cls.TILE_SIZES,
            "unroll_factor": cls.UNROLL_FACTORS,
            "enable_fusion": [True, False],
            "enable_scalrep": [True, False],
            "enable_coalescing": [True, False],
            "enable_super_vectorize": [True, False],
            "vector_width": cls.VECTOR_WIDTHS,
        }

    @classmethod
    def total_discrete_configurations(cls) -> int:
        """Calculates the size of the discrete parameter search space."""
        dims = cls.get_search_space_dimensions()
        total = 1
        for choices in dims.values():
            total *= len(choices)
        # Multiply by possible pass orderings (6! = 720)
        import math
        total_with_order = total * math.factorial(len(cls.PASS_NAMES))
        return total_with_order
