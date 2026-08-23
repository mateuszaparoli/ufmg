"""
Random Search Baseline Optimizer for Compiler Tuning.
"""

import random
from typing import List, Dict, Any
from .search_space import AffineTuningConfig, TuningSearchSpace
from .evaluator import KernelEvaluator


class RandomSearchOptimizer:
    """Random sampling baseline to evaluate relative efficiency of Bayesian and Genetic algorithms."""

    def __init__(self, evaluator: KernelEvaluator, n_trials: int = 50, seed: int = 42):
        self.evaluator = evaluator
        self.n_trials = n_trials
        random.seed(seed)
        self.history: List[Dict[str, Any]] = []

    def run_optimization(self) -> Dict[str, Any]:
        best_speedup = -1.0
        best_config = None

        for trial in range(self.n_trials):
            config = AffineTuningConfig(
                tile_size_l1=random.choice(TuningSearchSpace.TILE_SIZES),
                tile_size_k=random.choice(TuningSearchSpace.TILE_SIZES),
                unroll_factor=random.choice(TuningSearchSpace.UNROLL_FACTORS),
                enable_fusion=random.choice([True, False]),
                enable_scalrep=random.choice([True, False]),
                enable_coalescing=random.choice([True, False]),
                enable_super_vectorize=random.choice([True, False]),
                vector_width=random.choice(TuningSearchSpace.VECTOR_WIDTHS),
            )
            res = self.evaluator.evaluate_configuration(config)
            score = res["speedup"]

            self.history.append({
                "trial": trial,
                "speedup": score,
                "runtime_ms": res["runtime_ms"],
                "config": config.to_dict(),
                "flags": res["flags"]
            })

            if score > best_speedup:
                best_speedup = score
                best_config = config

        return {
            "best_speedup": round(best_speedup, 3),
            "best_config": best_config.to_dict() if best_config else {},
            "total_trials": self.n_trials,
            "history": self.history
        }
