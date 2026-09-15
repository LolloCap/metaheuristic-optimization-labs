"""Shared command-line helpers for QAP experiments."""

from __future__ import annotations

from pathlib import Path
from statistics import fmean, pstdev

from metaheuristics.qap import QAPInstance, read_qap_instance
from metaheuristics.results import OptimizationResult

DATASET_NAMES = ("tai25b", "sko90", "tai150b")


def load_instance(data_directory: str | Path, name: str) -> QAPInstance:
    path = Path(data_directory) / f"{name}.dat"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Follow data/README.md to obtain the QAPLIB files."
        )
    return read_qap_instance(path)


def print_summary(name: str, results: list[OptimizationResult]) -> None:
    costs = [float(result.cost) for result in results]
    evaluations = [result.evaluations for result in results]
    print(
        f"{name:<24} best={min(costs):.6g}  mean={fmean(costs):.6g}  "
        f"worst={max(costs):.6g}  std={pstdev(costs):.6g}  "
        f"mean_evaluations={fmean(evaluations):.1f}"
    )
