import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser, BrowserConfig
from langchain_anthropic import ChatAnthropic
from agent.tasks import build_system_prompt, TASK_EXAMPLES
from agent.logger import log_info, log_success, log_error

load_dotenv()

PANEL_URL = os.getenv("PANEL_URL", "http://localhost:5000")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def run_task(natural_language_task: str) -> str:
    """
    Run an IT support task using browser-use agent.
    The agent opens a real browser, navigates the panel visually,
    and completes the task like a human would.
    """
    log_info(f"Starting task: {natural_language_task}")
    
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        api_key=ANTHROPIC_API_KEY,
        max_tokens=4096,
    )
    
    browser = Browser(
        config=BrowserConfig(
            headless=False,  # Set True for production/CI
            disable_security=False,
        )
    )
    
    system_prompt = build_system_prompt(PANEL_URL)
    
    agent = Agent(
        task=natural_language_task,
        llm=llm,
        browser=browser,
        system_prompt_override=system_prompt,
        max_actions_per_step=5,
        max_failures=3,
    )
    
    try:
        result = await agent.run(max_steps=20)
        log_success(f"Task completed: {result}")
        return str(result)
    except Exception as e:
        log_error(f"Task failed: {e}")
        raise
    finally:
        await browser.close()


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m agent.agent \"<task description>\"")
        print("\nExample tasks:")
        for example in TASK_EXAMPLES:
            print(f"  - {example}")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    result = asyncio.run(run_task(task))
    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()