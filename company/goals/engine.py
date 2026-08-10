from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class Milestone(BaseModel):
    id: str
    title: str
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED
    progress_percentage: int = 0

class GoalContract(BaseModel):
    goal_id: str
    title: str
    description: str
    owner_agent: str
    priority: str = "HIGH"  # HIGH, MEDIUM, LOW
    status: str = "ACTIVE"  # ACTIVE, PAUSED, COMPLETED
    progress_percentage: int = 0
    milestones: List[Milestone] = Field(default_factory=list)

class GoalEngine:
    """
    Goal Engine module for creating, decomposing, and tracking Founder Goals into Milestones and Tasks.
    """
    def __init__(self):
        self.goals: Dict[str, GoalContract] = {}
        self._init_default_goals()

    def _init_default_goals(self):
        g1 = GoalContract(
            goal_id="GOAL-01",
            title="Complete Comments System",
            description="Audit, refactor, and implement the complete Comments module adhering to ThinkYet OS Visibility Invariants (A3).",
            owner_agent="Engineering Agent",
            priority="HIGH",
            status="ACTIVE",
            progress_percentage=82,
            milestones=[
                Milestone(id="M1", title="Audit server-side comment authorization", status="COMPLETED", progress_percentage=100),
                Milestone(id="M2", title="Testing cross-surface visibility gates", status="IN_PROGRESS", progress_percentage=75),
                Milestone(id="M3", title="Final regression & performance benchmark", status="PENDING", progress_percentage=0)
            ]
        )
        g2 = GoalContract(
            goal_id="GOAL-02",
            title="Redesign Feed Card & Design System Reconciliation",
            description="Reconcile ThinkYet Design System v1 with current Next.js feed components.",
            owner_agent="Design Agent",
            priority="MEDIUM",
            status="ACTIVE",
            progress_percentage=65,
            milestones=[
                Milestone(id="M1", title="Tokens & Color Tokens export", status="COMPLETED", progress_percentage=100),
                Milestone(id="M2", title="PostCard component alignment", status="IN_PROGRESS", progress_percentage=50)
            ]
        )
        self.goals[g1.goal_id] = g1
        self.goals[g2.goal_id] = g2

    def create_goal(self, goal: GoalContract) -> GoalContract:
        self.goals[goal.goal_id] = goal
        return goal

    def get_all_goals(self) -> List[Dict[str, Any]]:
        return [g.dict() for g in self.goals.values()]
