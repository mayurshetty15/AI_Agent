from flask import Flask, render_template, request, redirect, url_for, flash
import panel.database as db

app = Flask(__name__)
app.secret_key = "supersecretkey"  # In production, use a secure key

@app.route('/')
def index():
    stats = db.get_stats()
    recent_activity = db.get_recent_activity()
    return render_template('index.html', stats=stats, recent_activity=recent_activity)

@app.route('/users')
def users():
    all_users = db.get_all_users()
    return render_template('users.html', users=all_users)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', '')
        status = request.form.get('status', '')
        password = request.form.get('password', '')

        errors = []
        if len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        if '@' not in email or '.' not in email:
            errors.append("Email must contain @ and .")
        if role not in ['Admin', 'Developer', 'Designer', 'Manager', 'Viewer']:
            errors.append("Role must be one of: Admin, Developer, Designer, Manager, Viewer")
        if status not in ['Active', 'Inactive']:
            errors.append("Status must be Active or Inactive")
        if not password:
            errors.append("Password is required.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create_user.html', name=name, email=email, role=role, status=status)

        user_id = db.add_user(name, email, role, status, password)
        db.add_activity(f"User created: {name} ({email})")
        flash("User created successfully", 'success')
        return redirect(url_for('users'))

    return render_template('create_user.html')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        flash("User not found", 'error')
        return redirect(url_for('users'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', '')
        status = request.form.get('status', '')

        errors = []
        if len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        if '@' not in email or '.' not in email:
            errors.append("Email must contain @ and .")
        if role not in ['Admin', 'Developer', 'Designer', 'Manager', 'Viewer']:
            errors.append("Role must be one of: Admin, Developer, Designer, Manager, Viewer")
        if status not in ['Active', 'Inactive']:
            errors.append("Status must be Active or Inactive")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit_user.html', user=user, name=name, email=email, role=role, status=status)

        db.update_user(user_id, name=name, email=email, role=role, status=status)
        db.add_activity(f"User updated: {name} ({email})")
        flash("User updated successfully", 'success')
        return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = db.get_user_by_id(user_id)
    if user:
        db.delete_user(user_id)
        db.add_activity(f"User deleted: {user['name']} ({user['email']})")
        flash("User deleted successfully", 'success')
    else:
        flash("User not found", 'error')
    return redirect(url_for('users'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        new_password = request.form.get('new_password', '')

        if not new_password:
            flash("New password is required.", 'error')
            return render_template('reset_password.html', email=email)

        if db.reset_password(email, new_password):
            db.add_activity(f"Password reset for {email}")
            flash(f"Password reset for {email}", 'success')
        else:
            flash("User not found.", 'error')

    return render_template('reset_password.html')

@app.route('/licenses')
def licenses():
    all_users = db.get_all_users()
    return render_template('licenses.html', users=all_users)

@app.route('/licenses/assign', methods=['POST'])
def assign_license():
    user_id = int(request.form.get('user_id', 0))
    license = request.form.get('license', 'None')

    if license not in ['None', 'Microsoft365', 'GitHub', 'Slack', 'Jira']:
        flash("Invalid license.", 'error')
        return redirect(url_for('licenses'))

    user = db.get_user_by_id(user_id)
    if user:
        db.assign_license(user_id, license)
        db.add_activity(f"License assigned: {license} to {user['name']} ({user['email']})")
        flash("License assigned successfully", 'success')
    else:
        flash("User not found.", 'error')

    return redirect(url_for('licenses'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)