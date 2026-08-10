import os
import yaml
from typing import Dict, Any, Optional

class ThinkYetOSLoader:
    """
    OS Loader module for loading canonical machine-readable artifacts and active ThinkYet OS rules.
    Does not reload or re-parse large raw markdown files on every request.
    """
    def __init__(self, thinkyet_dir: str = "/Users/mac/Downloads/thinkyet"):
        self.thinkyet_dir = thinkyet_dir
        self._authority_map: Optional[Dict[str, Any]] = None
        self._agent_routing: Optional[Dict[str, Any]] = None
        self._risk_register: Optional[Dict[str, Any]] = None
        self._conflict_register: Optional[Dict[str, Any]] = None
        self.reload_all()

    def _load_yaml_file(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.thinkyet_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def reload_all(self):
        self._authority_map = self._load_yaml_file("AUTHORITY_MAP.yaml")
        self._agent_routing = self._load_yaml_file("AGENT_ROUTING.yaml")
        self._risk_register = self._load_yaml_file("RISK_REGISTER.yaml")
        self._conflict_register = self._load_yaml_file("CONFLICT_REGISTER.yaml")

    def get_authority_map(self) -> Dict[str, Any]:
        return self._authority_map or {}

    def get_agent_routing(self) -> Dict[str, Any]:
        return self._agent_routing or {}

    def get_risk_register(self) -> Dict[str, Any]:
        return self._risk_register or {}

    def get_conflict_register(self) -> Dict[str, Any]:
        return self._conflict_register or {}

    def get_visibility_policy(self) -> Dict[str, str]:
        return {
            "feed_visibility": "HIDE_YES_NO_PERCENTAGE_AND_GATED_COMMENTS",
            "detail_visibility_before_stance": "HIDE_GATED_COMMENTS_AND_PERCENTAGE",
            "detail_visibility_after_stance": "UNLOCK_CANONICAL_RESULTS_AND_DISCUSSION"
        }
