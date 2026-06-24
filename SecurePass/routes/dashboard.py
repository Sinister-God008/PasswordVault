from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..database.connectionpostgreSQL import get_db
from ..database.audit_db import get_recent_log
from ..database.vault_entry_db import safe_passwd,refresh_entry,get_type_brkdwn

dashboard_bp = Blueprint("dashboard", __name__)

#this route is /dashboard/ cause we registered it with url prefix as /dashboard
@dashboard_bp.route("/")
@login_required
def index():
    user_id = str(current_user.id)

    with get_db() as conn:
        #this query is for analysis to check what all passwds are safe and what are vulnerable
        entries=safe_passwd(conn,user_id)
         #returns the entries requiring change once the user enters dashboard it refreshes
        rotation_entries=refresh_entry(conn,user_id)
        #returns the recent logs(last 8)
        recent_logs=get_recent_log(conn,user_id)

    total = len(entries)
    password_entries = [e for e in entries if e["type"] == "password"]
    weak = sum(1 for e in password_entries if (e["strength_score"] or 0) < 40)
    breached = sum(1 for e in entries if e["is_breached"])

    from datetime import datetime, timezone, timedelta
    ninety_days_ago = datetime.now(timezone.utc) - timedelta(days=90)
    old = sum(1 for e in password_entries if e["last_changed_at"] < ninety_days_ago)

    secret_counts: dict = {}
    for e in entries:
        k = e["encrypted_secret"]
        secret_counts[k] = secret_counts.get(k, 0) + 1
    reused = sum(c - 1 for c in secret_counts.values() if c > 1)

    strong = sum(1 for e in password_entries if (e["strength_score"] or 0) >= 70)
    pct_strong = round(strong / len(password_entries) * 100) if password_entries else 100

    #This displays the safety score analysis in the form of a valued meter that represents passwd safety rating
    if total==0:
        score=None
    else:
        score = 100
        score -= min(30, round(weak / max(len(password_entries), 1) * 30))
        score -= min(30, breached * 10)
        score -= min(20, reused * 5)
        score -= min(10, round(old / max(len(password_entries), 1) * 10))

        score = max(0, min(100, score))

    now_ts = datetime.now(timezone.utc).timestamp()
    rotation_due = []
    for e in rotation_entries:
        rotation_days=e["rotation_interval_days"]
        if rotation_days:
            due_ts = e["last_changed_at"].timestamp() + (rotation_days*86400)
        else:
            due_ts= e["last_changed_at"].timestamp()
        days_overdue = int((now_ts - due_ts) / 86400)
        if days_overdue >= 0:
            rotation_due.append({**dict(e), "days_overdue": days_overdue})
    rotation_due.sort(key=lambda x: x["days_overdue"], reverse=True)

    type_breakdown=get_type_brkdwn(user_id)
    #This part basically checks if there is 0 entries the dashboard metershows N/A instead of default 100
    for row in type_breakdown:
        row["percentage"]=(
            round(row["count"]/total*100)
            if total>0
            else 0
        )

    return render_template(
        "app/dashboard.html",
        score=score,
        total=total,
        weak=weak,
        breached=breached,
        reused=reused,
        old=old,
        pct_strong=pct_strong,
        rotation_due=rotation_due[:5],
        recent_logs=recent_logs,
        type_breakdown=type_breakdown,
    )
