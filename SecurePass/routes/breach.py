from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from ..crypto import check_hibp_password, password_strength, strength_label
from ..database.connectionpostgreSQL import get_db

breach_bp = Blueprint("breach", __name__)


@breach_bp.route("/", methods=["GET", "POST"])
#means user must be logged in for accesing this
@login_required
def index():
    result = None
    checked_password = ""
    #getting the data from the field
    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if not password:
            flash("Please enter a password to check.", "warning")
        else:
            checked_password = password
            #checking if data has been found in any breach using HIBP api
            occurrences = check_hibp_password(password)
            #using the password_strength function from crypto.py file to check passwd strength
            score = password_strength(password)
            result = {
                "is_breached": occurrences > 0,
                "occurrences": occurrences,
                "score": score,
                "label": strength_label(score),
            }

    user_id = str(current_user.id)
    with get_db() as conn:
        #cursor is used to execute sql queries
        with conn.cursor() as cur:
            #executing query for the user_id and checking each passwd entry for breach
            cur.execute(
                "SELECT id, name, type, is_breached, strength_score FROM vault_entries "
                "WHERE user_id = %s AND (is_breached = TRUE OR strength_score < 40) "
                "ORDER BY is_breached DESC, strength_score ASC LIMIT 10",
                (user_id,),
            )
            #returns all the passwds that are at risk
            at_risk = cur.fetchall()

    return render_template(
        "app/breach.html",
        result=result,
        checked_password=checked_password,
        at_risk=at_risk,
        strength_label=strength_label,
    )
