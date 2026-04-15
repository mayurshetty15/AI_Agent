"""Quick start script to run the panel and agent demo."""

import subprocess
import time
import sys
import os

def run_panel():
    """Start the FastAPI panel."""
    print("\n" + "="*60)
    print("🚀 STARTING IT ADMIN PANEL")
    print("="*60)
    print("\nPanel will start at: http://localhost:8000")
    print("Login with: admin / admin")
    print("\nPress Ctrl+C to stop the panel.\n")
    
    subprocess.run([sys.executable, "main.py"])

def run_agent_demo():
    """Run demo agent tasks."""
    print("\n" + "="*60)
    print("🤖 RUNNING AGENT DEMO")
    print("="*60 + "\n")
    
    demo_tasks = [
        "Create a user john@company.com with password secure123",
        "Reset password for john@company.com",
        "Check if john@company.com exists",
    ]
    
    for i, task in enumerate(demo_tasks, 1):
        print(f"\n📋 Demo Task {i}/{len(demo_tasks)}: {task}")
        print("-" * 60)
        
        result = subprocess.run(
            [sys.executable, "agent.py", task],
            capture_output=False
        )
        
        if result.returncode != 0:
            print(f"❌ Task failed with return code {result.returncode}")
        else:
            print(f"✅ Task completed")
        
        if i < len(demo_tasks):
            print("\nWaiting 2 seconds before next task...")
            time.sleep(2)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "panel":
            run_panel()
        elif sys.argv[1] == "demo":
            run_agent_demo()
        else:
            print("Usage: python run_local.py [panel|demo]")
            print("\nExamples:")
            print("  python run_local.py panel  # Start the admin panel")
            print("  python run_local.py demo   # Run demo agent tasks")
    else:
        print("\n" + "="*60)
        print("🎯 AI IT SUPPORT AGENT - QUICK START")
        print("="*60)
        print("\nUsage:")
        print("  python run_local.py panel  # Start admin panel")
        print("  python run_local.py demo   # Run agent demo tasks")
        print("\nManual Usage:")
        print("  Terminal 1: python main.py")
        print("  Terminal 2: python agent.py '<task description>'")
        print("\n" + "="*60 + "\n")
