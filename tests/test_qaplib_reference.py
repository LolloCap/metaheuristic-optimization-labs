from __future__ import annotations

from pathlib import Path

import pytest

from metaheuristics.qap import read_qap_instance, read_qap_solution

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "qaplib"


@pytest.mark.parametrize("name", ["tai25b", "sko90", "tai150b"])
def test_published_qaplib_solution_cost(name: str) -> None:
    instance_path = DATA_DIRECTORY / f"{name}.dat"
    solution_path = DATA_DIRECTORY / f"{name}.sln"
    if not instance_path.exists() or not solution_path.exists():
        pytest.skip("Download QAPLIB data with scripts/fetch_qaplib.py")
    instance = read_qap_instance(instance_path)
    published_cost, permutation = read_qap_solution(solution_path)
    assert instance.cost(permutation) == published_cost
