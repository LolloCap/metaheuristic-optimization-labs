"""Practice 2b: evolutionary algorithms on QAP."""

from __future__ import annotations

import argparse

from metaheuristics.evolutionary import (
    chc_genetic_algorithm,
    multimodal_genetic_algorithm,
    simple_genetic_algorithm,
)
from metaheuristics.neighborhood import greedy_qap

from .common import DATASET_NAMES, load_instance, print_summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/qaplib")
    parser.add_argument("--dataset", choices=DATASET_NAMES, action="append")
    parser.add_argument("--quick", action="store_true", help="Use shorter demonstration budgets.")
    arguments = parser.parse_args()
    seeds = [10_000_000 * value for value in (10, 20, 30, 40, 50)]
    population = 30 if arguments.quick else 190
    generations = 20 if arguments.quick else 1000
    chc_evaluations = 1_000 if arguments.quick else 50_000

    for dataset_name in arguments.dataset or DATASET_NAMES:
        instance = load_instance(arguments.data_dir, dataset_name)
        print(f"\n{dataset_name} (n={instance.size})")
        print_summary("Greedy", [greedy_qap(instance)])
        print_summary(
            "Simple GA",
            [
                simple_genetic_algorithm(
                    instance,
                    population_size=population,
                    generations=generations,
                    seed=seed,
                )
                for seed in seeds
            ],
        )
        print_summary(
            "CHC",
            [
                chc_genetic_algorithm(
                    instance,
                    population_size=population,
                    max_evaluations=chc_evaluations,
                    seed=seed,
                )
                for seed in seeds
            ],
        )
        print_summary(
            "Multimodal GA",
            [
                multimodal_genetic_algorithm(
                    instance,
                    population_size=population,
                    generations=generations,
                    seed=seed,
                )
                for seed in seeds
            ],
        )


if __name__ == "__main__":
    main()
