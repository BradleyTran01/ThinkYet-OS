import enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TaskState(str, enum.Enum):
    QUEUED = "QUEUED"
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    REVIEW = "REVIEW"
    FIXING = "FIXING"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class TaskContract(BaseModel):
    task_id: str
    goal_id: str
    objective: str
    scope: str
    owner_agent: str
    dependencies: List[str] = Field(default_factory=list)
    status: TaskState = TaskState.QUEUED
    max_retries: int = 3
    retries_count: int = 0
    evidence: Optional[Dict[str, Any]] = None

class TaskEngine:
    """
    Task Engine module managing the 10-state task lifecycle and evidence tracking.
    """
    def __init__(self):
        self.tasks: Dict[str, TaskContract] = {}

    def create_task(self, task: TaskContract) -> TaskContract:
        self.tasks[task.task_id] = task
        return task

    def transition_state(self, task_id: str, new_state: TaskState) -> TaskContract:
        if task_id in self.tasks:
            self.tasks[task_id].status = new_state
            return self.tasks[task_id]
        raise ValueError(f"Task {task_id} not found")
