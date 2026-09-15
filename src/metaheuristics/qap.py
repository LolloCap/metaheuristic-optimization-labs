"""Quadratic Assignment Problem data model and objective utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

IntArray = NDArray[np.int64]


@dataclass(frozen=True)
class QAPInstance:
    """A QAPLIB instance with a flow matrix and a distance matrix.

    A solution is a zero-based permutation ``p``. Facility ``i`` is assigned to
    location ``p[i]`` and the objective is ``sum(A[i,j] * B[p[i],p[j]])``.
    """

    flows: IntArray
    distances: IntArray
    name: str = "qap"

    def __post_init__(self) -> None:
        if self.flows.ndim != 2 or self.flows.shape[0] != self.flows.shape[1]:
            raise ValueError("The flow matrix must be square.")
        if self.distances.shape != self.flows.shape:
            raise ValueError("Flow and distance matrices must have equal shape.")

    @property
    def size(self) -> int:
        return int(self.flows.shape[0])

    def validate(self, permutation: NDArray[np.integer] | list[int]) -> IntArray:
        candidate = np.asarray(permutation, dtype=np.int64)
        if candidate.shape != (self.size,):
            raise ValueError(f"Expected a permutation of length {self.size}.")
        if not np.array_equal(np.sort(candidate), np.arange(self.size)):
            raise ValueError("A QAP solution must be a zero-based permutation.")
        return candidate

    def cost(self, permutation: NDArray[np.integer] | list[int]) -> int:
        candidate = self.validate(permutation)
        permuted_distances = self.distances[candidate][:, candidate]
        return int(np.sum(self.flows * permuted_distances, dtype=np.int64))

    def swap_cost(
        self,
        permutation: NDArray[np.integer] | list[int],
        current_cost: int,
        first: int,
        second: int,
    ) -> int:
        """Evaluate a 2-opt swap in O(n) from a known current objective value."""

        candidate = self.validate(permutation)
        if first == second:
            return int(current_cost)
        if not (0 <= first < self.size and 0 <= second < self.size):
            raise IndexError("Swap positions must be valid facility indices.")

        r, s = first, second
        a, b = self.flows, self.distances
        delta = 0
        for k in range(self.size):
            if k == r or k == s:
                continue
            delta += (a[r, k] - a[s, k]) * (
                b[candidate[s], candidate[k]] - b[candidate[r], candidate[k]]
            )
            delta += (a[k, r] - a[k, s]) * (
                b[candidate[k], candidate[s]] - b[candidate[k], candidate[r]]
            )
        delta += (a[r, r] - a[s, s]) * (
            b[candidate[s], candidate[s]] - b[candidate[r], candidate[r]]
        )
        delta += (a[r, s] - a[s, r]) * (
            b[candidate[s], candidate[r]] - b[candidate[r], candidate[s]]
        )
        return int(current_cost + delta)


def read_qap_instance(path: str | Path) -> QAPInstance:
    """Read the plain-text QAPLIB format: n, matrix A, matrix B."""

    source = Path(path)
    tokens = [int(token) for token in source.read_text(encoding="utf-8").split()]
    if not tokens:
        raise ValueError(f"Empty QAP instance: {source}")
    size = tokens[0]
    expected = 1 + 2 * size * size
    if len(tokens) != expected:
        raise ValueError(f"{source.name} contains {len(tokens)} integers; expected {expected}.")
    split = 1 + size * size
    flows = np.asarray(tokens[1:split], dtype=np.int64).reshape(size, size)
    distances = np.asarray(tokens[split:], dtype=np.int64).reshape(size, size)
    return QAPInstance(flows=flows, distances=distances, name=source.stem)


def read_qap_solution(path: str | Path) -> tuple[int, IntArray]:
    """Read a QAPLIB solution file and convert its permutation to zero-based."""

    source = Path(path)
    tokens = [int(token) for token in source.read_text(encoding="utf-8").split()]
    if len(tokens) < 2:
        raise ValueError(f"Invalid QAP solution file: {source}")
    size, objective = tokens[:2]
    permutation = np.asarray(tokens[2:], dtype=np.int64) - 1
    if permutation.shape != (size,) or not np.array_equal(np.sort(permutation), np.arange(size)):
        raise ValueError(f"Invalid permutation in {source.name}.")
    return objective, permutation
