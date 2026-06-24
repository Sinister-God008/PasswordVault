from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..database.user_db import get_user_by_email, create_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    #if user alreqady logged in take to dashboard directly
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    #taking the field values from form
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))
        #checking if details exist in db for login using function from db.py
        user = get_user_by_email(email)
        #checking if user is valid or password is valid
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", email=email)
        #creates session for logged in user and creates a cookie to remember the user
        login_user(user, remember=remember)
        #checks if there is a next parameter value where user wants to go after login
        next_page = request.args.get("next")
        #if next parameter true? go there else take to to dashboard
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    #if user already login take to dashboard directly
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if not name:
            errors.append("Full name is required.")
        if not email or "@" not in email:
            errors.append("A valid email address is required.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if get_user_by_email(email):
            errors.append("An account with this email already exists.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/register.html", name=name, email=email)
        #saving the hash vlue instead of the actual passwd
        password_hash = generate_password_hash(password)
        #creating and storing user details with hashed passwd using funcn from db.py
        user = create_user(email, name, password_hash)
        #create login session for the user created
        login_user(user)
        flash("Welcome to SecurePass! Your vault is ready.", "success")
        #take to dashboard
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
#means to logout user must be logged in
@login_required
def logout():
    logout_user()
    flash("You have been signed out securely.", "info")
    #takes to home page
    return redirect(url_for("pages.index"))
