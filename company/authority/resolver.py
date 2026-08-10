from typing import Dict, Any, List

class AuthorityResolver:
    """
    Authority Resolver (A0-A7) for resolving conflicts between rules, candidate proposals, and code reality.
    Strictly enforces Machine Canonical Artifacts > Raw Historical Prose.
    Discards DRAFT, CANDIDATE, SUPERSEDED, HISTORICAL rules by default.
    """
    AUTHORITY_LEVELS = {
        "A0": "THINKYET_CONSTITUTION",
        "A1": "ACTIVE_FOUNDER_DECISIONS",
        "A2": "MACHINE_CANONICAL_ARTIFACTS",
        "A3": "ACTIVE_THINKYET_OS_SPECS",
        "A4": "CURRENT_REPOSITORY_REALITY",
        "A5": "APPROVED_DESIGN_SYSTEM",
        "A6": "HERMES_CURRENT_IMPLEMENTATION",
        "A7": "LEGACY_MATERIAL"
    }

    DISCARD_STATUSES = {"DRAFT", "CANDIDATE", "PROPOSED", "SUPERSEDED", "HISTORICAL", "REJECTED", "RETIRED"}

    def resolve_rule_priority(self, rule_a: Dict[str, Any], rule_b: Dict[str, Any]) -> Dict[str, Any]:
        level_a = rule_a.get("authority_level", "A7")
        level_b = rule_b.get("authority_level", "A7")
        
        # Check for discarded statuses
        if rule_a.get("status") in self.DISCARD_STATUSES:
            return rule_b
        if rule_b.get("status") in self.DISCARD_STATUSES:
            return rule_a

        if level_a < level_b:
            return rule_a
        return rule_b
