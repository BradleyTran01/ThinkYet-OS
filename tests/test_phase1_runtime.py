import unittest
from company.os.loader import ThinkYetOSLoader
from company.authority.resolver import AuthorityResolver
from company.tools.gateway import ToolCapabilityGateway, ToolPermission
from company.context.compiler import ContextCompiler
from company.tasks.engine import TaskEngine, TaskContract, TaskState

class TestPhase1ThinRuntime(unittest.TestCase):

    def test_os_loader(self):
        loader = ThinkYetOSLoader()
        visibility = loader.get_visibility_policy()
        self.assertIn("feed_visibility", visibility)
        self.assertEqual(visibility["feed_visibility"], "HIDE_YES_NO_PERCENTAGE_AND_GATED_COMMENTS")

    def test_authority_resolver(self):
        resolver = AuthorityResolver()
        rule_a = {"name": "Rule A", "authority_level": "A1", "status": "APPROVED"}
        rule_b = {"name": "Rule B", "authority_level": "A3", "status": "APPROVED"}
        resolved = resolver.resolve_rule_priority(rule_a, rule_b)
        self.assertEqual(resolved["name"], "Rule A")

    def test_tool_capability_gateway(self):
        gateway = ToolCapabilityGateway()
        # Reporead should be allowed
        self.assertTrue(gateway.validate_tool_execution("git_status", ToolPermission.REPO_READ))
        # code_interpreter should be disabled by default
        self.assertFalse(gateway.validate_tool_execution("code_interpreter", ToolPermission.REPO_READ))

    def test_context_compiler(self):
        compiler = ContextCompiler()
        pack = compiler.compile_knowledge_pack("Comments API", "Engineer")
        self.assertIn("visibility_invariants", pack)
        self.assertLessEqual(pack["max_context_bytes"], 15360)

    def test_task_engine_lifecycle(self):
        engine = TaskEngine()
        task = TaskContract(
            task_id="TASK-01",
            goal_id="GOAL-01",
            objective="Audit Comments API",
            scope="apps/web",
            owner_agent="Engineer"
        )
        engine.create_task(task)
        self.assertEqual(engine.tasks["TASK-01"].status, TaskState.QUEUED)
        
        engine.transition_state("TASK-01", TaskState.RUNNING)
        self.assertEqual(engine.tasks["TASK-01"].status, TaskState.RUNNING)

        engine.transition_state("TASK-01", TaskState.REVIEW)
        self.assertEqual(engine.tasks["TASK-01"].status, TaskState.REVIEW)

        engine.transition_state("TASK-01", TaskState.ACCEPTED)
        self.assertEqual(engine.tasks["TASK-01"].status, TaskState.ACCEPTED)

if __name__ == "__main__":
    unittest.main()
