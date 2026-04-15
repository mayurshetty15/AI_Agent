# 🤖 AI IT Support Agent

A fully automated AI agent that performs IT support tasks (user creation, password resets) by navigating a web-based admin panel using browser automation. The agent understands natural language commands and executes them like a human—no DOM selectors or API shortcuts.

## 🎯 Features

- **Natural Language Interface**: Give commands like "Create user john@company.com with password secure123"
  python agent.py "Reset password john@company.com"
- **Browser Automation**: Uses Playwright to control a real browser
- **LLM-Based Task Parsing**: Converts natural language to structured tasks using OpenAI API (or mock parser)
- **Mock Admin Panel**: FastAPI-based panel with user management features
- **Human-Like Navigation**: Clicks buttons, fills forms, submits like a real user

## 🏗️ Architecture

### Components

1. **Mock IT Admin Panel** (`main.py`)
   - FastAPI application
   - Routes: `/login`, `/dashboard`, `/create-user`, `/reset-password`
   - In-memory user storage
   - Session-based authentication

2. **AI Agent** (`agent.py`)
   - Playwright-based browser automation
   - Executes multi-step workflows
   - Handles login, navigation, form filling
   - Result reporting

3. **LLM Parser** (`llm.py`)
   - Natural language → Structured tasks
   - Uses OpenAI API (or simple heuristic fallback)
   - Supports: create_user, reset_password, check_user actions

4. **Data Layer** (`data.py`)
   - In-memory user database
   - User management functions

### Flow

```
User Input
   ↓
LLM Parser (NLU)
   ↓
Agent (Playwright)
   ↓
Browser Automation
   ↓
Admin Panel (FastAPI)
   ↓
Result
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key (optional - works with mock parser)

### Installation

```bash
# Clone/create the project
cd ai-it-support-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install browser binaries
python -m playwright install chromium

# Create .env file (optional for OpenAI)
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY if desired
```

### Run the Panel

```bash
# Terminal 1: Start the admin panel
python main.py

# Output:
# 🚀 Starting IT Admin Panel at http://localhost:8000
```

The panel is now available at:

- **Login**: http://localhost:8000/login
- **Demo Credentials**:
  - Email: `admin`
  - Password: `admin`

### Run the Agent

```bash
# Terminal 2: Run an agent task
python agent.py "Create a user john@company.com with password secure123"

# Output:
# ============================================================
# 📋 Task: Create a user john@company.com with password secure123
# ============================================================
# 🧠 Parsed Task: {'action': 'create_user', 'email': 'john@company.com', 'password': 'secure123', 'reasoning': '...'}
# ✅ Browser started
# 🔐 Logging in as admin...
# ✅ Logged in successfully
# 📍 Navigating to /create-user
# 👤 Creating user: john@company.com
# ✅ User john@company.com created successfully
# ============================================================
# 📊 Result: {'task': '...', 'action': 'create_user', 'success': True, 'message': '...'}
# ============================================================
```

## 📝 Example Commands

### Create a User

```bash
python agent.py "Create a user john@company.com with password secure123"
python agent.py "Create user jane@example.com password mypass123"
```

### Reset Password

```bash
python agent.py "Reset password for john@company.com"
python agent.py "Reset password john@example.com"
```

### Check if User Exists

```bash
python agent.py "Check if admin@company.com exists"
python agent.py "Does john@company.com exist in the system"
```

## 🧠 Task Parser Behavior

The agent parses natural language using:

1. **OpenAI API** (if `OPENAI_API_KEY` is set in `.env`)
   - More accurate intent extraction
   - Better handling of variations

2. **Simple Heuristic Parser** (fallback)
   - Keyword matching: "create", "reset", "check"
   - Regex email extraction
   - Works without API key

Example parsing:

```
Input: "Create a user john@company.com with password secure123"
↓
Output: {
  "action": "create_user",
  "email": "john@company.com",
  "password": "secure123",
  "reasoning": "User wants to create a new account"
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Optional: OpenAI API key for better NLU
OPENAI_API_KEY=sk-your-key-here

# Panel URL (usually localhost:8000)
PANEL_URL=http://localhost:8000
```

### Headless Mode

By default, the browser runs with UI visible (`headless=False`). To run headless:

Edit `agent.py` line 241:

```python
result = await agent.execute_task(task, headless=True)  # Change False to True
```

## 📁 Project Structure

```
ai-it-support-agent/
├── main.py                 # FastAPI backend
├── agent.py               # Playwright automation
├── llm.py                 # LLM task parser
├── data.py                # In-memory database
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
└── templates/
    ├── login.html        # Login form
    ├── dashboard.html    # Main dashboard
    ├── create_user.html  # User creation form
    └── reset_password.html # Password reset form
```

## 🧪 Testing

### Manual Testing

1. Start panel: `python main.py`
2. Open browser: `http://localhost:8000`
3. Login with admin/admin
4. Manually test buttons

### Agent Testing

```bash
# Create user test
python agent.py "Create user test@example.com with password test123"

# Reset password test
python agent.py "Reset password for admin"

# Check user test
python agent.py "Does test@example.com exist"
```

## 🔐 Security Notes

⚠️ **This is a demo/educational project!** Not for production use:

- Passwords stored in plaintext (should be hashed)
- Simple session management (should use JWT/secure cookies)
- No input validation on forms (should be validated)
- CORS not configured
- Admin credentials hardcoded

## 📊 Supported Actions

| Action           | Example Input                                   | Requirement     |
| ---------------- | ----------------------------------------------- | --------------- |
| `create_user`    | "Create user john@example.com password pass123" | email, password |
| `reset_password` | "Reset password for john@example.com"           | email           |
| `check_user`     | "Does john@example.com exist"                   | email           |

## 🐛 Troubleshooting

### Browser won't start

```bash
# Reinstall Playwright browsers
python -m playwright install chromium
```

### Login fails

- Ensure panel is running: `python main.py`
- Check panel is accessible: `http://localhost:8000/login`
- Try username: `admin`, password: `admin`

### OpenAI API errors

- Leave `OPENAI_API_KEY` unset to use mock parser
- Mock parser doesn't require API key

### Port already in use

Change port in `main.py`:

```python
uvicorn.run(app, host="127.0.0.1", port=8001)  # Change 8000 to 8001
```

Update agent:

```python
result = await agent.execute_task(task, base_url="http://localhost:8001")
```

## 🎓 Learning Outcomes

This project demonstrates:

- **LLM Integration**: Using LLMs for NLU
- **Browser Automation**: Playwright for web automation
- **FastAPI**: Building REST APIs
- **Async Programming**: Async/await patterns
- **Web Scraping**: Reading page content for form-filling logic
- **Multi-step Workflows**: Chaining browser actions

## 📚 Resources

- [Playwright Docs](https://playwright.dev/python/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs/)

## 📄 License

MIT - Educational use

## 🤝 Contributing

Feel free to extend with:

- More panel features
- Additional agent actions
- Better error handling
- Test suite
- Docker setup
#   A I _ A g e n t  
 