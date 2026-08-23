"""
Differential Testing Engine & Metamorphic Oracle for Polyhedral Passes.
"""

import numpy as np
from typing import Dict, Any, List, Tuple


class DifferentialEngine:
    """Compares numerical outputs of unoptimized baseline vs optimized MLIR pipeline."""

    @staticmethod
    def verify_equivalence(output_ref: np.ndarray, output_opt: np.ndarray, tolerance: float = 1e-5) -> Dict[str, Any]:
        """Verifies if two output tensors are numerically equivalent within floating point tolerance."""
        if output_ref.shape != output_opt.shape:
            return {
                "equivalent": False,
                "error": f"Shape mismatch: {output_ref.shape} vs {output_opt.shape}",
                "max_diff": float("inf")
            }

        abs_diff = np.abs(output_ref - output_opt)
        max_diff = float(np.max(abs_diff))
        is_equiv = bool(max_diff <= tolerance)

        return {
            "equivalent": is_equiv,
            "max_difference": max_diff,
            "mean_difference": float(np.mean(abs_diff)),
            "tolerance_used": tolerance
        }
