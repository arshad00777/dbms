from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/seed-admin")
def seed_admin():
    if User.query.filter_by(username="admin").first():
        flash("Admin already exists", "info")
        return redirect(url_for("auth.login"))
    user = User(username="admin", role="admin", password_hash=generate_password_hash("admin123"))
    db.session.add(user)
    db.session.commit()
    flash("Seeded admin (admin/admin123)", "success")
    return redirect(url_for("auth.login"))

