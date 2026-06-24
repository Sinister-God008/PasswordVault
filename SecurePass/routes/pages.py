from flask import Blueprint, render_template, request, jsonify
from ..crypto import check_hibp_password

#Creates the blueprint object for creating routes
pages_bp = Blueprint("pages", __name__)

#home route
@pages_bp.route("/")
def index():
    return render_template("index.html")

#contact route
@pages_bp.route("/contact")
def contact():
    return render_template("contact.html")


@pages_bp.route("/api/public/breach/check", methods=["POST"])
def public_breach_check():
    #returns json data if invalid or absent returns {}
    data = request.get_json(silent=True) or {}
    #retreiving password w/o any spaces
    password = data.get("password", "").strip()
    if not password:
        #handling user trying to access breach data w/o login
        return jsonify({"error": "Password is required"}), 400
    #checking for passwd breach
    occurrences = check_hibp_password(password)
    #if breach data found return it else will return Flase and 0 as json
    return jsonify({"is_breached": occurrences > 0, "occurrences": occurrences})
