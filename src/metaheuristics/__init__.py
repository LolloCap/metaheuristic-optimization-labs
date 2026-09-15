"""Metaheuristic algorithms developed for the course laboratory series."""

from .qap import QAPInstance, read_qap_instance, read_qap_solution
from .results import HistoryPoint, OptimizationResult

__all__ = [
    "HistoryPoint",
    "OptimizationResult",
    "QAPInstance",
    "read_qap_instance",
    "read_qap_solution",
]
