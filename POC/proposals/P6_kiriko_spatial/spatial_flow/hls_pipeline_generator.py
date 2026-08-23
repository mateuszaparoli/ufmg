"""
SODA-OPT & CIRCT Hardware High-Level Synthesis Pipeline Generator.
Transforms MLIR Affine into spatial dataflow pipelines for hardware accelerator generation.
"""

from typing import List


class SpatialHLSPipeline:
    """Manages the compilation pipeline for MLIR to Hardware synthesis."""

    @staticmethod
    def get_hls_pipeline_passes() -> List[str]:
        """Returns the passes required to generate dataflow hardware from Affine IR."""
        return [
            # 1. Polyhedral optimization for spatial streaming
            "-affine-loop-tile=tile-size=16",
            "-affine-loop-unroll=unroll-factor=4",
            # 2. Extract hardware kernels into SODA / CIRCT spatial dialect
            "-soda-opt-pipeline",
            "-convert-affine-to-soda",
            # 3. Lower control flow to handshake / dataflow CIRCT dialect
            "-convert-scf-to-circt-handshake",
            "-canonicalize"
        ]
