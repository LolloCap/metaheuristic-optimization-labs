from __future__ import annotations

from itertools import combinations

import numpy as np

from metaheuristics.qap import QAPInstance, read_qap_instance


def test_cost_matches_direct_sum(small_qap: QAPInstance) -> None:
    permutation = np.asarray([2, 0, 4, 1, 3])
    direct = sum(
        int(small_qap.flows[i, j]) * int(small_qap.distances[permutation[i], permutation[j]])
        for i in range(small_qap.size)
        for j in range(small_qap.size)
    )
    assert small_qap.cost(permutation) == direct


def test_swap_delta_matches_full_recomputation(small_qap: QAPInstance) -> None:
    generator = np.random.default_rng(42)
    for _ in range(20):
        permutation = generator.permutation(small_qap.size)
        current = small_qap.cost(permutation)
        for first, second in combinations(range(small_qap.size), 2):
            swapped = permutation.copy()
            swapped[first], swapped[second] = swapped[second], swapped[first]
            assert small_qap.swap_cost(permutation, current, first, second) == small_qap.cost(
                swapped
            )


def test_qaplib_reader(tmp_path) -> None:
    source = tmp_path / "tiny.dat"
    source.write_text("2\n0 3\n3 0\n0 2\n2 0\n", encoding="utf-8")
    instance = read_qap_instance(source)
    assert instance.size == 2
    assert instance.cost([0, 1]) == 12
