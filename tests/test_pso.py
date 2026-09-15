from __future__ import annotations

import json

import numpy as np

from metaheuristics.pso import local_search_rastrigin, particle_swarm_optimization, rastrigin


def test_rastrigin_global_minimum() -> None:
    assert rastrigin(np.zeros(2)) == 0.0
    assert np.array_equal(rastrigin(np.zeros((3, 2))), np.zeros(3))


def test_pso_evaluation_count_and_bounds() -> None:
    result = particle_swarm_optimization(particles=10, iterations=4, seed=42)
    assert result.evaluations == 50
    assert np.all(result.solution >= -5.12)
    assert np.all(result.solution <= 5.12)
    assert result.cost == rastrigin(result.solution)
    json.dumps(result.as_dict())


def test_local_search_evaluation_count() -> None:
    result = local_search_rastrigin(iterations=4, neighbors=10, seed=42)
    assert result.evaluations == 41
    assert result.cost == rastrigin(result.solution)
