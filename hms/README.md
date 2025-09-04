## Hospital Management System (Flask)

### Quickstart
1. Create virtualenv (optional) and install deps:
```bash
pip install -r requirements.txt
```
2. Initialize database and run:
```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "init"
flask db upgrade
python app.py
```
3. Seed admin and login:
- Visit `/auth/seed-admin` once, then login with `admin / admin123`.

### Notes
- Uses Bootstrap 5, SQLAlchemy, Flask-Login.
- Extend CRUD following the pattern in `app/routes.py`.

