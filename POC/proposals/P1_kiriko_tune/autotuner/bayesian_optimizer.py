"""
Bayesian Optimizer for Compiler Pipelines using Optuna & Tree-structured Parzen Estimator (TPE).
Searches for optimal multi-level tiling, loop unrolling, and vectorization widths.
"""

import optuna
import numpy as np
from typing import Dict, Any, List, Tuple, Callable
from .search_space import AffineTuningConfig, TuningSearchSpace
from .evaluator import KernelEvaluator

# Suppress verbose Optuna logging
optuna.logging.set_verbosity(optuna.logging.WARNING)


class BayesianCompilerAutotuner:
    """Bayesian Optimization Engine for MLIR Affine Dialect."""

    def __init__(self, evaluator: KernelEvaluator, n_trials: int = 50, seed: int = 42):
        self.evaluator = evaluator
        self.n_trials = n_trials
        self.seed = seed
        self.sampler = optuna.samplers.TPESampler(seed=seed, multivariate=True)
        self.study = optuna.create_study(direction="maximize", sampler=self.sampler)
        self.history: List[Dict[str, Any]] = []

    def _objective(self, trial: optuna.Trial) -> float:
        # Sample discrete choices from the defined search space
        tile_l1 = trial.suggest_categorical("tile_size_l1", TuningSearchSpace.TILE_SIZES)
        tile_k = trial.suggest_categorical("tile_size_k", TuningSearchSpace.TILE_SIZES)
        unroll = trial.suggest_categorical("unroll_factor", TuningSearchSpace.UNROLL_FACTORS)
        enable_fusion = trial.suggest_categorical("enable_fusion", [True, False])
        enable_scalrep = trial.suggest_categorical("enable_scalrep", [True, False])
        enable_coalescing = trial.suggest_categorical("enable_coalescing", [True, False])
        enable_vec = trial.suggest_categorical("enable_super_vectorize", [True, False])
        vec_w = trial.suggest_categorical("vector_width", TuningSearchSpace.VECTOR_WIDTHS)

        config = AffineTuningConfig(
            tile_size_l1=tile_l1,
            tile_size_k=tile_k,
            unroll_factor=unroll,
            enable_fusion=enable_fusion,
            enable_scalrep=enable_scalrep,
            enable_coalescing=enable_coalescing,
            enable_super_vectorize=enable_vec,
            vector_width=vec_w,
        )

        result = self.evaluator.evaluate_configuration(config)
        speedup = result["speedup"]

        record = {
            "trial": trial.number,
            "speedup": speedup,
            "runtime_ms": result["runtime_ms"],
            "config": config.to_dict(),
            "flags": result["flags"],
        }
        self.history.append(record)
        return speedup

    def run_optimization(self) -> Dict[str, Any]:
        """Executes the Bayesian optimization search loop."""
        self.study.optimize(self._objective, n_trials=self.n_trials)
        best_trial = self.study.best_trial
        return {
            "best_speedup": round(best_trial.value, 3),
            "best_params": best_trial.params,
            "total_trials": len(self.study.trials),
            "history": self.history
        }
