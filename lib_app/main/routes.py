from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import Book, Transaction, User
from ..forms import BookForm
from .. import db
from datetime import datetime


main_bp = Blueprint('main', __name__)

@main_bp.route("/books/<int:book_id>/borrow", methods=["POST"])
@login_required
def borrow_book(book_id):
    # Only normal users can borrow
    if current_user.role != "user":
        flash("Only users can borrow books.", "danger")
        return redirect(url_for("main.index"))

    book = Book.query.get_or_404(book_id)

    if not book.available:
        flash("Book is already borrowed.", "warning")
        return redirect(url_for("main.index"))

    book.available = False

    tx = Transaction(
        user_id=current_user.id,
        book_id=book.id,
        borrowed_at=datetime.utcnow()
    )

    db.session.add(tx)
    db.session.commit()

    flash("Book borrowed successfully.", "success")
    return redirect(url_for("main.index"))

@main_bp.route("/books/<int:book_id>/return", methods=["POST"])
@login_required
def return_book(book_id):
    # Only normal users can return
    if current_user.role != "user":
        flash("Only users can return books.", "danger")
        return redirect(url_for("main.index"))

    # Strictly get the active transaction for this user and book
    tx = Transaction.query.filter(
        Transaction.book_id == book_id,
        Transaction.user_id == current_user.id,
        Transaction.returned_at.is_(None)
    ).first()

    if not tx:
        flash("You cannot return a book you haven't borrowed.", "warning")
        return redirect(url_for("main.index"))

    # Mark book as available
    book = Book.query.get(tx.book_id)
    try:
        book.available = True
        tx.returned_at = datetime.utcnow()
        db.session.commit()
        flash("Book returned successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error returning book: {str(e)}", "danger")

    return redirect(request.referrer or url_for("main.index"))


@main_bp.route("/books")
@login_required
def books():
    query = request.args.get("q", "").strip()

    if query:
        books = Book.query.filter(
            Book.title.ilike(f"%{query}%") |
            Book.author.ilike(f"%{query}%")
        ).all()
    else:
        books = Book.query.all()

    return render_template("books.html", books=books, query=query)

@main_bp.route("/books/list")
@login_required
def book_list():
    books = Book.query.order_by(Book.title).all()
    return render_template("book_list.html", books=books)

@main_bp.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    if current_user.role != "librarian":
        flash("You are not authorized to edit books.", "danger")
        return redirect(url_for("main.index"))

    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data.strip()
        book.author = form.author.data.strip()
        book.year = form.year.data
        db.session.commit()
        flash("Book updated successfully.", "success")
        return redirect(url_for("main.book_detail", book_id=book.id))

    return render_template("edit_book.html", form=form, book=book)

@main_bp.route("/books/delete/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):
    if current_user.role != "librarian":
        flash("You are not authorized to delete books.", "danger")
        return redirect(url_for("main.index"))

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully.", "success")
    return redirect(url_for("main.book_list"))

@main_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()

    query = Book.query

    if q:
        query = query.filter(
            (Book.title.ilike(f"%{q}%")) |
            (Book.author.ilike(f"%{q}%"))
        )

    books = query.order_by(Book.title).paginate(
        page=page,
        per_page=20,
        error_out=False
)

    return render_template('index.html', books=books, q=q)



@main_bp.route('/transactions')
@login_required
def transactions():
    if current_user.is_librarian():
        txs = Transaction.query.order_by(Transaction.borrowed_at.desc()).limit(200).all()
    else:
        txs = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.borrowed_at.desc()).all()
    return render_template('transactions.html', txs=txs)

@main_bp.route("/books/add", methods=["GET", "POST"])
@login_required
def add_book():
    if current_user.role != "librarian":
        flash("You are not authorized to add books.", "danger")
        return redirect(url_for("main.index"))

    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data.strip(),
            author=form.author.data.strip(),
            year=form.year.data
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("main.index"))

    return render_template("add_book.html", form=form)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_librarian():
        return render_template('403.html'), 403
    total_books = Book.query.count()
    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    ongoing_transactions = Transaction.query.filter_by(returned_at=None).count()
    return render_template('dashboard.html', total_books=total_books, total_users=total_users,
                           total_transactions=total_transactions, ongoing_transactions=ongoing_transactions)
