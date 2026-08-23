"""
FPGA and CGRA Area, Timing, and Resource Estimator for MLIR Spatial Acceleration.
Models Xilinx/AMD UltraScale+ and Intel Agilex FPGA resources (LUTs, DSPs, FFs, BRAMs).
"""

from typing import Dict, Any


class SpatialHardwareEstimator:
    """Estimates silicon area, frequency (Fmax), and hardware throughput."""

    def __init__(self, target_fpga: str = "Xilinx UltraScale+ VU9P"):
        self.target_fpga = target_fpga
        # Approximate resource costs per 64-bit FP operator on UltraScale+
        self.lut_per_fp64_add = 650
        self.lut_per_fp64_mul = 420
        self.dsp_per_fp64_mul = 3
        self.dsp_per_fp64_add = 2

    def estimate_resources(self, cdfg_info: Dict[str, Any], unroll_factor: int = 1) -> Dict[str, Any]:
        """Calculates total resource utilization and timing for pipelined spatial hardware."""
        n_mul = cdfg_info["num_multipliers"] * unroll_factor
        n_add = cdfg_info["num_adders"] * unroll_factor
        n_ports = (cdfg_info["memory_read_ports"] + cdfg_info["memory_write_ports"]) * unroll_factor

        total_luts = (n_mul * self.lut_per_fp64_mul) + (n_add * self.lut_per_fp64_add) + (n_ports * 80)
        total_dsps = (n_mul * self.dsp_per_fp64_mul) + (n_add * self.dsp_per_fp64_add)
        total_ffs = total_luts * 2
        total_brams = max(2, (n_ports * 2))

        # Clock frequency in MHz (Fmax degrades with unroll factor and routing congestion)
        base_fmax_mhz = 450.0
        fmax_mhz = max(150.0, base_fmax_mhz - (unroll_factor * 8.5))

        # Throughput in Operations per Second = (Operations / cycle) * Fmax
        ops_per_cycle = (n_mul + n_add)
        gflops_spatial = (ops_per_cycle * fmax_mhz * 1e6) / 1e9

        return {
            "target_hardware": self.target_fpga,
            "unroll_factor": unroll_factor,
            "luts": total_luts,
            "dsps": total_dsps,
            "flip_flops": total_ffs,
            "bram_18k": total_brams,
            "fmax_mhz": round(fmax_mhz, 1),
            "operations_per_cycle": ops_per_cycle,
            "peak_gflops": round(gflops_spatial, 2)
        }
