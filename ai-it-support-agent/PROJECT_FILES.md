# Project Files Overview

## Core Application Files

### `main.py` - FastAPI Backend

- FastAPI application with all routes
- Template rendering logic
- User authentication and session management
- Route handlers for login, dashboard, create-user, reset-password

**Key Routes:**

- `GET /` → Redirect to login
- `GET/POST /login` → Authentication
- `GET /dashboard` → Main panel
- `GET/POST /create-user` → User creation
- `GET/POST /reset-password` → Password reset
- `GET /logout` → Logout

### `agent.py` - Browser Automation

- `ITSupportAgent` class with Playwright integration
- Async browser control methods
- Task execution workflow
- Login automation
- Form filling and submission
- Success/failure detection

**Key Methods:**

- `start()` → Launch browser
- `login()` → Authenticate to panel
- `create_user()` → Create new user
- `reset_password()` → Reset user password
- `execute_task()` → Main task executor

### `llm.py` - Natural Language Processing

- OpenAI API integration
- Mock LLM fallback parser
- Task intent extraction
- Parameter extraction (email, password, action)

**Functions:**

- `parse_task_with_openai()` → Use OpenAI API
- `parse_task_mock()` → Fallback parser
- `parse_task()` → Main entry point

### `data.py` - In-Memory Database

- User storage dictionary
- Session management
- User CRUD operations

**Functions:**

- `get_user()` → Retrieve user password
- `create_user()` → Add new user
- `user_exists()` → Check user existence
- `reset_password()` → Change user password
- `list_all_users()` → Get all users

## HTML Templates

### `templates/login.html`

- Login page with email/password form
- Demo credentials helper
- Gradient styling

### `templates/dashboard.html`

- Main dashboard after login
- Navigation cards (Create User, Reset Password)
- User list table
- Logout button

### `templates/create_user.html`

- User creation form
- Email and password inputs
- Success/error message display
- Cancel button

### `templates/reset_password.html`

- Password reset form
- Email input only
- Resets to "default123"
- Success/error messaging

## Configuration Files

### `requirements.txt`

Dependencies:

- fastapi==0.104.1
- uvicorn==0.24.0
- playwright==1.40.0
- openai==1.3.0
- python-dotenv==1.0.0
- pydantic==2.5.0

### `.env` and `.env.example`

Environment variables:

- `OPENAI_API_KEY` → OpenAI API key (optional)
- `PANEL_URL` → Panel URL (default: http://localhost:8000)

## Documentation Files

### `README.md`

Comprehensive documentation:

- Architecture overview
- Setup instructions
- Usage examples
- Configuration guide
- Troubleshooting tips

### `QUICKSTART.md`

Quick start guide:

- 5-minute setup
- Basic commands
- Examples
- Troubleshooting

## Helper Scripts

### `run_local.py`

Convenience script:

- `python run_local.py panel` → Start panel
- `python run_local.py demo` → Run demo tasks

## Project Structure

```
ai-it-support-agent/
├── main.py                    # FastAPI app
├── agent.py                   # Playwright automation
├── llm.py                     # LLM parsing
├── data.py                    # Database
├── run_local.py              # Helper script
├── requirements.txt           # Dependencies
├── .env                      # Configuration (created)
├── .env.example             # Config template
├── README.md                # Full documentation
├── QUICKSTART.md            # Quick start
├── PROJECT_FILES.md         # This file
└── templates/               # HTML templates
    ├── login.html
    ├── dashboard.html
    ├── create_user.html
    └── reset_password.html
```

## How to Use Each File

1. **Start Development:**
   - `python main.py` → Run panel
   - `python agent.py "<task>"` → Run agent

2. **Understand Flow:**
   - Read `main.py` for HTTP routes
   - Check `agent.py` for automation logic
   - See `llm.py` for NLU

3. **Modify:**
   - Edit `data.py` for new user actions
   - Update `templates/` for UI changes
   - Extend `agent.py` for new automation patterns

4. **Deploy:**
   - Copy all files to server
   - Install dependencies
   - Set environment variables
   - Run `python main.py`

## File Dependencies

```
main.py
├── data.py (user storage)
├── templates/*.html (rendering)
└── pathlib, fastapi, starlette

agent.py
├── llm.py (task parsing)
├── playwright (browser automation)
└── asyncio (async support)

llm.py
├── openai (optional)
├── json, re (parsing)
└── os (environment)

data.py
├── typing (type hints)
└── None
```

## Quick Reference

| Component    | Language | Purpose    |
| ------------ | -------- | ---------- |
| main.py      | Python   | HTTP API   |
| agent.py     | Python   | Automation |
| llm.py       | Python   | NLU        |
| data.py      | Python   | Database   |
| \*.html      | HTML     | UI         |
| run_local.py | Python   | Utilities  |

---

**Total Lines of Code:** ~1500
**File Size:** ~50 KB
**Dependencies:** 6 packages
