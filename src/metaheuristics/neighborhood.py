"""Greedy, random, local, simulated annealing, and tabu search for QAP."""

from __future__ import annotations

import math
from collections import deque
from itertools import combinations

import numpy as np
from numpy.random import Generator

from .qap import QAPInstance
from .results import HistoryPoint, OptimizationResult


def _rng(seed: int | None) -> Generator:
    return np.random.default_rng(seed)


def greedy_qap(instance: QAPInstance) -> OptimizationResult:
    """Match high-flow facilities with centrally located sites."""

    flow_potential = instance.flows.sum(axis=1)
    distance_potential = instance.distances.sum(axis=1)
    facilities = np.argsort(-flow_potential)
    locations = np.argsort(distance_potential)
    solution = np.empty(instance.size, dtype=np.int64)
    solution[facilities] = locations
    cost = instance.cost(solution)
    return OptimizationResult(
        solution=solution,
        cost=cost,
        evaluations=1,
        best_iteration=0,
        history=(HistoryPoint(1, cost),),
    )


def random_search(
    instance: QAPInstance,
    *,
    iterations: int | None = None,
    seed: int | None = None,
) -> OptimizationResult:
    """Sample independent random permutations and retain the best one."""

    generator = _rng(seed)
    budget = iterations if iterations is not None else 1000 * instance.size
    if budget < 1:
        raise ValueError("iterations must be positive")

    best_solution: np.ndarray | None = None
    best_cost = math.inf
    best_iteration = 0
    history: list[HistoryPoint] = []
    for iteration in range(1, budget + 1):
        solution = generator.permutation(instance.size)
        cost = instance.cost(solution)
        if cost < best_cost:
            best_solution = solution.copy()
            best_cost = cost
            best_iteration = iteration
            history.append(HistoryPoint(iteration, cost))

    assert best_solution is not None
    return OptimizationResult(
        solution=best_solution,
        cost=best_cost,
        evaluations=budget,
        best_iteration=best_iteration,
        history=tuple(history),
    )


def local_search(
    instance: QAPInstance,
    initial_solution: np.ndarray | list[int] | None = None,
    *,
    strategy: str = "first",
    shuffle_neighborhood: bool = True,
    seed: int | None = None,
) -> OptimizationResult:
    """Run first- or best-improvement 2-opt local search."""

    if strategy not in {"first", "best"}:
        raise ValueError("strategy must be 'first' or 'best'")
    generator = _rng(seed)
    current = (
        generator.permutation(instance.size)
        if initial_solution is None
        else instance.validate(initial_solution).copy()
    )
    current_cost = instance.cost(current)
    evaluations = 1
    iteration = 0
    history = [HistoryPoint(evaluations, current_cost)]
    moves = np.asarray(list(combinations(range(instance.size), 2)), dtype=np.int64)

    while True:
        iteration += 1
        order = generator.permutation(len(moves)) if shuffle_neighborhood else np.arange(len(moves))
        selected_move: tuple[int, int] | None = None
        selected_cost = current_cost

        for move_index in order:
            r, s = (int(value) for value in moves[move_index])
            candidate_cost = instance.swap_cost(current, current_cost, r, s)
            evaluations += 1
            if candidate_cost < selected_cost:
                selected_move = (r, s)
                selected_cost = candidate_cost
                if strategy == "first":
                    break

        if selected_move is None:
            break
        r, s = selected_move
        current[r], current[s] = current[s], current[r]
        current_cost = selected_cost
        history.append(HistoryPoint(evaluations, current_cost))

    return OptimizationResult(
        solution=current,
        cost=current_cost,
        evaluations=evaluations,
        best_iteration=iteration - 1,
        history=tuple(history),
        metadata={"strategy": strategy},
    )


def simulated_annealing(
    instance: QAPInstance,
    *,
    max_coolings: int | None = None,
    max_generated: int = 40,
    max_accepted: int = 5,
    mu: float = 0.3,
    phi: float = 0.3,
    seed: int | None = None,
) -> OptimizationResult:
    """Simulated annealing with the Cauchy cooling schedule from Practice 1."""

    if not (0 < phi < 1) or mu <= 0:
        raise ValueError("phi must be in (0, 1) and mu must be positive")
    generator = _rng(seed)
    coolings = max_coolings if max_coolings is not None else 50 * instance.size
    current = generator.permutation(instance.size)
    current_cost = instance.cost(current)
    evaluations = 1
    best = current.copy()
    best_cost = current_cost
    best_iteration = 0
    initial_temperature = -mu * current_cost / math.log(phi)
    history = [HistoryPoint(evaluations, best_cost)]

    for cooling in range(coolings):
        temperature = initial_temperature / (1 + cooling)
        accepted = 0
        generated = 0
        while accepted < max_accepted and generated < max_generated:
            r, s = generator.choice(instance.size, size=2, replace=False)
            r, s = int(r), int(s)
            candidate_cost = instance.swap_cost(current, current_cost, r, s)
            evaluations += 1
            generated += 1
            difference = candidate_cost - current_cost
            if difference < 0 or generator.random() < math.exp(-difference / temperature):
                current[r], current[s] = current[s], current[r]
                current_cost = candidate_cost
                accepted += 1
                if current_cost < best_cost:
                    best = current.copy()
                    best_cost = current_cost
                    best_iteration = cooling + 1
                    history.append(HistoryPoint(evaluations, best_cost))

    return OptimizationResult(
        solution=best,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=best_iteration,
        history=tuple(history),
        metadata={"initial_temperature": initial_temperature},
    )


def tabu_search(
    instance: QAPInstance,
    *,
    max_iterations: int | None = None,
    sampled_neighbors: int = 40,
    seed: int | None = None,
) -> OptimizationResult:
    """Tabu search with aspiration, four restarts, and adaptive tenure."""

    generator = _rng(seed)
    iterations = max_iterations if max_iterations is not None else 40 * instance.size
    current = generator.permutation(instance.size)
    current_cost = instance.cost(current)
    evaluations = 1
    best = current.copy()
    best_cost = current_cost
    best_iteration = 0
    tenure = max(1, instance.size // 2)
    tabu_moves: deque[tuple[int, int]] = deque()
    all_moves = np.asarray(list(combinations(range(instance.size), 2)), dtype=np.int64)
    restart_points = {8 * instance.size * step for step in range(1, 5)}
    history = [HistoryPoint(evaluations, best_cost)]

    for iteration in range(1, iterations + 1):
        sample_size = min(sampled_neighbors, len(all_moves))
        sample = all_moves[generator.choice(len(all_moves), size=sample_size, replace=False)]
        candidates: list[tuple[int, int, int, bool]] = []
        for r_raw, s_raw in sample:
            r, s = int(r_raw), int(s_raw)
            candidate_cost = instance.swap_cost(current, current_cost, r, s)
            evaluations += 1
            admissible = (r, s) not in tabu_moves or candidate_cost < best_cost
            candidates.append((candidate_cost, r, s, admissible))

        admissible_candidates = [item for item in candidates if item[3]]
        pool = admissible_candidates if admissible_candidates else candidates
        candidate_cost, r, s, _ = min(pool, key=lambda item: item[0])
        current[r], current[s] = current[s], current[r]
        current_cost = candidate_cost
        tabu_moves.append((r, s))
        while len(tabu_moves) > tenure:
            tabu_moves.popleft()

        if current_cost < best_cost:
            best = current.copy()
            best_cost = current_cost
            best_iteration = iteration
            history.append(HistoryPoint(evaluations, best_cost))

        if iteration in restart_points and iteration < iterations:
            draw = generator.random()
            if draw < 0.25:
                current = generator.permutation(instance.size)
                restart_kind = "random restart"
            elif draw < 0.75:
                current = greedy_qap(instance).solution.copy()
                restart_kind = "greedy restart"
            else:
                current = best.copy()
                restart_kind = "best restart"
            current_cost = instance.cost(current)
            evaluations += 1
            factor = 1.5 if generator.random() < 0.5 else 0.5
            tenure = max(1, int(round(tenure * factor)))
            while len(tabu_moves) > tenure:
                tabu_moves.popleft()
            history.append(HistoryPoint(evaluations, best_cost, restart_kind))

    return OptimizationResult(
        solution=best,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=best_iteration,
        history=tuple(history),
        metadata={"final_tabu_tenure": tenure},
    )
