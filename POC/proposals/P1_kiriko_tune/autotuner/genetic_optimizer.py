"""
Genetic Algorithm Optimizer for Pass Permutations and Tile Sizing in Kiriko-Tune.
Represents compiler configurations as chromosomes with crossover and mutation.
"""

import random
import copy
from typing import List, Dict, Any, Tuple
from .search_space import AffineTuningConfig, TuningSearchSpace
from .evaluator import KernelEvaluator


class GeneticCompilerOptimizer:
    """Evolutionary algorithm searching over compiler pass orderings and parameters."""

    def __init__(
        self,
        evaluator: KernelEvaluator,
        population_size: int = 16,
        generations: int = 6,
        mutation_rate: float = 0.25,
        crossover_rate: float = 0.75,
        elite_size: int = 2,
        seed: int = 42
    ):
        self.evaluator = evaluator
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        random.seed(seed)
        self.history: List[Dict[str, Any]] = []

    def _random_individual(self) -> AffineTuningConfig:
        pass_order = copy.deepcopy(TuningSearchSpace.PASS_NAMES)
        random.shuffle(pass_order)
        return AffineTuningConfig(
            tile_size_l1=random.choice(TuningSearchSpace.TILE_SIZES),
            tile_size_k=random.choice(TuningSearchSpace.TILE_SIZES),
            unroll_factor=random.choice(TuningSearchSpace.UNROLL_FACTORS),
            enable_fusion=random.choice([True, False]),
            enable_scalrep=random.choice([True, False]),
            enable_coalescing=random.choice([True, False]),
            enable_super_vectorize=random.choice([True, False]),
            vector_width=random.choice(TuningSearchSpace.VECTOR_WIDTHS),
            pass_order=pass_order
        )

    def _mutate(self, ind: AffineTuningConfig) -> AffineTuningConfig:
        mut = copy.deepcopy(ind)
        if random.random() < self.mutation_rate:
            mut.tile_size_l1 = random.choice(TuningSearchSpace.TILE_SIZES)
        if random.random() < self.mutation_rate:
            mut.tile_size_k = random.choice(TuningSearchSpace.TILE_SIZES)
        if random.random() < self.mutation_rate:
            mut.unroll_factor = random.choice(TuningSearchSpace.UNROLL_FACTORS)
        if random.random() < self.mutation_rate:
            mut.enable_fusion = not mut.enable_fusion
        if random.random() < self.mutation_rate:
            mut.enable_scalrep = not mut.enable_scalrep
        if random.random() < self.mutation_rate:
            mut.vector_width = random.choice(TuningSearchSpace.VECTOR_WIDTHS)
        if random.random() < self.mutation_rate and len(mut.pass_order) >= 2:
            i, j = random.sample(range(len(mut.pass_order)), 2)
            mut.pass_order[i], mut.pass_order[j] = mut.pass_order[j], mut.pass_order[i]
        return mut

    def _crossover(self, p1: AffineTuningConfig, p2: AffineTuningConfig) -> Tuple[AffineTuningConfig, AffineTuningConfig]:
        c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
        if random.random() < self.crossover_rate:
            c1.tile_size_l1, c2.tile_size_l1 = p2.tile_size_l1, p1.tile_size_l1
            c1.unroll_factor, c2.unroll_factor = p2.unroll_factor, p1.unroll_factor
            c1.vector_width, c2.vector_width = p2.vector_width, p1.vector_width
            c1.enable_scalrep, c2.enable_scalrep = p2.enable_scalrep, p1.enable_scalrep
        return c1, c2

    def run_evolution(self) -> Dict[str, Any]:
        """Runs the genetic algorithm loop."""
        population = [self._random_individual() for _ in range(self.population_size)]
        best_overall_score = -1.0
        best_overall_config = None

        trial_count = 0
        for gen in range(self.generations):
            scored = []
            for ind in population:
                trial_count += 1
                res = self.evaluator.evaluate_configuration(ind)
                score = res["speedup"]
                scored.append((score, ind, res))

                self.history.append({
                    "generation": gen,
                    "trial": trial_count,
                    "speedup": score,
                    "runtime_ms": res["runtime_ms"],
                    "config": ind.to_dict(),
                    "flags": res["flags"]
                })

                if score > best_overall_score:
                    best_overall_score = score
                    best_overall_config = ind

            scored.sort(key=lambda x: x[0], reverse=True)
            elites = [scored[i][1] for i in range(self.elite_size)]

            # Selection via tournament
            new_pop = list(elites)
            while len(new_pop) < self.population_size:
                p1 = max(random.sample(scored, 3), key=lambda x: x[0])[1]
                p2 = max(random.sample(scored, 3), key=lambda x: x[0])[1]
                c1, c2 = self._crossover(p1, p2)
                new_pop.append(self._mutate(c1))
                if len(new_pop) < self.population_size:
                    new_pop.append(self._mutate(c2))
            population = new_pop

        return {
            "best_speedup": round(best_overall_score, 3),
            "best_config": best_overall_config.to_dict() if best_overall_config else {},
            "total_evaluations": trial_count,
            "history": self.history
        }
