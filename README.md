# Refactored Flask Library App

1. create virtual env and install

python -m venv venv
source venv/bin/activate # windows: venv\Scripts\activate
pip install -r requirements.txt

2. set environment variables (important):

export FLASK_APP=lib_app
export FLASK_ENV=development
export SECRET_KEY="your-secret-here"
# optional admin creds used by seed script
export ADMIN_PASSWORD="changeme"

3. initialize database & migrations

flask db init
flask db migrate -m "init"
flask db upgrade

4. seed the database

python seed.py

5. run

flask run