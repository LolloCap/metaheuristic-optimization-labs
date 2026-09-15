"""Shared result objects for discrete and continuous optimizers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


def _json_value(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


@dataclass(frozen=True)
class HistoryPoint:
    """Best-known objective value at a point in an optimization run."""

    evaluations: int
    best_cost: float
    event: str | None = None


@dataclass(frozen=True)
class OptimizationResult:
    """Common return type used by every optimizer in the repository."""

    solution: np.ndarray
    cost: float
    evaluations: int
    best_iteration: int | None = None
    history: tuple[HistoryPoint, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "solution": self.solution.tolist(),
            "cost": float(self.cost),
            "evaluations": int(self.evaluations),
            "best_iteration": self.best_iteration,
            "history": [
                {
                    "evaluations": point.evaluations,
                    "best_cost": float(point.best_cost),
                    "event": point.event,
                }
                for point in self.history
            ],
            "metadata": _json_value(self.metadata),
        }
