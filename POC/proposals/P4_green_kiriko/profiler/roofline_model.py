"""
Dynamic Roofline Model Calculator for Compiler Optimizations.
Correlates Arithmetic Intensity (FLOPs / Byte) with Compute Performance (GFLOPS/s).
"""

from typing import Dict, Any


class DynamicRooflineModel:
    """Evaluates arithmetic intensity and hardware efficiency bounds."""

    def __init__(self, peak_gflops: float = 350.0, peak_bandwidth_gb_s: float = 68.0):
        self.peak_gflops = peak_gflops
        self.peak_bandwidth = peak_bandwidth_gb_s
        self.ridge_point = peak_gflops / peak_bandwidth_gb_s  # FLOPs/Byte

    def evaluate_kernel(self, total_flops: float, bytes_moved: float, runtime_sec: float) -> Dict[str, Any]:
        arithmetic_intensity = total_flops / max(1.0, bytes_moved)
        achieved_gflops = (total_flops / (runtime_sec * 1e9))
        
        # Theoretical ceiling based on Roofline
        theoretical_ceiling = min(self.peak_gflops, arithmetic_intensity * self.peak_bandwidth)
        efficiency_pct = (achieved_gflops / theoretical_ceiling) * 100.0

        is_compute_bound = arithmetic_intensity >= self.ridge_point

        return {
            "arithmetic_intensity_flops_per_byte": round(arithmetic_intensity, 2),
            "achieved_gflops": round(achieved_gflops, 2),
            "theoretical_ceiling_gflops": round(theoretical_ceiling, 2),
            "hardware_efficiency_pct": round(efficiency_pct, 1),
            "limiting_factor": "Compute" if is_compute_bound else "Memory Bandwidth",
            "ridge_point": round(self.ridge_point, 2)
        }
