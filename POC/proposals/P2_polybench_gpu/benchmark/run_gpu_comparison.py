#!/usr/bin/env python3
"""
Benchmark Runner: Comparing CPU Baseline vs MLIR GPU Dialect across Matrix Sizes.
Identifies crossover points, memory transfer overheads, and peak GPU speedups.
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cuda_emulator_harness import GPUMicroarchModel


def run_cpu_vs_gpu_study():
    print("=" * 75)
    print("🔥 [PolyBench-GPU] Benchmarking CPU vs MLIR GPU Dialect Lowering")
    print("=" * 75)

    gpu_model = GPUMicroarchModel()
    matrix_sizes = [128, 256, 512, 1024, 2048, 4096]

    results = []

    print(f"\n{'Size (N)':<10} | {'CPU O3 (ms)':<12} | {'GPU Kernel (ms)':<16} | {'PCIe Xfer (ms)':<14} | {'Total GPU (ms)':<14} | {'Speedup':<10}")
    print("-" * 85)

    for n in matrix_sizes:
        # Theoretical CPU time based on AVX2 multicore (approx 150 GFLOPS peak on Xeon)
        cpu_flops = 2.0 * (n ** 3)
        cpu_time_ms = (cpu_flops / (150.0 * 1e9)) * 1000.0

        gpu_res = gpu_model.simulate_gemm(n, block_size=16, use_shared_mem=True)
        kernel_ms = gpu_res["kernel_time_ms"]
        pcie_ms = gpu_res["pcie_transfer_ms"]
        total_gpu_ms = gpu_res["total_gpu_time_ms"]

        speedup_kernel = cpu_time_ms / kernel_ms
        speedup_total = cpu_time_ms / total_gpu_ms

        print(f"{n:<10} | {cpu_time_ms:<12.2f} | {kernel_ms:<16.3f} | {pcie_ms:<14.3f} | {total_gpu_ms:<14.2f} | {speedup_total:<9.1f}x")

        results.append({
            "matrix_size": n,
            "cpu_time_ms": round(cpu_time_ms, 3),
            "gpu_kernel_ms": kernel_ms,
            "gpu_pcie_ms": pcie_ms,
            "total_gpu_ms": total_gpu_ms,
            "speedup_kernel_only": round(speedup_kernel, 2),
            "speedup_end_to_end": round(speedup_total, 2),
            "gflops": gpu_res["gflops_achieved"]
        })

    # Save results to JSON
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "gpu_benchmark_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ GPU Experiment completed! Results saved to: {out_file}")
    print("=" * 75)
    return results


if __name__ == "__main__":
    run_cpu_vs_gpu_study()
