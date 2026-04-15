"""FastAPI admin panel backend."""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

import data

app = FastAPI(title="AI IT Support Admin Panel")

# Store template directory
TEMPLATE_DIR = Path(__file__).parent / "templates"


def render_template(filename: str, **context) -> str:
    """Simple template rendering function."""
    template_path = TEMPLATE_DIR / filename
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple variable replacement
    for key, value in context.items():
        if value is not None and value != "":
            content = content.replace(f"{{{{{key}}}}}", str(value))
        else:
            # Replace with empty string for None or empty values
            content = content.replace(f"{{{{{key}}}}}", "")
    
    return content


@app.get("/", response_class=HTMLResponse)
async def home():
    """Redirect to login."""
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Display login page."""
    content = render_template("login.html", error="")
    return HTMLResponse(content=content)


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Process login."""
    form_data = await request.form()
    email = form_data.get("email", "").strip()
    password = form_data.get("password", "").strip()
    
    # Check credentials
    user_password = data.get_user(email)
    
    if user_password and user_password == password:
        # Store session (simple approach)
        session_id = f"session_{email}_{id(email)}"
        data.sessions[session_id] = email
        
        # Redirect with session in cookie (simplified approach)
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("session_email", email)
        return response
    else:
        error_html = '<div class="error-message">Invalid email or password</div>'
        content = render_template("login.html", error=error_html)
        return HTMLResponse(content=content)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Display dashboard (requires login)."""
    session_email = request.cookies.get("session_email")
    
    if not session_email or not data.user_exists(session_email):
        return RedirectResponse(url="/login")
    
    users_list = data.list_all_users()
    users_html = "".join([f"<tr><td>{email}</td></tr>" for email in users_list.keys()])
    
    content = render_template(
        "dashboard.html",
        username=session_email,
        users_list=users_html
    )
    return HTMLResponse(content=content)


@app.get("/create-user", response_class=HTMLResponse)
async def create_user_page(request: Request):
    """Display create user form."""
    session_email = request.cookies.get("session_email")
    
    if not session_email or not data.user_exists(session_email):
        return RedirectResponse(url="/login")
    
    content = render_template("create_user.html", success="", error="")
    return HTMLResponse(content=content)


@app.post("/create-user", response_class=HTMLResponse)
async def create_user_action(request: Request):
    """Process create user."""
    session_email = request.cookies.get("session_email")
    
    if not session_email or not data.user_exists(session_email):
        return RedirectResponse(url="/login")
    
    form_data = await request.form()
    new_email = form_data.get("email", "").strip()
    new_password = form_data.get("password", "").strip()
    
    if not new_email or not new_password:
        error_html = '<div class="error-message">Email and password are required</div>'
        content = render_template("create_user.html", success="", error=error_html)
        return HTMLResponse(content=content)
    
    # Check if user already exists
    if data.user_exists(new_email):
        error_html = f'<div class="error-message">User {new_email} already exists</div>'
        content = render_template("create_user.html", success="", error=error_html)
        return HTMLResponse(content=content)
    
    # Create user
    if data.create_user(new_email, new_password):
        success_html = f'<div class="success-message">User {new_email} created successfully</div>'
        content = render_template("create_user.html", success=success_html, error="")
        return HTMLResponse(content=content)
    else:
        error_html = '<div class="error-message">Failed to create user</div>'
        content = render_template("create_user.html", success="", error=error_html)
        return HTMLResponse(content=content)


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    """Display reset password form."""
    session_email = request.cookies.get("session_email")
    
    if not session_email or not data.user_exists(session_email):
        return RedirectResponse(url="/login")
    
    content = render_template("reset_password.html", success="", error="")
    return HTMLResponse(content=content)


@app.post("/reset-password", response_class=HTMLResponse)
async def reset_password_action(request: Request):
    """Process password reset."""
    session_email = request.cookies.get("session_email")
    
    if not session_email or not data.user_exists(session_email):
        return RedirectResponse(url="/login")
    
    form_data = await request.form()
    target_email = form_data.get("email", "").strip()
    
    if not target_email:
        error_html = '<div class="error-message">Email is required</div>'
        content = render_template("reset_password.html", success="", error=error_html)
        return HTMLResponse(content=content)
    
    # Reset password
    if data.reset_password(target_email):
        success_html = f'<div class="success-message">Password for {target_email} reset to \'default123\'</div>'
        content = render_template("reset_password.html", success=success_html, error="")
        return HTMLResponse(content=content)
    else:
        error_html = f'<div class="error-message">User {target_email} not found</div>'
        content = render_template("reset_password.html", success="", error=error_html)
        return HTMLResponse(content=content)


@app.get("/logout")
async def logout():
    """Logout user."""
    response = RedirectResponse(url="/login")
    response.delete_cookie("session_email")
    return response


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting IT Admin Panel at http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
