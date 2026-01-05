import os
from lib_app import create_app
from lib_app.extensions import db
from lib_app.models import User, Book

app = create_app()

with app.app_context():
    db.create_all()

    # create admin if missing
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
            role='librarian'
        )
        admin.set_password(os.environ.get('ADMIN_PASSWORD', 'adminpass'))
        db.session.add(admin)

    # create normal user if missing
    if not User.query.filter_by(username='user').first():
        user = User(
            username='user',
            email=os.environ.get('USER_EMAIL', 'user@example.com'),
            role='user'
        )
        user.set_password(os.environ.get('USER_PASSWORD', 'userpass'))
        db.session.add(user)

    # seed books if empty
    if Book.query.count() == 0:
        sample_books = [
            Book(title='1984', author='George Orwell', year=1949),
            Book(title='The Hobbit', author='J.R.R. Tolkien', year=1937),
            Book(title='Clean Code', author='Robert C. Martin', year=2008),
        ]
        db.session.add_all(sample_books)

    db.session.commit()
    print('Database created/seeded.')
