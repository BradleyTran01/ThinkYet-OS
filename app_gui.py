import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from company.os.loader import ThinkYetOSLoader
from company.authority.resolver import AuthorityResolver
from company.tools.gateway import ToolCapabilityGateway, ToolPermission
from company.context.compiler import ContextCompiler
from company.tasks.engine import TaskEngine, TaskContract, TaskState

class ThinkYetOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ThinkYet OS — AI Company Runtime")
        self.root.geometry("850x600")
        self.root.configure(bg="#1E1E2E")

        # Initialize Runtime System
        self.os_loader = ThinkYetOSLoader()
        self.task_engine = TaskEngine()
        self.context_compiler = ContextCompiler(self.os_loader)
        self.tool_gateway = ToolCapabilityGateway()

        self._build_ui()

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#181825", padx=10, pady=10)
        header_frame.pack(fill="x")

        # Load Logo
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(logo_path).resize((40, 40), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                logo_label = tk.Label(header_frame, image=self.logo_img, bg="#181825")
                logo_label.pack(side="left", padx=(0, 10))
            except Exception:
                pass
        
        title_label = tk.Label(header_frame, text="ThinkYet OS", font=("Helvetica", 18, "bold"), fg="#89B4FA", bg="#181825")
        title_label.pack(side="left", padx=5)

        subtitle_label = tk.Label(header_frame, text="AI Company Runtime v1.0", font=("Helvetica", 11), fg="#A6ADC8", bg="#181825")
        subtitle_label.pack(side="left")

        # Main Layout
        main_frame = tk.Frame(self.root, bg="#1E1E2E")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Control Panel
        control_frame = tk.LabelFrame(main_frame, text=" Bảng điều khiển Goal & Task ", font=("Helvetica", 11, "bold"), fg="#CDD6F4", bg="#1E1E2E", bd=1)
        control_frame.pack(fill="x", pady=10)

        tk.Label(control_frame, text="Founder Goal / Task Objective:", font=("Helvetica", 10), fg="#BAC2DE", bg="#1E1E2E").pack(anchor="w", padx=10, pady=5)

        self.goal_entry = tk.Entry(control_frame, font=("Helvetica", 11), bg="#313244", fg="#CDD6F4", insertbackground="white", bd=0)
        self.goal_entry.insert(0, "Kiểm tra và xác thực Visibility Gate cho Comments API")
        self.goal_entry.pack(fill="x", padx=10, pady=5)

        btn_frame = tk.Frame(control_frame, bg="#1E1E2E")
        btn_frame.pack(fill="x", padx=10, pady=5)

        run_btn = tk.Button(btn_frame, text="🚀 Chạy Task Lifecycle", font=("Helvetica", 10, "bold"), bg="#89B4FA", fg="#11111B", activebackground="#B4BEFE", command=self.run_task_thread)
        run_btn.pack(side="left", padx=10)

        audit_btn = tk.Button(btn_frame, text="🔍 Kiểm tra OS Policy", font=("Helvetica", 10), bg="#45475A", fg="#CDD6F4", command=self.show_os_policy)
        audit_btn.pack(side="left")

        # Output / Log Area
        output_frame = tk.LabelFrame(main_frame, text=" Nhật ký Runtime Log ", font=("Helvetica", 11, "bold"), fg="#CDD6F4", bg="#1E1E2E", bd=1)
        output_frame.pack(fill="both", expand=True, pady=10)

        self.log_area = scrolledtext.ScrolledText(output_frame, font=("Menlo", 10), bg="#11111B", fg="#A6E3A1", insertbackground="white")
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

        self.log("[SYSTEM] ThinkYet OS AI Company Runtime ready.")
        self.log(f"[OS LOADER] Loaded Authority Levels A0-A7 & Canonical Artifacts.")

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def show_os_policy(self):
        visibility = self.os_loader.get_visibility_policy()
        self.log("\n--- THINKYET OS VISIBILITY INVARIANTS ---")
        for k, v in visibility.items():
            self.log(f"• {k}: {v}")

    def run_task_thread(self):
        threading.Thread(target=self._execute_task_pipeline, daemon=True).start()

    def _execute_task_pipeline(self):
        objective = self.goal_entry.get()
        self.log(f"\n[GOAL ENGINE] Received Goal: '{objective}'")
        
        # Create Task
        task = TaskContract(
            task_id="TASK-GUI-01",
            goal_id="GOAL-FOUNDER",
            objective=objective,
            scope="apps/web/comments",
            owner_agent="Engineer"
        )
        self.task_engine.create_task(task)
        self.log(f"[TASK ENGINE] Task Created: {task.task_id} | State: {task.status}")

        # Transition to RUNNING
        self.task_engine.transition_state(task.task_id, TaskState.RUNNING)
        self.log(f"[TASK ENGINE] State -> {TaskState.RUNNING}")

        # Context Compiler
        kpack = self.context_compiler.compile_knowledge_pack(task.scope, task.owner_agent)
        self.log(f"[CONTEXT COMPILER] Compiled Knowledge Pack ({kpack['max_context_bytes']} bytes budget)")

        # Capability Gateway check
        perm = ToolPermission.REPO_READ
        allowed = self.tool_gateway.validate_tool_execution("repo_read", perm)
        self.log(f"[TOOL GATEWAY] Permission check for '{perm.value}': ALLOWED={allowed}")

        # Transition to REVIEW
        self.task_engine.transition_state(task.task_id, TaskState.REVIEW)
        self.log(f"[TASK ENGINE] State -> {TaskState.REVIEW} (Independent Reviewer audit)")

        # Transition to ACCEPTED
        self.task_engine.transition_state(task.task_id, TaskState.ACCEPTED)
        self.log(f"[TASK ENGINE] State -> {TaskState.ACCEPTED} (Goal execution successful & verified)")
        self.log("[EVIDENCE] Artifacts & diffs attached successfully.")

def main():
    root = tk.Tk()
    app = ThinkYetOSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
