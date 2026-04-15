# ⚡ Quick Start Guide

Get the AI IT Support Agent running in 5 minutes!

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## 2️⃣ Start the Admin Panel

**Terminal 1:**

```bash
python main.py
```

You should see:

```
🚀 Starting IT Admin Panel at http://localhost:8000
```

Open in browser: [http://localhost:8000](http://localhost:8000)

**Login with:**

- Email: `admin`
- Password: `admin`

## 3️⃣ Run Agent Commands

**Terminal 2:**

```bash
python agent.py "Create a user john@company.com with password secure123"
```

Watch the browser automate the form! ✨

## 📋 Example Commands

### Create User

```bash
python agent.py "Create a user john@company.com with password MySecure123"
python agent.py "Create user jane@example.com password pass456"
```

### Reset Password

```bash
python agent.py "Reset password for john@company.com"
python agent.py "Reset john@company.com to default password"
```

### Check User Exists

```bash
python agent.py "Does john@company.com exist"
python agent.py "Check if admin exists in the system"
```

## 🧪 Run Demo

See everything in action:

```bash
# Terminal 1: Start panel
python main.py

# Terminal 2: Run demo (in another terminal)
python run_local.py demo
```

The demo will:

1. Create a user
2. Reset the password
3. Check if the user exists

## 🌐 Panel Routes

| Route                  | Purpose               |
| ---------------------- | --------------------- |
| `GET /login`           | Login page            |
| `POST /login`          | Process login         |
| `GET /dashboard`       | Main dashboard        |
| `GET /create-user`     | User creation form    |
| `POST /create-user`    | Create user action    |
| `GET /reset-password`  | Password reset form   |
| `POST /reset-password` | Reset password action |

## 🔧 Configuration

Create `.env` file for OpenAI API (optional):

```env
OPENAI_API_KEY=sk-your-api-key-here
PANEL_URL=http://localhost:8000
```

If no API key, the agent uses simple keyword matching (no LLM needed).

## 🐛 Troubleshooting

### Port 8000 already in use?

```python
# Edit main.py, change port:
uvicorn.run(app, host="127.0.0.1", port=8001)

# Update agent.py:
result = await agent.execute_task(task, base_url="http://localhost:8001")
```

### Playwright error?

```bash
python -m playwright install chromium
```

### Can't login?

- Ensure panel is running: `python main.py`
- Check http://localhost:8000
- Use admin/admin credentials

## 📚 Next Steps

- Explore `agent.py` to see how automation works
- Check `llm.py` for NLU logic
- Modify `templates/` to customize the UI
- Add more agent actions in `data.py`

## ✨ Key Features

- ✅ Natural language task parsing
- ✅ Real browser automation (Playwright)
- ✅ Form filling and submission
- ✅ Multi-step workflows
- ✅ Result reporting
- ✅ No API shortcuts (human-like!)

---

**Ready? Start with:** `python main.py`
