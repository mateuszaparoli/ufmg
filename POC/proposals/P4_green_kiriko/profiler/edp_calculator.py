"""
Energy-Delay Product (EDP) and Multi-objective Pareto Frontier Calculator.
"""

from typing import Dict, Any, List


class EDPCalculator:
    """Calculates EDP (Joules * Seconds) and ED^2P (Joules * Seconds^2)."""

    @staticmethod
    def compute_metrics(energy_joules: float, runtime_sec: float) -> Dict[str, float]:
        edp = energy_joules * runtime_sec
        ed2p = energy_joules * (runtime_sec ** 2)
        return {
            "energy_joules": round(energy_joules, 4),
            "runtime_sec": round(runtime_sec, 4),
            "edp": round(edp, 6),
            "ed2p": round(ed2p, 8)
        }

    @staticmethod
    def find_pareto_frontier(configurations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies non-dominated points in the (Runtime, Energy) 2D plane."""
        pareto = []
        for i, c1 in enumerate(configurations):
            dominated = False
            for j, c2 in enumerate(configurations):
                if i != j:
                    e1 = c1.get("energy_joules", c1.get("total_energy_joules", 0.0))
                    e2 = c2.get("energy_joules", c2.get("total_energy_joules", 0.0))
                    if (c2["runtime_ms"] <= c1["runtime_ms"] and e2 <= e1) and \
                       (c2["runtime_ms"] < c1["runtime_ms"] or e2 < e1):
                        dominated = True
                        break
            if not dominated:
                pareto.append(c1)
        return pareto
