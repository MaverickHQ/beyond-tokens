from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from services.core.transitions import Action

Plan = List[Action]


@dataclass(frozen=True)
class PlannerError:
    code: str
    message: str


@dataclass(frozen=True)
class PlannerRejection:
    rejected_step_index: int
    violations: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class PlannerResult:
    plan: Plan
    planner_name: str
    metadata: Dict[str, object] = field(default_factory=dict)
    error: Optional[PlannerError] = None
    rejection: Optional[PlannerRejection] = None