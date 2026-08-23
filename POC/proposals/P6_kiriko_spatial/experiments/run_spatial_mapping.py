#!/usr/bin/env python3
"""
Spatial Acceleration & Hardware Synthesis Mapping Benchmark.
Evaluates FPGA resource usage (LUTs, DSPs), Frequency (Fmax), and Throughput across PolyBench Kernels.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spatial_flow.cdfg_extractor import CDFGExtractor
from spatial_flow.area_delay_estimator import SpatialHardwareEstimator

# Sample MLIR kernel definitions
KERNELS_MLIR = {
    "gemm": "affine.for %i { affine.for %j { affine.for %k { %v = affine.load; %m = arith.mulf; %a = arith.addf; affine.store; } } }",
    "stencil2d": "affine.for %i { affine.for %j { %l1 = affine.load; %l2 = affine.load; %s = arith.subf; %m = arith.mulf; affine.store; } }",
    "atax": "affine.for %i { affine.for %j { %l = affine.load; %m = arith.mulf; %a = arith.addf; affine.store; } }",
    "2mm": "affine.for %i { affine.for %j { %m1 = arith.mulf; %a1 = arith.addf; %m2 = arith.mulf; %a2 = arith.addf; } }"
}


def run_spatial_study():
    print("=" * 85)
    print("🛰️ [Kiriko-Spatial] Hardware Acceleration & Spatial Dataflow Synthesis Study")
    print("=" * 85)

    estimator = SpatialHardwareEstimator()
    results = []

    print(f"\n{'Kernel':<12} | {'Unroll':<7} | {'LUTs':<8} | {'DSPs':<6} | {'Fmax (MHz)':<12} | {'Throughput (GFLOPS)':<20}")
    print("-" * 88)

    for name, code in KERNELS_MLIR.items():
        cdfg = CDFGExtractor.extract_from_mlir(code)
        for u in [1, 4, 8]:
            hw = estimator.estimate_resources(cdfg, unroll_factor=u)
            print(f"{name:<12} | {u:<7} | {hw['luts']:<8} | {hw['dsps']:<6} | {hw['fmax_mhz']:<12.1f} | {hw['peak_gflops']:<20.2f}")
            results.append({
                "kernel": name,
                "unroll_factor": u,
                "resources": hw
            })

    output_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "spatial_hardware_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Spatial Experiment completed! Results saved to: {out_path}")
    print("=" * 85)


if __name__ == "__main__":
    run_spatial_study()
