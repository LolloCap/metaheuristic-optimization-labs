from __future__ import annotations

import numpy as np

from metaheuristics.evolutionary import (
    chc_genetic_algorithm,
    multimodal_genetic_algorithm,
    simple_genetic_algorithm,
)
from metaheuristics.multistart import grasp, iterated_local_search, variable_neighborhood_search
from metaheuristics.neighborhood import (
    greedy_qap,
    local_search,
    random_search,
    simulated_annealing,
    tabu_search,
)
from metaheuristics.qap import QAPInstance


def assert_valid_result(instance: QAPInstance, result) -> None:
    assert np.array_equal(np.sort(result.solution), np.arange(instance.size))
    assert result.cost == instance.cost(result.solution)
    assert result.evaluations > 0


def test_neighborhood_algorithms_return_valid_permutations(small_qap: QAPInstance) -> None:
    results = [
        greedy_qap(small_qap),
        random_search(small_qap, iterations=25, seed=1),
        local_search(small_qap, strategy="first", seed=2),
        local_search(small_qap, strategy="best", seed=3),
        simulated_annealing(small_qap, max_coolings=10, seed=4),
        tabu_search(small_qap, max_iterations=25, seed=5),
    ]
    for result in results:
        assert_valid_result(small_qap, result)


def test_multistart_algorithms_respect_search_counts(small_qap: QAPInstance) -> None:
    results = [
        grasp(small_qap, constructions=3, seed=6),
        iterated_local_search(small_qap, local_searches=4, seed=7),
        variable_neighborhood_search(small_qap, max_local_searches=5, seed=8),
    ]
    for result in results:
        assert_valid_result(small_qap, result)
    assert results[1].metadata["local_searches"] == 4
    assert results[2].metadata["local_searches"] == 5


def test_evolutionary_algorithms_keep_population_shape(small_qap: QAPInstance) -> None:
    results = [
        simple_genetic_algorithm(small_qap, population_size=8, generations=3, seed=9),
        chc_genetic_algorithm(small_qap, population_size=8, max_evaluations=80, seed=10),
        multimodal_genetic_algorithm(
            small_qap, population_size=8, generations=3, radius=1, seed=11
        ),
    ]
    for result in results:
        assert_valid_result(small_qap, result)
    assert results[0].evaluations == 32
    assert results[2].evaluations == 32


def test_seeded_run_is_reproducible(small_qap: QAPInstance) -> None:
    first = random_search(small_qap, iterations=40, seed=123)
    second = random_search(small_qap, iterations=40, seed=123)
    assert first.cost == second.cost
    assert np.array_equal(first.solution, second.solution)
