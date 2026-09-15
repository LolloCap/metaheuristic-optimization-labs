"""Simple, CHC, and clearing-based multimodal genetic algorithms for QAP."""

from __future__ import annotations

import math

import numpy as np
from numpy.random import Generator

from .qap import QAPInstance
from .results import HistoryPoint, OptimizationResult


def order_crossover(parent_a: np.ndarray, parent_b: np.ndarray, generator: Generator) -> np.ndarray:
    """Create a permutation child with order crossover (OX)."""

    size = len(parent_a)
    start, end = sorted(generator.choice(size, size=2, replace=False).tolist())
    child = np.full(size, -1, dtype=np.int64)
    child[start:end] = parent_a[start:end]
    remaining = [
        int(gene) for gene in np.concatenate((parent_b[end:], parent_b[:end])) if gene not in child
    ]
    positions = list(range(end, size)) + list(range(0, start))
    child[positions] = remaining
    return child


def cyclic_sublist_mutation(
    solution: np.ndarray,
    mutation_size: int,
    generator: Generator,
) -> np.ndarray:
    """Randomly reorder a fixed-size circular segment."""

    child = solution.copy()
    width = min(len(child), max(2, mutation_size))
    start = int(generator.integers(len(child)))
    indices = (start + np.arange(width)) % len(child)
    child[indices] = generator.permutation(child[indices])
    return child


def hamming_distance(first: np.ndarray, second: np.ndarray) -> int:
    return int(np.count_nonzero(first != second))


def _tournament(
    population: list[np.ndarray],
    scores: np.ndarray,
    size: int,
    generator: Generator,
) -> np.ndarray:
    width = min(len(population), max(2, size))
    selected = generator.choice(len(population), size=width, replace=False)
    winner = int(selected[np.argmin(scores[selected])])
    return population[winner]


def _evaluate_population(
    instance: QAPInstance,
    population: list[np.ndarray],
) -> np.ndarray:
    return np.asarray([instance.cost(solution) for solution in population], dtype=np.float64)


def simple_genetic_algorithm(
    instance: QAPInstance,
    *,
    population_size: int = 190,
    generations: int = 1000,
    crossover_probability: float = 0.9,
    mutation_fraction: float = 0.1,
    elite_count: int = 1,
    seed: int | None = None,
) -> OptimizationResult:
    """Generational GA with tournament selection, OX, mutation, and elitism."""

    if population_size < 2 or generations < 0:
        raise ValueError("population_size must be at least 2 and generations non-negative")
    if not 0 <= elite_count < population_size:
        raise ValueError("elite_count must be between 0 and population_size - 1")
    generator = np.random.default_rng(seed)
    population = [generator.permutation(instance.size) for _ in range(population_size)]
    scores = _evaluate_population(instance, population)
    evaluations = population_size
    best_index = int(np.argmin(scores))
    best_solution = population[best_index].copy()
    best_cost = float(scores[best_index])
    history = [HistoryPoint(evaluations, best_cost)]
    tournament_size = max(2, int(round(population_size * 0.1)))
    mutation_size = max(2, int(round(instance.size * mutation_fraction)))

    for _ in range(generations):
        elite_indices = np.argsort(scores)[:elite_count]
        next_population = [population[int(index)].copy() for index in elite_indices]
        while len(next_population) < population_size:
            parent_a = _tournament(population, scores, tournament_size, generator)
            parent_b = _tournament(population, scores, tournament_size, generator)
            if generator.random() < crossover_probability:
                child = order_crossover(parent_a, parent_b, generator)
            else:
                child = cyclic_sublist_mutation(parent_a, mutation_size, generator)
            next_population.append(child)

        population = next_population
        scores = _evaluate_population(instance, population)
        evaluations += population_size
        candidate_index = int(np.argmin(scores))
        if scores[candidate_index] < best_cost:
            best_solution = population[candidate_index].copy()
            best_cost = float(scores[candidate_index])
            history.append(HistoryPoint(evaluations, best_cost))

    return OptimizationResult(
        solution=best_solution,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=len(history) - 1,
        history=tuple(history),
        metadata={
            "population_size": population_size,
            "generations": generations,
            "tournament_size": tournament_size,
            "mutation_size": mutation_size,
        },
    )


def chc_genetic_algorithm(
    instance: QAPInstance,
    *,
    population_size: int = 190,
    max_evaluations: int = 50_000,
    seed: int | None = None,
) -> OptimizationResult:
    """Permutation CHC with incest prevention, elitist survival, and restarts."""

    if population_size < 2 or max_evaluations < population_size:
        raise ValueError("The evaluation budget must cover the initial population.")
    generator = np.random.default_rng(seed)
    population = [generator.permutation(instance.size) for _ in range(population_size)]
    scores = _evaluate_population(instance, population)
    evaluations = population_size
    best_index = int(np.argmin(scores))
    best_solution = population[best_index].copy()
    best_cost = float(scores[best_index])
    threshold = instance.size // 4
    restarts = 0
    generation = 0
    history = [HistoryPoint(evaluations, best_cost)]

    while evaluations < max_evaluations:
        generation += 1
        order = generator.permutation(population_size)
        children: list[np.ndarray] = []
        for left in range(0, population_size - 1, 2):
            parent_a = population[int(order[left])]
            parent_b = population[int(order[left + 1])]
            if hamming_distance(parent_a, parent_b) <= threshold:
                continue
            for first, second in ((parent_a, parent_b), (parent_b, parent_a)):
                if evaluations + len(children) >= max_evaluations:
                    break
                children.append(order_crossover(first, second, generator))

        inserted = False
        if children:
            child_scores = _evaluate_population(instance, children)
            evaluations += len(children)
            combined_population = population + children
            combined_scores = np.concatenate((scores, child_scores))
            survivors = np.argsort(combined_scores)[:population_size]
            inserted = any(int(index) >= population_size for index in survivors)
            population = [combined_population[int(index)].copy() for index in survivors]
            scores = combined_scores[survivors]
            candidate_index = int(np.argmin(scores))
            if scores[candidate_index] < best_cost:
                best_solution = population[candidate_index].copy()
                best_cost = float(scores[candidate_index])
                history.append(HistoryPoint(evaluations, best_cost))

        if not inserted:
            threshold -= 1

        if threshold <= 0:
            remaining = max_evaluations - evaluations
            if remaining < population_size - 1:
                break
            population = [best_solution.copy()] + [
                generator.permutation(instance.size) for _ in range(population_size - 1)
            ]
            random_scores = _evaluate_population(instance, population[1:])
            scores = np.concatenate(([best_cost], random_scores))
            evaluations += population_size - 1
            threshold = instance.size // 4
            restarts += 1
            history.append(HistoryPoint(evaluations, best_cost, "restart"))

        if not children and threshold > 0:
            history.append(HistoryPoint(evaluations, best_cost, "threshold reduced"))

    return OptimizationResult(
        solution=best_solution,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=generation,
        history=tuple(history),
        metadata={"restarts": restarts, "final_threshold": threshold},
    )


def _clearing_scores(
    population: list[np.ndarray],
    raw_scores: np.ndarray,
    radius: int,
    capacity: int,
) -> np.ndarray:
    adjusted = raw_scores.copy()
    leaders: list[tuple[int, int]] = []
    for index_raw in np.argsort(raw_scores):
        index = int(index_raw)
        matched_leader: int | None = None
        for leader_position, (leader_index, members) in enumerate(leaders):
            if hamming_distance(population[index], population[leader_index]) <= radius:
                matched_leader = leader_position
                if members >= capacity:
                    adjusted[index] = math.inf
                else:
                    leaders[leader_position] = (leader_index, members + 1)
                break
        if matched_leader is None:
            leaders.append((index, 1))
    return adjusted


def multimodal_genetic_algorithm(
    instance: QAPInstance,
    *,
    population_size: int = 190,
    generations: int = 1000,
    crossover_probability: float = 0.9,
    mutation_fraction: float = 0.1,
    radius: int = 3,
    niche_capacity: int = 1,
    elite_count: int = 1,
    seed: int | None = None,
) -> OptimizationResult:
    """Generational GA that preserves multiple niches through fitness clearing."""

    if radius < 0 or niche_capacity < 1:
        raise ValueError("radius must be non-negative and niche_capacity positive")
    generator = np.random.default_rng(seed)
    population = [generator.permutation(instance.size) for _ in range(population_size)]
    raw_scores = _evaluate_population(instance, population)
    selection_scores = _clearing_scores(population, raw_scores, radius, niche_capacity)
    evaluations = population_size
    best_index = int(np.argmin(raw_scores))
    best_solution = population[best_index].copy()
    best_cost = float(raw_scores[best_index])
    history = [HistoryPoint(evaluations, best_cost)]
    tournament_size = max(2, int(round(population_size * 0.1)))
    mutation_size = max(2, int(round(instance.size * mutation_fraction)))

    for _ in range(generations):
        elite_indices = np.argsort(raw_scores)[:elite_count]
        next_population = [population[int(index)].copy() for index in elite_indices]
        while len(next_population) < population_size:
            parent_a = _tournament(population, selection_scores, tournament_size, generator)
            parent_b = _tournament(population, selection_scores, tournament_size, generator)
            if generator.random() < crossover_probability:
                child = order_crossover(parent_a, parent_b, generator)
            else:
                child = cyclic_sublist_mutation(parent_a, mutation_size, generator)
            next_population.append(child)

        population = next_population
        raw_scores = _evaluate_population(instance, population)
        evaluations += population_size
        selection_scores = _clearing_scores(population, raw_scores, radius, niche_capacity)
        candidate_index = int(np.argmin(raw_scores))
        if raw_scores[candidate_index] < best_cost:
            best_solution = population[candidate_index].copy()
            best_cost = float(raw_scores[candidate_index])
            history.append(HistoryPoint(evaluations, best_cost))

    return OptimizationResult(
        solution=best_solution,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=len(history) - 1,
        history=tuple(history),
        metadata={
            "population_size": population_size,
            "generations": generations,
            "radius": radius,
            "niche_capacity": niche_capacity,
        },
    )
