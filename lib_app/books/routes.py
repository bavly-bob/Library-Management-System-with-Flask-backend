from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Book, Transaction
from datetime import datetime
from ..forms import BookForm

books_bp = Blueprint('books', __name__, template_folder='templates', url_prefix='/books')

# simple decorator for librarian-only routes
from functools import wraps

def librarian_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_librarian():
            flash('You need librarian access.', 'warning')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return wrapped


@books_bp.route('/add', methods=['GET', 'POST'])
@login_required
@librarian_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data.strip(), author=form.author.data.strip(), year=form.year.data)
        db.session.add(book)
        db.session.commit()
        flash('Book added.', 'success')
        return redirect(url_for('main.index'))
    return render_template('book_form.html', form=form)


@books_bp.route('/<int:book_id>/borrow', methods=['POST'])
@login_required
def borrow(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.available:
        flash('Book is not available.', 'warning')
        return redirect(url_for('main.index'))
    tx = Transaction(user_id=current_user.id, book_id=book.id, borrowed_at=datetime.utcnow(), due_date=Transaction.compute_due_date())
    book.available = False
    db.session.add(tx)
    db.session.commit()
    flash(f"Borrowed '{book.title}'. Due: {tx.due_date.date()}", 'success')
    return redirect(url_for('main.index'))
