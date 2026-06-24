from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from ..database.connectionpostgreSQL import get_db
from ..crypto import encrypt, decrypt, password_strength, strength_label
from ..database.vault_entry_db import get_vault_data,insert_vault_entry,get_all_vdata,get_user_vault_entry,update_vault,del_vault_entry
from ..database.audit_db import create_audit_log
from ..database.folders_db import get_id_name
from ..utils.form_helpers import get_vault_form_data
vault_bp = Blueprint("vault", __name__)

ENTRY_TYPES = [
    "password", "api_key", "ssh_key", "env_var",
    "secure_note", "database_credential", "jwt_secret",
]

#Getting the IP of the user 
def _get_client_ip():
    return (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.remote_addr or "unknown"
    )
@vault_bp.route("/")
@login_required
#
def index():
    user_id = str(current_user.id)
    type_filter = request.args.get("type", "")
    folder_filter = request.args.get("folder_id", "")
    search = request.args.get("search", "").strip().lower()
    entries=get_vault_data(user_id, folder_filter, type_filter)
    folders=get_id_name(user_id)
    if search:
        entries = [
            e for e in entries
            if search in e["name"].lower()
            or search in (e["username"] or "").lower()
            or search in (e["url"] or "").lower()
        ]

    return render_template(
        "app/vault.html",
        entries=entries,
        folders=folders,
        type_filter=type_filter,
        folder_filter=folder_filter,
        search=search,
        entry_types=ENTRY_TYPES,
        strength_label=strength_label,
    )


@vault_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_entry():
    user_id = str(current_user.id)
    folders=get_id_name(user_id)
    if request.method == "POST":
        entry_type = request.form.get("type", "")
        data=get_vault_form_data(request)
        name = data["name"]
        secret = data["secret"]
        username = data["username"]
        url = data["url"]
        notes = data["notes"]
        folder_id = data["folder_id"]
        rotation_days = data["rotation_days"]

        if not name or not secret or entry_type not in ENTRY_TYPES:
            flash("Name, type, and secret value are all required.", "danger")
            return render_template("app/vault_new.html", folders=folders, entry_types=ENTRY_TYPES)

        enc_secret = encrypt(secret)
        score = password_strength(secret) if entry_type == "password" else None
        
        with get_db() as conn:
            new_id=insert_vault_entry(conn,user_id,entry_type,name,username,url,notes,enc_secret,folder_id,rotation_days,score)
            client_ip=_get_client_ip()
            create_audit_log(conn,client_ip,user_id,"VAULT_ENTRY_CREATED",name)
            conn.commit()
        flash(f'"{name}" has been added to your vault.', "success")
        return redirect(url_for("vault.detail", entry_id=new_id))

    return render_template("app/vault_new.html", folders=folders, entry_types=ENTRY_TYPES)


@vault_bp.route("/<int:entry_id>")
@login_required
def detail(entry_id):
    user_id = str(current_user.id)
    with get_db() as conn:
        entry=get_user_vault_entry(conn,entry_id,user_id)
        if not entry:
            flash("Entry not found.", "danger")
            return redirect(url_for("vault.index"))
        secret = decrypt(entry["encrypted_secret"])
        client_ip=_get_client_ip()
        create_audit_log(conn,client_ip,user_id, "VAULT_ENTRY_VIEWED", entry["name"])
        conn.commit()
    score = entry["strength_score"]
    return render_template(
        "app/vault_detail.html",
        entry=entry,
        secret=secret,
        score=score,
        strength_label=strength_label(score) if score is not None else "N/A",
    )

@vault_bp.route("/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit(entry_id):
    user_id = str(current_user.id)
    entry=get_all_vdata(entry_id,user_id)
    if not entry:
        flash("Entry not found.", "danger")
        return redirect(url_for("vault.index"))
    folders=get_id_name(user_id)

    if request.method == "POST":
        data=get_vault_form_data(request)
        name = data["name"]
        secret = data["secret"]
        username = data["username"]
        url = data["url"]
        notes = data["notes"]
        folder_id = data["folder_id"]
        rotation_days = data["rotation_days"]

        if not name:
            flash("Name is required.", "danger")
            return render_template("app/vault_edit.html", entry=entry, folders=folders, entry_types=ENTRY_TYPES)

        updates = {
            "name": name, "username": username, "url": url,
            "notes": notes, "folder_id": folder_id,
            "rotation_interval_days": rotation_days,
        }
        if secret:
            updates["encrypted_secret"] = encrypt(secret)
            updates["strength_score"] = password_strength(secret) if entry["type"] == "password" else None
            updates["last_changed_at"] = "NOW()"

        with get_db() as conn:
            update_vault(conn,entry_id,user_id,updates)
            client_ip=_get_client_ip()
            create_audit_log(conn,client_ip, user_id, "VAULT_ENTRY_UPDATED", name)
            conn.commit()
        flash(f'"{name}" has been updated.', "success")
        return redirect(url_for("vault.detail", entry_id=entry_id))
    return render_template("app/vault_edit.html", entry=entry, folders=folders, entry_types=ENTRY_TYPES)


@vault_bp.route("/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete(entry_id):
    user_id = str(current_user.id)
    
    with get_db() as conn:
        row=del_vault_entry(conn,entry_id,user_id)
        if row:
            client_ip=_get_client_ip()
            create_audit_log(conn, client_ip,user_id, "VAULT_ENTRY_DELETED", row["name"])
            conn.commit()
            flash(f'"{row["name"]}" has been permanently deleted.', "success")
        else:
            flash("Entry not found.", "danger")
    return redirect(url_for("vault.index"))
