from datetime import datetime

# In-memory database
users = {}
activity_log = []

# Pre-seed users
users[1] = {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@company.com",
    "role": "Admin",
    "status": "Active",
    "password": "password123",  # In real app, this would be hashed
    "license": "None"
}

users[2] = {
    "id": 2,
    "name": "Bob Smith",
    "email": "bob@company.com",
    "role": "Developer",
    "status": "Active",
    "password": "password123",
    "license": "None"
}

users[3] = {
    "id": 3,
    "name": "Carol White",
    "email": "carol@company.com",
    "role": "Designer",
    "status": "Inactive",
    "password": "password123",
    "license": "None"
}

users[4] = {
    "id": 4,
    "name": "David Lee",
    "email": "david@company.com",
    "role": "Developer",
    "status": "Active",
    "password": "password123",
    "license": "None"
}

users[5] = {
    "id": 5,
    "name": "Eve Martin",
    "email": "eve@company.com",
    "role": "Manager",
    "status": "Active",
    "password": "password123",
    "license": "None"
}

next_user_id = 6

def get_user_by_id(user_id):
    return users.get(user_id)

def get_user_by_email(email):
    for user in users.values():
        if user["email"] == email:
            return user
    return None

def get_all_users():
    return list(users.values())

def add_user(name, email, role, status, password):
    global next_user_id
    user_id = next_user_id
    next_user_id += 1
    users[user_id] = {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "status": status,
        "password": password,
        "license": "None"
    }
    return user_id

def update_user(user_id, name=None, email=None, role=None, status=None, password=None, license=None):
    user = users.get(user_id)
    if user:
        if name is not None:
            user["name"] = name
        if email is not None:
            user["email"] = email
        if role is not None:
            user["role"] = role
        if status is not None:
            user["status"] = status
        if password is not None:
            user["password"] = password
        if license is not None:
            user["license"] = license
        return True
    return False

def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return True
    return False

def reset_password(email, new_password):
    user = get_user_by_email(email)
    if user:
        user["password"] = new_password
        return True
    return False

def assign_license(user_id, license):
    user = users.get(user_id)
    if user:
        user["license"] = license
        return True
    return False

def add_activity(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    activity_log.append({
        "timestamp": timestamp,
        "action": action
    })

def get_recent_activity(limit=10):
    return activity_log[-limit:]

def get_stats():
    total_users = len(users)
    active_users = sum(1 for u in users.values() if u["status"] == "Active")
    inactive_users = total_users - active_users
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    }