import enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ToolPermission(str, enum.Enum):
    REPO_READ = "repo.read"
    REPO_BRANCH_WRITE = "repo.branch_write"
    REPO_COMMIT = "repo.commit"
    TEST_RUN = "test.run"
    BUILD_RUN = "build.run"
    PR_CREATE = "pr.create"
    PROD_DEPLOY = "deploy.production"

class ToolCapabilityGateway:
    """
    Tool Capability Gateway enforcing RBAC tool permissions.
    Interprets all untrusted model calls and blocks unauthorized execution.
    Disables arbitrary code_interpreter execution by default.
    """
    def __init__(self, allowed_permissions: Optional[List[ToolPermission]] = None):
        if allowed_permissions is None:
            # Default initial autonomy: Read, branch write, commit, test, build, PR create (No prod deploy)
            self.allowed_permissions = [
                ToolPermission.REPO_READ,
                ToolPermission.REPO_BRANCH_WRITE,
                ToolPermission.REPO_COMMIT,
                ToolPermission.TEST_RUN,
                ToolPermission.BUILD_RUN,
                ToolPermission.PR_CREATE
            ]
        else:
            self.allowed_permissions = allowed_permissions

    def validate_tool_execution(self, tool_name: str, required_permission: ToolPermission) -> bool:
        if tool_name == "code_interpreter":
            # Disabled by default for security
            return False
        return required_permission in self.allowed_permissions
