from datetime import datetime, timedelta
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="patron", nullable=False)


    transactions = db.relationship("Transaction", back_populates="user", cascade='all, delete-orphan')


    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_librarian(self) -> bool:
        return self.role == "librarian"
    


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)

    transactions = db.relationship("Transaction", back_populates='book', cascade='all, delete-orphan')

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="transactions")
    book = db.relationship("Book", back_populates="transactions")

    @staticmethod
    def compute_due_date(days: int = 14):
        return datetime.utcnow() + timedelta(days=days)

    def mark_returned(self):
        self.returned_at = datetime.utcnow()