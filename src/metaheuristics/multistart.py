"""GRASP, Iterated Local Search, and Variable Neighborhood Search for QAP."""

from __future__ import annotations

import numpy as np
from numpy.random import Generator

from .neighborhood import local_search
from .qap import QAPInstance
from .results import HistoryPoint, OptimizationResult


def _random_sublist(
    solution: np.ndarray,
    size: int,
    generator: Generator,
) -> np.ndarray:
    """Shuffle a fixed-size cyclic sublist of a permutation."""

    candidate = solution.copy()
    sublist_size = min(len(candidate), max(2, size))
    start = int(generator.integers(len(candidate)))
    indices = (start + np.arange(sublist_size)) % len(candidate)
    candidate[indices] = generator.permutation(candidate[indices])
    return candidate


def _randomized_greedy_solution(
    instance: QAPInstance,
    restricted_list_size: int,
    generator: Generator,
) -> np.ndarray:
    """Construct one solution from restricted candidate lists."""

    available_facilities = list(range(instance.size))
    available_locations = list(range(instance.size))
    flow_potential = instance.flows.sum(axis=1)
    distance_potential = instance.distances.sum(axis=1)
    solution = np.empty(instance.size, dtype=np.int64)

    while available_facilities:
        width = min(restricted_list_size, len(available_facilities))
        facility_rcl = sorted(available_facilities, key=lambda index: -flow_potential[index])[
            :width
        ]
        location_rcl = sorted(available_locations, key=lambda index: distance_potential[index])[
            :width
        ]
        facility = int(generator.choice(facility_rcl))
        location = int(generator.choice(location_rcl))
        solution[facility] = location
        available_facilities.remove(facility)
        available_locations.remove(location)
    return solution


def grasp(
    instance: QAPInstance,
    *,
    constructions: int = 5,
    restricted_fraction: float = 0.1,
    seed: int | None = None,
) -> OptimizationResult:
    """Build and locally improve several randomized greedy solutions."""

    if constructions < 1:
        raise ValueError("constructions must be positive")
    generator = np.random.default_rng(seed)
    restricted_size = max(1, int(round(restricted_fraction * instance.size)))
    best_solution: np.ndarray | None = None
    best_cost = float("inf")
    evaluations = 0
    history: list[HistoryPoint] = []

    for _construction in range(1, constructions + 1):
        initial = _randomized_greedy_solution(instance, restricted_size, generator)
        result = local_search(
            instance,
            initial,
            strategy="first",
            shuffle_neighborhood=False,
            seed=int(generator.integers(0, 2**32 - 1)),
        )
        evaluations += result.evaluations
        if result.cost < best_cost:
            best_solution = result.solution.copy()
            best_cost = result.cost
            history.append(HistoryPoint(evaluations, best_cost))

    assert best_solution is not None
    return OptimizationResult(
        solution=best_solution,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=len(history),
        history=tuple(history),
        metadata={"constructions": constructions, "restricted_list_size": restricted_size},
    )


def iterated_local_search(
    instance: QAPInstance,
    *,
    local_searches: int = 10,
    perturbation_fraction: float = 0.25,
    seed: int | None = None,
) -> OptimizationResult:
    """ILS using strong cyclic-sublist perturbations and best-so-far acceptance."""

    if local_searches < 1:
        raise ValueError("local_searches must be positive")
    generator = np.random.default_rng(seed)
    perturbation_size = max(2, int(instance.size * perturbation_fraction))
    initial = generator.permutation(instance.size)
    result = local_search(
        instance,
        initial,
        strategy="first",
        shuffle_neighborhood=False,
        seed=int(generator.integers(0, 2**32 - 1)),
    )
    best_solution = result.solution.copy()
    best_cost = result.cost
    evaluations = result.evaluations
    history = [HistoryPoint(evaluations, best_cost)]

    for _ in range(1, local_searches):
        perturbed = _random_sublist(best_solution, perturbation_size, generator)
        result = local_search(
            instance,
            perturbed,
            strategy="first",
            shuffle_neighborhood=False,
            seed=int(generator.integers(0, 2**32 - 1)),
        )
        evaluations += result.evaluations
        if result.cost < best_cost:
            best_solution = result.solution.copy()
            best_cost = result.cost
            history.append(HistoryPoint(evaluations, best_cost))

    return OptimizationResult(
        solution=best_solution,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=len(history),
        history=tuple(history),
        metadata={
            "local_searches": local_searches,
            "perturbation_size": perturbation_size,
        },
    )


def variable_neighborhood_search(
    instance: QAPInstance,
    *,
    max_local_searches: int = 10,
    max_neighborhood: int = 5,
    seed: int | None = None,
) -> OptimizationResult:
    """VNS with five cyclic-sublist neighborhoods and an exact search budget."""

    if max_local_searches < 1 or max_neighborhood < 1:
        raise ValueError("Search and neighborhood limits must be positive")
    generator = np.random.default_rng(seed)
    current = generator.permutation(instance.size)
    current_cost = instance.cost(current)
    evaluations = 1
    history = [HistoryPoint(evaluations, current_cost)]
    neighborhood = 1

    for _ in range(max_local_searches):
        if neighborhood > max_neighborhood:
            neighborhood = 1
        denominator = max(1, 9 - neighborhood)
        sublist_size = max(2, instance.size // denominator)
        shaken = _random_sublist(current, sublist_size, generator)
        result = local_search(
            instance,
            shaken,
            strategy="first",
            shuffle_neighborhood=False,
            seed=int(generator.integers(0, 2**32 - 1)),
        )
        evaluations += result.evaluations
        if result.cost < current_cost:
            current = result.solution.copy()
            current_cost = result.cost
            neighborhood = 1
            history.append(HistoryPoint(evaluations, current_cost))
        else:
            neighborhood += 1

    return OptimizationResult(
        solution=current,
        cost=current_cost,
        evaluations=evaluations,
        best_iteration=len(history) - 1,
        history=tuple(history),
        metadata={
            "local_searches": max_local_searches,
            "max_neighborhood": max_neighborhood,
        },
    )
