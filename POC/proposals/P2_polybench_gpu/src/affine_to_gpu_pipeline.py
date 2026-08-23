"""
MLIR Affine to GPU Dialect Lowering Pipeline Generator.
Demonstrates lowering sequence from affine.for/affine.parallel to gpu.launch and NVVM/PTX.
"""

from typing import List, Dict, Any


class MLIRGpuPipeline:
    """Manages MLIR pass pipelines for targetting NVIDIA and AMD GPUs."""

    @staticmethod
    def get_affine_to_gpu_passes(block_x: int = 16, block_y: int = 16) -> List[str]:
        """Returns the pipeline that converts Affine loop nests to GPU kernel launches."""
        return [
            # 1. Polyhedral parallelization and loop tiling for GPU workgroups
            f"-affine-parallelize",
            f"-affine-loop-tile=tile-size={block_x}",
            # 2. Map parallel loops to GPU thread blocks and grids
            f"-convert-affine-to-gpu=gpu-block-dims={block_x},{block_y},1",
            # 3. Outline kernel into a nested gpu.module
            "-gpu-kernel-outlining",
            # 4. Standard memory and arithmetic lowerings
            "-lower-affine",
            "-convert-scf-to-cf",
            "-convert-math-to-funcs",
            "-finalize-memref-to-llvm",
        ]

    @staticmethod
    def get_gpu_to_nvvm_passes() -> List[str]:
        """Returns the lowering pipeline from MLIR GPU dialect to NVIDIA NVVM dialect."""
        return [
            "-convert-gpu-to-nvvm",
            "-convert-arith-to-llvm",
            "-convert-func-to-llvm",
            "-reconcile-unrealized-casts"
        ]

    @staticmethod
    def get_gpu_to_rocdl_passes() -> List[str]:
        """Returns the lowering pipeline from MLIR GPU dialect to AMD ROCm ROCDL dialect."""
        return [
            "-convert-gpu-to-rocdl",
            "-convert-arith-to-llvm",
            "-convert-func-to-llvm",
            "-reconcile-unrealized-casts"
        ]
