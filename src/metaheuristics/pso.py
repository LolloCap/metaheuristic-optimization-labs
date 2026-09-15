"""Particle Swarm Optimization and a local-search baseline for Rastrigin."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .results import HistoryPoint, OptimizationResult


def rastrigin(points: np.ndarray | list[float]) -> float | np.ndarray:
    """Evaluate the standard Rastrigin function with A = 10."""

    values = np.asarray(points, dtype=float)
    dimension = values.shape[-1]
    result = 10 * dimension + np.sum(values**2 - 10 * np.cos(2 * np.pi * values), axis=-1)
    return float(result) if np.ndim(result) == 0 else result


def particle_swarm_optimization(
    *,
    particles: int = 30,
    dimensions: int = 2,
    lower_bound: float = -5.12,
    upper_bound: float = 5.12,
    iterations: int = 100,
    inertia: float = 0.7,
    cognitive: float = 1.5,
    social: float = 1.5,
    neighborhood_radius: int = 2,
    seed: int | None = None,
) -> OptimizationResult:
    """Optimize Rastrigin with a local-best ring-topology PSO.

    Boundary violations are clipped and the corresponding velocity components
    are set to zero. A radius of two gives every particle four ring neighbors.
    """

    if particles < 2 or dimensions < 1 or iterations < 0:
        raise ValueError("particles and dimensions must be positive")
    if lower_bound >= upper_bound:
        raise ValueError("lower_bound must be smaller than upper_bound")
    generator = np.random.default_rng(seed)
    positions = generator.uniform(lower_bound, upper_bound, size=(particles, dimensions))
    velocities = np.zeros_like(positions)
    personal_best = positions.copy()
    personal_values = np.asarray(rastrigin(personal_best), dtype=float)
    evaluations = particles
    best_index = int(np.argmin(personal_values))
    best_cost = float(personal_values[best_index])
    best_position = personal_best[best_index].copy()
    best_iteration = 0
    history = [HistoryPoint(evaluations, best_cost)]
    trajectories = [positions.copy()]

    indices = np.arange(particles)
    for iteration in range(1, iterations + 1):
        local_best = np.empty_like(positions)
        for particle in range(particles):
            neighborhood = [
                indices[(particle + offset) % particles]
                for offset in range(-neighborhood_radius, neighborhood_radius + 1)
            ]
            neighborhood_values = personal_values[neighborhood]
            local_index = int(neighborhood[int(np.argmin(neighborhood_values))])
            local_best[particle] = personal_best[local_index]

        random_cognitive = generator.random((particles, dimensions))
        random_social = generator.random((particles, dimensions))
        velocities = (
            inertia * velocities
            + cognitive * random_cognitive * (personal_best - positions)
            + social * random_social * (local_best - positions)
        )
        proposed = positions + velocities
        outside = (proposed < lower_bound) | (proposed > upper_bound)
        positions = np.clip(proposed, lower_bound, upper_bound)
        velocities[outside] = 0.0
        values = np.asarray(rastrigin(positions), dtype=float)
        evaluations += particles
        improved = values < personal_values
        personal_best[improved] = positions[improved]
        personal_values[improved] = values[improved]
        candidate_index = int(np.argmin(personal_values))
        if personal_values[candidate_index] < best_cost:
            best_cost = float(personal_values[candidate_index])
            best_position = personal_best[candidate_index].copy()
            best_iteration = iteration
            history.append(HistoryPoint(evaluations, best_cost))
        trajectories.append(positions.copy())

    return OptimizationResult(
        solution=best_position,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=best_iteration,
        history=tuple(history),
        metadata={
            "particles": particles,
            "iterations": iterations,
            "trajectories": np.asarray(trajectories),
            "boundary_strategy": "clip and zero velocity",
        },
    )


def local_search_rastrigin(
    *,
    dimensions: int = 2,
    lower_bound: float = -5.12,
    upper_bound: float = 5.12,
    iterations: int = 100,
    neighbors: int = 10,
    step: float = 0.1,
    seed: int | None = None,
) -> OptimizationResult:
    """Best-neighbor local search used as the final-project baseline."""

    generator = np.random.default_rng(seed)
    point = generator.uniform(lower_bound, upper_bound, size=dimensions)
    best_cost = float(rastrigin(point))
    best_iteration = 0
    evaluations = 1
    history = [HistoryPoint(evaluations, best_cost)]

    for iteration in range(1, iterations + 1):
        candidates = point + generator.uniform(-step, step, size=(neighbors, dimensions))
        candidates = np.clip(candidates, lower_bound, upper_bound)
        values = np.asarray(rastrigin(candidates), dtype=float)
        evaluations += neighbors
        best_index = int(np.argmin(values))
        if values[best_index] < best_cost:
            point = candidates[best_index].copy()
            best_cost = float(values[best_index])
            best_iteration = iteration
            history.append(HistoryPoint(evaluations, best_cost))

    return OptimizationResult(
        solution=point,
        cost=best_cost,
        evaluations=evaluations,
        best_iteration=best_iteration,
        history=tuple(history),
        metadata={"neighbors": neighbors, "step": step},
    )


def save_trajectory_plots(
    result: OptimizationResult,
    output_directory: str | Path,
    *,
    lower_bound: float = -5.12,
    upper_bound: float = 5.12,
) -> tuple[Path, Path]:
    """Save two-dimensional and surface views of a two-dimensional PSO run."""

    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    trajectories = np.asarray(result.metadata["trajectories"])
    if trajectories.shape[-1] != 2:
        raise ValueError("Trajectory plots require a two-dimensional run.")
    destination = Path(output_directory)
    destination.mkdir(parents=True, exist_ok=True)
    path_2d = destination / "particle-trajectories-2d.png"
    path_3d = destination / "particle-trajectories-3d.png"

    figure, axis = plt.subplots(figsize=(8, 6))
    for particle in range(trajectories.shape[1]):
        axis.plot(
            trajectories[:, particle, 0],
            trajectories[:, particle, 1],
            color="#2563EB",
            alpha=0.18,
            linewidth=0.8,
        )
    axis.scatter(
        trajectories[0, :, 0],
        trajectories[0, :, 1],
        color="#F97316",
        s=18,
        alpha=0.8,
        label="Initial positions",
    )
    axis.scatter(
        trajectories[-1, :, 0],
        trajectories[-1, :, 1],
        color="#16A34A",
        s=18,
        alpha=0.8,
        label="Final positions",
    )
    axis.scatter([0], [0], color="black", marker="*", s=110, label="Global minimum")
    axis.set(xlabel="x1", ylabel="x2", title="PSO particle trajectories")
    axis.set_xlim(lower_bound, upper_bound)
    axis.set_ylim(lower_bound, upper_bound)
    axis.grid(alpha=0.2)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path_2d, dpi=180)
    plt.close(figure)

    grid = np.linspace(lower_bound, upper_bound, 120)
    grid_x, grid_y = np.meshgrid(grid, grid)
    grid_points = np.stack((grid_x, grid_y), axis=-1)
    grid_z = np.asarray(rastrigin(grid_points))
    figure = plt.figure(figsize=(10, 7))
    axis_3d = figure.add_subplot(111, projection="3d")
    axis_3d.plot_surface(grid_x, grid_y, grid_z, cmap="viridis", alpha=0.55)
    for particle in range(trajectories.shape[1]):
        path = trajectories[:, particle]
        axis_3d.plot(
            path[:, 0],
            path[:, 1],
            rastrigin(path),
            color="#DC2626",
            alpha=0.22,
            linewidth=0.7,
        )
    axis_3d.set(xlabel="x1", ylabel="x2", zlabel="f(x)", title="PSO on Rastrigin")
    figure.tight_layout()
    figure.savefig(path_3d, dpi=180)
    plt.close(figure)
    return path_2d, path_3d
