"""Final project: PSO versus best-neighbor local search on Rastrigin."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import fmean, pstdev

from metaheuristics.pso import (
    local_search_rastrigin,
    particle_swarm_optimization,
    save_trajectory_plots,
)

from .common import print_summary


def write_results(output_directory: Path, pso_results, local_results) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    with (output_directory / "runs.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["algorithm", "run", "seed", "cost", "evaluations", "x1", "x2"])
        for algorithm, results in (("PSO", pso_results), ("Local Search", local_results)):
            for seed, result in enumerate(results):
                writer.writerow(
                    [
                        algorithm,
                        seed + 1,
                        seed,
                        f"{result.cost:.12g}",
                        result.evaluations,
                        f"{result.solution[0]:.12g}",
                        f"{result.solution[1]:.12g}",
                    ]
                )

    with (output_directory / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            ["algorithm", "best", "mean", "worst", "population_std", "mean_evaluations"]
        )
        for algorithm, results in (("PSO", pso_results), ("Local Search", local_results)):
            costs = [float(result.cost) for result in results]
            evaluations = [result.evaluations for result in results]
            writer.writerow(
                [
                    algorithm,
                    f"{min(costs):.12g}",
                    f"{fmean(costs):.12g}",
                    f"{max(costs):.12g}",
                    f"{pstdev(costs):.12g}",
                    f"{fmean(evaluations):.1f}",
                ]
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument(
        "--output-dir", type=Path, help="Save run tables and plots from the first PSO run."
    )
    arguments = parser.parse_args()

    pso_results = [
        particle_swarm_optimization(iterations=arguments.iterations, seed=seed)
        for seed in range(arguments.runs)
    ]
    local_results = [
        local_search_rastrigin(iterations=arguments.iterations, seed=seed)
        for seed in range(arguments.runs)
    ]
    print_summary("PSO", pso_results)
    print_summary("Local search", local_results)
    if arguments.output_dir:
        write_results(arguments.output_dir, pso_results, local_results)
        save_trajectory_plots(pso_results[0], arguments.output_dir)
        print(f"Saved tables and plots to {arguments.output_dir}")


if __name__ == "__main__":
    main()
