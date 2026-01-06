# Library Management Web Application (CS50 Final Project)

## 📌 Project Overview

This project is a **Library Management Web Application** built as my **CS50 Final Project**. The application allows users to browse and borrow books, while librarians can manage the library’s catalog and monitor borrowing activity. The system implements authentication, role-based access control, and persistent storage using a relational database.

The project demonstrates my understanding of:

* Web application architecture
* Backend development with Flask
* Authentication and authorization
* Database modeling and transactions
* Debugging and iterative development

---

## 🎥 Video Demo

A short video demonstrating the project and explaining the code:

**Video URL:** *to be added*

---

## 🧰 Technologies Used

* **Python 3**
* **Flask** (web framework)
* **Flask-Login** (authentication)
* **Flask-SQLAlchemy** (ORM)
* **SQLite** (database)
* **HTML / Jinja2 / CSS** (frontend)

---

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd lib_app_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

The database is initialized automatically when the application starts.

(Optional) Seed sample data:

```bash
python seed.py
```

### 5. Run the application

```bash
flask run
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000/
```

---

## 👥 User Roles

### Normal User

* Register and log in
* Browse available books
* Borrow books
* Return **only books they personally borrowed**

### Librarian

* Add and edit books
* View dashboard statistics
* Monitor all transactions

---

## 🗂️ Project Structure

```
lib_app/
│── auth/           # Authentication routes (login, register)
│── books/          # Librarian book management
│── main/           # User-facing routes (borrow, return, list)
│── models.py       # Database models
│── forms.py        # WTForms definitions
│── templates/      # HTML templates
│── static/         # CSS and static assets
│── extensions.py   # Flask extensions
│── __init__.py     # App factory
```

---

## 🧠 Design Decisions

* **Role-based access control** was implemented to clearly separate user and librarian capabilities.
* **Transactions table** was used instead of a simple borrow flag to preserve borrowing history.
* **Flask Blueprints** were used to keep the project modular and maintainable.
* The database logic ensures that a book can only have one active borrowing transaction at a time.

---

## 🐞 Known Bugs & Fixes

* A critical bug was discovered where **any logged-in user could return a book borrowed by another user**.

  * Cause: A duplicate return route allowed returning the latest transaction without checking ownership.
  * Fix: Enforced strict filtering by `current_user.id` and removed the unsafe route.

---

## 📚 What I Learned

Through this project, I strengthened my skills in:

* Debugging real-world authorization bugs
* Designing secure backend logic
* Structuring Flask applications
* Translating requirements into working features

---

## ✅ CS50 Compliance

* Uses Python and Flask
* Includes a SQL database
* Demonstrates non-trivial logic
* Original project beyond problem sets
* Accompanied by a video demo

---

## 👤 Author

**Bavly Peter**

CS50 Final Project