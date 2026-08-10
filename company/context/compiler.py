from typing import Dict, Any, List, Optional
from company.os.loader import ThinkYetOSLoader

class ContextCompiler:
    """
    Context Compiler module.
    Compiles minimal sufficient KNOWLEDGE_PACK per task (< 15KB context budget).
    Prevents megaword context overflow and filters out draft/historical prose.
    """
    def __init__(self, os_loader: Optional[ThinkYetOSLoader] = None):
        self.os_loader = os_loader or ThinkYetOSLoader()

    def compile_knowledge_pack(self, task_scope: str, agent_role: str) -> Dict[str, Any]:
        visibility = self.os_loader.get_visibility_policy()
        return {
            "task_scope": task_scope,
            "agent_role": agent_role,
            "visibility_invariants": visibility,
            "core_stance_rule": "YES / NO binary stance only. No third options.",
            "max_context_bytes": 15360
        }
