from __future__ import annotations

import numpy as np
import pytest

from metaheuristics.qap import QAPInstance


@pytest.fixture
def small_qap() -> QAPInstance:
    flows = np.asarray(
        [
            [0, 5, 2, 4, 1],
            [5, 0, 3, 0, 2],
            [2, 3, 0, 2, 4],
            [4, 0, 2, 0, 3],
            [1, 2, 4, 3, 0],
        ],
        dtype=np.int64,
    )
    distances = np.asarray(
        [
            [0, 1, 3, 4, 2],
            [1, 0, 2, 3, 4],
            [3, 2, 0, 2, 1],
            [4, 3, 2, 0, 2],
            [2, 4, 1, 2, 0],
        ],
        dtype=np.int64,
    )
    return QAPInstance(flows=flows, distances=distances, name="small")
