"""
Linalg Dialect Transformation Pipeline Generator.
Demonstrates structured tiling, operator fusion, bufferization, and vectorization.
"""

from typing import List


class LinalgPipelineGenerator:
    """Manages MLIR pass pipelines for Linalg structured transformations."""

    @staticmethod
    def get_structured_tiling_passes(tile_m: int = 32, tile_n: int = 32, tile_k: int = 16) -> List[str]:
        """Returns the pipeline for Linalg tile-and-fuse on tensors."""
        return [
            # 1. Transform dialect / linalg structured tiling
            f"-linalg-fuse-elementwise-ops",
            f"-test-linalg-transform-patterns=tile-sizes={tile_m},{tile_n},{tile_k}",
            # 2. Comprehensive bufferization (convert tensor semantics to memref)
            "-one-shot-bufferize=bufferize-function-boundaries",
            # 3. Vectorize structured linalg operations to vector dialect
            "-convert-linalg-to-vector",
            # 4. Standard lowering to LLVM
            "-convert-vector-to-scf",
            "-convert-scf-to-cf",
            "-finalize-memref-to-llvm",
            "-convert-func-to-llvm",
            "-reconcile-unrealized-casts"
        ]

    @staticmethod
    def get_linalg_to_affine_passes() -> List[str]:
        """Bridge pipeline: lowers Linalg structured ops to Affine loops for polyhedral analysis."""
        return [
            "-one-shot-bufferize=bufferize-function-boundaries",
            "-convert-linalg-to-affine-loops",
            "-affine-loop-tile=tile-size=32",
            "-affine-loop-fusion",
            "-affine-super-vectorize"
        ]
