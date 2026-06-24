from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..database.connectionpostgreSQL import get_db
from ..database.audit_db import get_log_count,get_logs
audit_bp = Blueprint("audit", __name__)

ACTIONS = [
    "VAULT_ENTRY_CREATED", "VAULT_ENTRY_VIEWED",
    "VAULT_ENTRY_UPDATED", "VAULT_ENTRY_DELETED",
    "FOLDER_CREATED", "FOLDER_DELETED",
]


@audit_bp.route("/")
@login_required
def index():
    user_id = str(current_user.id)
    action_filter = request.args.get("action", "")
    page = max(1, int(request.args.get("page", 1)))
    per_page = 20
    offset = (page - 1) * per_page
    total=get_log_count(user_id,action_filter)
    logs=get_logs(user_id,per_page,offset,action_filter)
    total_pages = max(1, (total + per_page - 1) // per_page)
    return render_template(
        "app/audit.html",
        logs=logs,
        actions=ACTIONS,
        action_filter=action_filter,
        page=page,
        total_pages=total_pages,
        total=total,
    )
