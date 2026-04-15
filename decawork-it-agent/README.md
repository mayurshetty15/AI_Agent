# Decawork IT Agent

## Overview

The Decawork IT Agent is an AI-powered system that allows users to perform IT administration tasks on a mock web-based admin panel using natural language commands. The AI agent uses browser automation (via browser-use library and Claude LLM) to interact with the panel visually, just like a human would, without any DOM shortcuts or API calls. It takes screenshots, interprets the UI, and performs actions such as creating users, resetting passwords, and assigning licenses.

## Architecture

- **Mock IT Panel**: A Flask web application with in-memory data storage, featuring four main pages: Dashboard (stats and activity log), Users (list, create, edit, delete), Reset Password, and Licenses (assignment).
- **AI Agent**: A Python script that leverages the browser-use library for browser automation, integrated with Anthropic's Claude (claude-3-5-sonnet-20241022) via LangChain. It uses Playwright for headless browser control.
- **Flow**: User provides a natural language task → Agent initializes browser → Navigates to panel URL → Takes screenshots and decides actions → Performs clicks, typing, scrolling → Confirms completion via flash messages → Returns result.

## Setup

### Prerequisites

- Python 3.11+
- Anthropic API key (obtain from Anthropic console)

### Install

```bash
git clone <repo>
cd decawork-it-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### Run the panel

```bash
python -m panel.app
# Panel runs at http://localhost:5000
```

### Run a task

```bash
python -m agent.agent "Reset password for bob@company.com to NewPass123"
python -m agent.agent "Create user Jane Doe, jane@company.com, role Designer, Active"
python -m agent.agent "Assign Microsoft365 license to alice@company.com"
python -m agent.agent "Create user Tom Ray, tom@company.com, role Viewer — if user already exists just assign them a GitHub license"
```

## Demo Tasks (for Loom video)

1. Password reset: "Reset the password for bob@company.com to SecurePass456"
2. Create new user: "Create a new user named John Doe with email john@company.com, role Developer, status Active"
3. Multi-step: create user + assign license: "Create user Sam Ray with email sam@company.com role Viewer, then assign them a GitHub license"

## Key Decisions

- **browser-use over raw Playwright**: browser-use provides a built-in LLM-browser interaction loop, allowing the agent to make decisions based on visual screenshots rather than hardcoded selectors, enabling more human-like and flexible automation.
- **In-memory storage**: Simplifies the demo by eliminating the need for database setup, keeping the panel zero-configuration.
- **Flash messages**: Provides clear, machine-readable feedback for the agent to confirm task success or failure by reading the page content.
- **Claude claude-sonnet-4-20250514**: Chosen for its strong vision capabilities and instruction-following accuracy in navigating and interacting with web forms.
