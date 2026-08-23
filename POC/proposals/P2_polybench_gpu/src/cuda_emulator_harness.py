"""
GPU Microarchitectural Performance Model and Execution Harness.
Models NVIDIA GPU (e.g. RTX 4090 / A100) memory hierarchy, coalescing, and PCIe transfer latency.
"""

import time
import numpy as np
from typing import Dict, Any, List, Tuple


class GPUMicroarchModel:
    """Models GPU execution latency, compute throughput, memory bandwidth, and transfer overheads."""

    def __init__(
        self,
        gpu_name: str = "NVIDIA RTX 4090 / A100 Class",
        peak_tflops_fp32: float = 35.0,
        memory_bandwidth_gb_s: float = 1000.0,  # 1 TB/s memory bandwidth
        pcie_bandwidth_gb_s: float = 32.0,      # PCIe 4.0 x16
        launch_overhead_us: float = 5.0,        # 5 microseconds kernel launch latency
    ):
        self.gpu_name = gpu_name
        self.peak_tflops = peak_tflops_fp32
        self.mem_bw = memory_bandwidth_gb_s
        self.pcie_bw = pcie_bandwidth_gb_s
        self.launch_overhead_us = launch_overhead_us

    def simulate_gemm(self, n: int, block_size: int = 16, use_shared_mem: bool = True) -> Dict[str, Any]:
        """
        Simulates GEMM execution on GPU.
        Computes PCIe transfer time, compute latency, global memory traffic, and occupancy.
        """
        flops = 2.0 * (n ** 3)
        bytes_per_matrix = (n * n) * 4.0  # FP32 = 4 bytes
        total_data_transferred_bytes = 3 * bytes_per_matrix  # 2 inputs + 1 output

        # 1. PCIe Data Transfer Latency (Host-to-Device + Device-to-Host)
        pcie_latency_ms = (total_data_transferred_bytes / (self.pcie_bw * 1e9)) * 1000.0

        # 2. Global Memory Traffic with vs without Shared Memory Tiling
        if use_shared_mem:
            # Re-use factor is equal to block_size
            dram_bytes = (2.0 * (n ** 3) * 4.0) / block_size
            coalescing_efficiency = 0.95
        else:
            # Uncoalesced / untiled direct global memory access
            dram_bytes = 2.0 * (n ** 3) * 4.0
            coalescing_efficiency = 0.40

        # 3. Kernel Compute vs Memory Bound Time (Roofline on GPU)
        compute_time_ms = (flops / (self.peak_tflops * 1e12)) * 1000.0
        effective_mem_bw = self.mem_bw * 1e9 * coalescing_efficiency
        memory_time_ms = (dram_bytes / effective_mem_bw) * 1000.0

        kernel_time_ms = max(compute_time_ms, memory_time_ms) + (self.launch_overhead_us / 1000.0)
        total_gpu_time_ms = kernel_time_ms + pcie_latency_ms

        return {
            "matrix_size": n,
            "kernel_time_ms": round(kernel_time_ms, 3),
            "pcie_transfer_ms": round(pcie_latency_ms, 3),
            "total_gpu_time_ms": round(total_gpu_time_ms, 3),
            "gflops_achieved": round((flops / (kernel_time_ms * 1e-3)) / 1e9, 1),
            "bound_by": "Compute" if compute_time_ms > memory_time_ms else "Memory Bandwidth",
            "use_shared_memory": use_shared_mem,
            "block_size": block_size
        }
