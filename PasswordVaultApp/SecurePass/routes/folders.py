from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..database.connectionpostgreSQL import get_db
from ..database.folders_db import user_folder,add_fold,del_fold,upd_fold
folders_bp = Blueprint("folders", __name__)


@folders_bp.route("/")
@login_required
def index():
    user_id = str(current_user.id)
    folders=user_folder(user_id)
    return render_template("app/folders.html", folders=folders)


@folders_bp.route("/new", methods=["POST"])
@login_required
def create():
    user_id = str(current_user.id)
    name = request.form.get("name", "").strip()
    if not name:
        flash("Folder name is required.", "danger")
        return redirect(url_for("folders.index"))
    add_fold(user_id,name)
    return redirect(url_for("folders.index"))


@folders_bp.route("/<int:folder_id>/delete", methods=["POST"])
@login_required
def delete(folder_id):
    user_id = str(current_user.id)
    del_fold(user_id,folder_id)
    return redirect(url_for("folders.index"))


@folders_bp.route("/<int:folder_id>/rename", methods=["POST"])
@login_required
def rename(folder_id):
    user_id = str(current_user.id)
    name = request.form.get("name", "").strip()
    if not name:
        flash("Folder name is required.", "danger")
        return redirect(url_for("folders.index"))
    upd_fold(name,folder_id,user_id)
    return redirect(url_for("folders.index"))
