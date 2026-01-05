# set_passwords.py
# Place this in the project root (same place you run your app from).
# Usage: activate your venv, then: python set_passwords.py

from lib_app import create_app
from lib_app.extensions import db
from lib_app.models import User
from werkzeug.security import generate_password_hash

# Choose secure test passwords (change them after testing)
ADMIN_PWD = "adminpass"   # example test password
USER_PWD  = "userpass"    # example test password

app = create_app()
with app.app_context():
    # Admin user
    admin = User.query.filter_by(username="admin").first()
    if admin:
        admin.password_hash = generate_password_hash(ADMIN_PWD)
        admin.role = "librarian"
    else:
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash(ADMIN_PWD),
            role="librarian"
        )
        db.session.add(admin)

    # Normal user
    user = User.query.filter_by(username="user").first()
    if user:
        user.password_hash = generate_password_hash(USER_PWD)
        user.role = "user"
    else:
        user = User(
            username="user",
            email="user@example.com",
            password_hash=generate_password_hash(USER_PWD),
            role="user"
        )
        db.session.add(user)

    db.session.commit()
    print("Passwords updated. Admin:", "admin /", ADMIN_PWD, "role=librarian")
    print("User:  ", "user  /", USER_PWD,  "role=user")
