"""AI Agent that controls the admin panel via Playwright browser automation."""

import asyncio
import os
from typing import Dict, Any, Optional
from llm import parse_task
import time


class ITSupportAgent:
    """AI agent that performs IT support tasks by navigating the web panel."""
    
    def __init__(self, base_url: str = "http://localhost:8000", headless: bool = False):
        """Initialize the agent."""
        self.base_url = base_url
        self.headless = headless
        self.browser = None
        self.page = None
        self.logged_in = False
        
    async def start(self):
        """Start the browser."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("❌ Playwright not installed. Install with: pip install playwright")
            return False
        
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.page = await self.browser.new_page()
            print("✅ Browser started")
            return True
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            return False
    
    async def stop(self):
        """Stop the browser."""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ Browser stopped")
    
    async def login(self, email: str = "admin", password: str = "admin"):
        """Login to the admin panel."""
        try:
            print(f"🔐 Logging in as {email}...")
            
            # Navigate to login page
            await self.page.goto(f"{self.base_url}/login")
            await self.page.wait_for_load_state("networkidle")
            
            # Wait for login form
            await self.page.wait_for_selector("input[name='email']", timeout=5000)
            
            # Fill in credentials
            await self.page.fill("input[name='email']", email)
            await self.page.fill("input[name='password']", password)
            
            # Click login button
            await self.page.click("button[type='submit']")
            await self.page.wait_for_load_state("networkidle")
            
            # Check if we're on dashboard
            if "/dashboard" in self.page.url:
                self.logged_in = True
                print(f"✅ Logged in successfully")
                return True
            else:
                print("❌ Login failed - not redirected to dashboard")
                return False
        
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    async def navigate_to(self, path: str):
        """Navigate to a specific page."""
        url = f"{self.base_url}{path}"
        print(f"📍 Navigating to {path}")
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")
    
    async def create_user(self, email: str, password: str) -> bool:
        """Create a new user."""
        try:
            print(f"👤 Creating user: {email}")
            
            # Navigate to create user page
            await self.navigate_to("/create-user")
            
            # Wait for form
            await self.page.wait_for_selector("input[name='email']", timeout=5000)
            
            # Fill in form
            await self.page.fill("input[name='email']", email)
            await self.page.fill("input[name='password']", password)
            
            # Click submit
            await self.page.click("button[type='submit']")
            await self.page.wait_for_load_state("networkidle")
            
            # Check for success message
            success_element = await self.page.query_selector(".success-message")
            if success_element:
                print(f"✅ User {email} created successfully")
                return True
            else:
                # Check for error message
                error_element = await self.page.query_selector(".error-message")
                if error_element:
                    error_text = await error_element.text_content()
                    print(f"❌ Error creating user: {error_text}")
                else:
                    print(f"⚠️  Unclear result - check browser")
                return False
        
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return False
    
    async def reset_password(self, email: str) -> bool:
        """Reset user password."""
        try:
            print(f"🔒 Resetting password for: {email}")
            
            # Navigate to reset password page
            await self.navigate_to("/reset-password")
            
            # Wait for form
            await self.page.wait_for_selector("input[name='email']", timeout=5000)
            
            # Fill in form
            await self.page.fill("input[name='email']", email)
            
            # Click submit
            await self.page.click("button[type='submit']")
            await self.page.wait_for_load_state("networkidle")
            
            # Check for success message
            success_element = await self.page.query_selector(".success-message")
            if success_element:
                print(f"✅ Password reset for {email}")
                return True
            else:
                # Check for error message
                error_element = await self.page.query_selector(".error-message")
                if error_element:
                    error_text = await error_element.text_content()
                    print(f"❌ Error resetting password: {error_text}")
                else:
                    print(f"⚠️  Unclear result - check browser")
                return False
        
        except Exception as e:
            print(f"❌ Error resetting password: {e}")
            return False
    
    async def check_user_exists(self, email: str) -> bool:
        """Check if a user exists (navigate to dashboard and look for user in list)."""
        try:
            print(f"🔍 Checking if user exists: {email}")
            
            # Navigate to dashboard
            await self.navigate_to("/dashboard")
            
            # Wait for the users table to load
            await self.page.wait_for_selector("table tbody", timeout=5000)
            
            # Get all table rows
            rows = await self.page.query_selector_all("table tbody tr")
            
            for row in rows:
                # Get the text content of the first cell (email column)
                cells = await row.query_selector_all("td")
                if cells:
                    email_text = await cells[0].text_content()
                    email_text = email_text.strip()
                    if email_text == email:
                        print(f"✅ User {email} exists")
                        return True
            
            print(f"❌ User {email} not found")
            return False
        
        except Exception as e:
            print(f"❌ Error checking user: {e}")
            return False
    
    async def execute_task(self, user_input: str) -> Dict[str, Any]:
        """Execute a task based on natural language input."""
        print(f"\n{'='*60}")
        print(f"📋 Task: {user_input}")
        print(f"{'='*60}")
        
        # Parse the task
        task_parsed = parse_task(user_input)
        print(f"🧠 Parsed Task: {task_parsed}")
        
        action = task_parsed.get("action", "unknown").lower()
        email = task_parsed.get("email")
        password = task_parsed.get("password")
        
        result = {
            "task": user_input,
            "action": action,
            "success": False,
            "message": ""
        }
        
        try:
            # Start browser if not already started
            if not self.browser:
                if not await self.start():
                    result["message"] = "Failed to start browser"
                    return result
            
            # Login if not already logged in
            if not self.logged_in:
                if not await self.login():
                    result["message"] = "Failed to login"
                    return result
            
            # Execute action
            if action == "create_user":
                if not email or not password:
                    result["message"] = "Email and password required for user creation"
                else:
                    success = await self.create_user(email, password)
                    result["success"] = success
                    result["message"] = f"User creation {'successful' if success else 'failed'}"
            
            elif action == "reset_password":
                if not email:
                    result["message"] = "Email required for password reset"
                else:
                    success = await self.reset_password(email)
                    result["success"] = success
                    result["message"] = f"Password reset {'successful' if success else 'failed'}"
            
            elif action == "check_user":
                if not email:
                    result["message"] = "Email required to check user"
                else:
                    success = await self.check_user_exists(email)
                    result["success"] = success
                    result["message"] = f"User {'exists' if success else 'does not exist'}"
            
            else:
                result["message"] = f"Unknown action: {action}"
        
        except Exception as e:
            result["message"] = f"Error: {str(e)}"
        
        print(f"{'='*60}")
        print(f"📊 Result: {result}")
        print(f"{'='*60}\n")
        
        return result


async def run_agent_task(user_input: str, base_url: str = "http://localhost:8000", headless: bool = False):
    """Run a single agent task."""
    agent = ITSupportAgent(base_url=base_url, headless=headless)
    
    try:
        result = await agent.execute_task(user_input)
        return result
    finally:
        await agent.stop()


def main():
    """Main entry point for agent."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent.py '<task_description>'")
        print("\nExample tasks:")
        print("  - 'Create a user john@company.com with password secure123'")
        print("  - 'Reset password for john@company.com'")
        print("  - 'Check if admin@company.com exists'")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    
    # Run agent
    result = asyncio.run(run_agent_task(task, headless=False))
    
    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")


if __name__ == "__main__":
    main()
