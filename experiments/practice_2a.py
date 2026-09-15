"""Practice 2a: GRASP, ILS, and VNS on QAP."""

from __future__ import annotations

import argparse

from metaheuristics.multistart import grasp, iterated_local_search, variable_neighborhood_search
from metaheuristics.neighborhood import greedy_qap, local_search

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
        print_summary("Greedy", [greedy_qap(instance)])
        print_summary(
            "First-improvement LS",
            [local_search(instance, strategy="first", seed=seed) for seed in range(5)],
        )
        print_summary(
            "GRASP",
            [grasp(instance, constructions=2 if arguments.quick else 5, seed=10)],
        )
        print_summary(
            "ILS",
            [iterated_local_search(instance, local_searches=3 if arguments.quick else 10, seed=20)],
        )
        vns_searches = 3 if arguments.quick else 10
        print_summary(
            "VNS",
            [
                variable_neighborhood_search(instance, max_local_searches=vns_searches, seed=seed)
                for seed in range(5)
            ],
        )


if __name__ == "__main__":
    main()
