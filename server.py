from flask import Flask, request, jsonify, send_from_directory
import os
import json
import sys

# Connect directly to Hermes Core modules
from prompter import PromptManager
from utils import validate_and_extract_tool_calls, get_assistant_message
from company.goals.engine import GoalEngine, GoalContract, Milestone
from company.os.loader import ThinkYetOSLoader
from company.authority.resolver import AuthorityResolver
from company.tools.gateway import ToolCapabilityGateway, ToolPermission
from company.context.compiler import ContextCompiler
from company.tasks.engine import TaskEngine, TaskContract, TaskState

app = Flask(__name__, static_folder=".")

# Hermes & ThinkYet Runtime Singletons
prompter = PromptManager()
os_loader = ThinkYetOSLoader()
authority_resolver = AuthorityResolver()
context_compiler = ContextCompiler(os_loader)
tool_gateway = ToolCapabilityGateway()
task_engine = TaskEngine()
goal_engine = GoalEngine()

@app.route("/api/goals", methods=["GET", "POST"])
def goals_handler():
    if request.method == "POST":
        data = request.json or {}
        new_goal = GoalContract(
            goal_id=f"GOAL-{len(goal_engine.goals) + 1:02d}",
            title=data.get("title", "New Goal"),
            description=data.get("description", "Goal description"),
            owner_agent=data.get("owner_agent", "Engineering Agent"),
            priority=data.get("priority", "HIGH"),
            status="ACTIVE",
            progress_percentage=0,
            milestones=[Milestone(id="M1", title="Initial milestone setup", status="IN_PROGRESS", progress_percentage=10)]
        )
        goal_engine.create_goal(new_goal)
        return jsonify({"status": "success", "goal": new_goal.dict()})
    return jsonify(goal_engine.get_all_goals())

@app.route("/api/agents", methods=["GET"])
def get_agents():
    return jsonify([
        {"id": "AGENT-01", "name": "Engineering Agent", "role": "Staff Engineer", "status": "Working", "task": "Visibility regression tests", "model": "Hermes-2-Pro-Llama-3-8B"},
        {"id": "AGENT-02", "name": "Product Agent", "role": "Product Guardian", "status": "Reviewing", "task": "Beta checklist review", "model": "Hermes-2-Pro-Llama-3-8B"},
        {"id": "AGENT-03", "name": "QA Agent", "role": "Quality Assurance", "status": "Working", "task": "Cross-surface test suite", "model": "Hermes-2-Pro-Llama-3-8B"},
        {"id": "AGENT-04", "name": "Design Agent", "role": "Design Systems Lead", "status": "Available", "task": "Ready for tasks", "model": "Hermes-2-Pro-Llama-3-8B"}
    ])

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify([t.dict() for t in task_engine.tasks.values()])

@app.route("/api/knowledge", methods=["GET"])
def get_knowledge():
    return jsonify({
        "authority_map": os_loader.get_authority_map(),
        "visibility_policy": os_loader.get_visibility_policy(),
        "risk_register": os_loader.get_risk_register()
    })

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/api/run_hermes_task", methods=["POST"])
def run_hermes_task():
    data = request.json or {}
    user_query = data.get("query", "Kiểm tra Visibility Gate cho Comments API")

    # 1. Hermes System Prompt Compilation
    sys_prompt = prompter.generate_prompt(user_query, tools=[], num_fewshot=None)

    # 2. ThinkYet OS Context Compiler
    knowledge_pack = context_compiler.compile_knowledge_pack("apps/web/comments", "Staff Engineer")

    # 3. Create Task Contract in Task Engine
    task = TaskContract(
        task_id=f"TASK-HERMES-{len(task_engine.tasks) + 1:02d}",
        goal_id="GOAL-FOUNDER",
        objective=user_query,
        scope="apps/web/comments",
        owner_agent="Engineer"
    )
    task_engine.create_task(task)
    task_engine.transition_state(task.task_id, TaskState.RUNNING)

    # 4. Hermes Simulated LLM Output with XML Tool Call
    simulated_hermes_completion = f"""<tool_call>
{{"name": "ContextCompiler.compile_knowledge_pack", "arguments": {{"task_scope": "apps/web/comments", "agent_role": "Staff Engineer"}}}}
</tool_call>"""

    # 5. Extract & Validate XML Tool Calls using Hermes Utils
    validation, tool_calls, error_msg = validate_and_extract_tool_calls(simulated_hermes_completion)

    # 6. Tool Capability Gateway RBAC Check
    rbac_allowed = tool_gateway.validate_tool_execution("repo_read", ToolPermission.REPO_READ)

    task_engine.transition_state(task.task_id, TaskState.REVIEW)
    task_engine.transition_state(task.task_id, TaskState.ACCEPTED)

    sys_prompt_str = str(sys_prompt)

    return jsonify({
        "status": "success",
        "task_id": task.task_id,
        "state": task.status.value,
        "query": user_query,
        "hermes_core": {
            "xml_parsed": validation,
            "parsed_tool_calls": tool_calls,
            "system_prompt_sample": sys_prompt_str[:250] + "..."
        },
        "thinkyet_os": {
            "knowledge_pack": knowledge_pack,
            "rbac_check": rbac_allowed,
            "visibility_policy": os_loader.get_visibility_policy()
        }
    })

if __name__ == "__main__":
    app.run(port=8080, debug=False)
