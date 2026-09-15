"""Practice 1: neighborhood- and trajectory-based search on QAP."""

from __future__ import annotations

import argparse

from metaheuristics.neighborhood import (
    greedy_qap,
    local_search,
    random_search,
    simulated_annealing,
    tabu_search,
)

from .common import DATASET_NAMES, load_instance, print_summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/qaplib")
    parser.add_argument("--dataset", choices=DATASET_NAMES, action="append")
    parser.add_argument("--quick", action="store_true", help="Use shorter demonstration budgets.")
    arguments = parser.parse_args()

    for dataset_name in arguments.dataset or DATASET_NAMES:
        instance = load_instance(arguments.data_dir, dataset_name)
        print(f"\n{dataset_name} (n={instance.size})")
        random_iterations = (20 if arguments.quick else 1000) * instance.size
        annealing_coolings = (2 if arguments.quick else 50) * instance.size
        tabu_iterations = (4 if arguments.quick else 40) * instance.size

        print_summary("Greedy", [greedy_qap(instance)])
        print_summary(
            "Random search",
            [random_search(instance, iterations=random_iterations, seed=seed) for seed in range(5)],
        )
        print_summary(
            "Best-improvement LS",
            [local_search(instance, strategy="best", seed=seed) for seed in range(5)],
        )
        print_summary(
            "Randomized first LS",
            [local_search(instance, strategy="first", seed=seed) for seed in range(5)],
        )
        print_summary(
            "Simulated annealing",
            [
                simulated_annealing(instance, max_coolings=annealing_coolings, seed=seed)
                for seed in range(5)
            ],
        )
        print_summary(
            "Tabu search",
            [
                tabu_search(instance, max_iterations=tabu_iterations, seed=seed)
                for seed in range(10)
            ],
        )


if __name__ == "__main__":
    main()
