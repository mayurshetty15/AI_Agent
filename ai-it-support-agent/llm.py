"""LLM task parsing logic."""

import json
import os
from typing import Dict, Any, Optional

# Try to import OpenAI, fall back to mock if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def parse_task_with_openai(user_input: str) -> Dict[str, Any]:
    """Parse user input using OpenAI API to extract task intent and parameters."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return parse_task_mock(user_input)
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are an IT support AI assistant. Parse the following user request and extract the intent and parameters.

User request: "{user_input}"

Respond with a JSON object containing:
- "action": one of "create_user", "reset_password", "check_user", or "unknown"
- "email": email address if mentioned
- "password": password if mentioned
- "reasoning": brief explanation of what you extracted

Example for "Create a user john@company.com with password secure123":
{{"action": "create_user", "email": "john@company.com", "password": "secure123", "reasoning": "User wants to create a new account"}}

Example for "Reset password for admin@company.com":
{{"action": "reset_password", "email": "admin@company.com", "password": null, "reasoning": "User wants to reset password to default"}}

Always respond with valid JSON, no additional text."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a JSON API. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        response_text = response.choices[0].message.content.strip()
        result = json.loads(response_text)
        return result
    except Exception as e:
        print(f"Error calling OpenAI: {e}. Falling back to mock parsing.")
        return parse_task_mock(user_input)


def parse_task_mock(user_input: str) -> Dict[str, Any]:
    """Mock LLM task parsing using simple NLP heuristics."""
    user_input_lower = user_input.lower()
    
    # Extract action
    if "create" in user_input_lower and "user" in user_input_lower:
        action = "create_user"
    elif "reset" in user_input_lower and "password" in user_input_lower:
        action = "reset_password"
    elif "check" in user_input_lower or "exist" in user_input_lower:
        action = "check_user"
    else:
        action = "unknown"
    
    # Extract email (simple regex for full emails, or simple word for check_user)
    email = None
    import re
    email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', user_input)
    if email_match:
        email = email_match.group()
    elif action == "check_user":
        # For check_user, also try to extract simple usernames
        # Look for words after "if", "check", "does" that might be usernames
        check_patterns = [
            r'if\s+([\w.-]+)\s+exists?',  # "if admin exists"
            r'check\s+if\s+([\w.-]+)\s+exists?',  # "check if admin exists" 
            r'does\s+([\w.-]+)\s+exist',  # "does admin exist"
            r'([\w.-]+)\s+exists?',  # "admin exists"
        ]
        for pattern in check_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                candidate = match.group(1)
                # Skip common words
                if candidate.lower() not in ['if', 'check', 'does', 'the', 'user', 'a']:
                    email = candidate
                    break
    
    # Extract password only for create_user tasks
    password = None
    if action == "create_user":
        password_match = re.search(r'password\s+([^\s.,?]+)', user_input, re.IGNORECASE)
        if password_match:
            password = password_match.group(1)
    
    return {
        "action": action,
        "email": email,
        "password": password,
        "reasoning": f"Parsed '{user_input}' using mock LLM"
    }


def parse_task(user_input: str) -> Dict[str, Any]:
    """Parse user input to extract task intent and parameters."""
    return parse_task_with_openai(user_input)
