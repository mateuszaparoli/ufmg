#!/usr/bin/env python3
"""
Experiment Runner: Benchmarking Bayesian vs Genetic vs Random Autotuning for GEMM and Jacobi-2D.
Demonstrates how Kiriko-Tune recovers peak performance on MLIR Affine.
"""

import os
import sys
import json
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autotuner.search_space import AffineTuningConfig
from autotuner.evaluator import KernelEvaluator
from autotuner.bayesian_optimizer import BayesianCompilerAutotuner
from autotuner.genetic_optimizer import GeneticCompilerOptimizer
from autotuner.random_search import RandomSearchOptimizer


def run_comparative_experiment():
    print("=" * 70)
    print("🚀 [Kiriko-Tune] Starting Autotuning Optimization Study for MLIR Affine")
    print("=" * 70)

    evaluator = KernelEvaluator(kernel_name="gemm", matrix_size=512, baseline_time_ms=450.0)

    # 1. Standard Static Kiriko Configuration (from LaC TechReport 02/2026)
    static_kiriko_config = AffineTuningConfig(
        tile_size_l1=32,
        tile_size_k=16,
        unroll_factor=4,
        enable_fusion=True,
        enable_scalrep=False,  # Scalrep was limited in static
        enable_super_vectorize=False,  # Baseline affine pipeline had no SIMD tuning
        vector_width=128
    )
    static_res = evaluator.evaluate_configuration(static_kiriko_config)
    print(f"\n[Baseline 1] Clang -O0 Baseline Time: {evaluator.baseline_time_ms:.1f} ms (Speedup: 1.00x)")
    print(f"[Baseline 2] Static MLIR Affine Pipeline (Artigo LaC): {static_res['runtime_ms']:.1f} ms (Speedup: {static_res['speedup']:.2f}x)")

    # 2. Random Search (50 trials)
    print("\n🔍 Running Random Search Autotuning (50 trials)...")
    random_opt = RandomSearchOptimizer(evaluator, n_trials=50, seed=42)
    random_res = random_opt.run_optimization()
    print(f"  --> Best Random Search Speedup: {random_res['best_speedup']:.2f}x")

    # 3. Genetic Algorithm (50 evaluations)
    print("\n🧬 Running Genetic Algorithm Autotuning (6 gens, pop 16)...")
    genetic_opt = GeneticCompilerOptimizer(evaluator, population_size=16, generations=6, seed=42)
    genetic_res = genetic_opt.run_evolution()
    print(f"  --> Best Genetic Algorithm Speedup: {genetic_res['best_speedup']:.2f}x")

    # 4. Bayesian Optimization via TPE (50 trials)
    print("\n🧠 Running Bayesian Optimization Autotuning via Optuna TPE (50 trials)...")
    bayes_opt = BayesianCompilerAutotuner(evaluator, n_trials=50, seed=42)
    bayes_res = bayes_opt.run_optimization()
    print(f"  --> Best Bayesian Optimization Speedup: {bayes_res['best_speedup']:.2f}x")
    print(f"  --> Optimal Parameters Discovered: {bayes_res['best_params']}")

    # Save summary data
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "autotuning_summary.json")

    results_data = {
        "kernel": "gemm",
        "baseline_clang_o0_speedup": 1.00,
        "static_kiriko_mlir_speedup": static_res["speedup"],
        "random_search_best_speedup": random_res["best_speedup"],
        "genetic_algorithm_best_speedup": genetic_res["best_speedup"],
        "bayesian_optimization_best_speedup": bayes_res["best_speedup"],
        "bayesian_best_params": bayes_res["best_params"],
        "bayes_history": bayes_res["history"],
        "genetic_history": genetic_res["history"],
        "random_history": random_res["history"]
    }

    with open(summary_path, "w") as f:
        json.dump(results_data, f, indent=2)

    print(f"\n✅ Experiment completed! Results saved to: {summary_path}")
    print("=" * 70)
    return results_data


if __name__ == "__main__":
    run_comparative_experiment()
