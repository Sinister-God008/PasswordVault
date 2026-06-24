#This file handles all the SQL queries that need to run as per users request and creates functions for each
from .connectionpostgreSQL import get_db
from SecurePass.models.folders_type import Folder
from flask import flash

def user_folder(user_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT f.id, f.name, f.created_at,
                COUNT(v.id) as entry_count
                FROM folders f
                LEFT JOIN vault_entries v ON f.id = v.folder_id
                WHERE f.user_id = %s
                GROUP BY f.id ORDER BY f.name
                """,
                (user_id,),
            )
            folders = cur.fetchall()
            return folders

#Getting id and name of folder for vault funciton route
def get_id_name(user_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name FROM folders WHERE user_id=%s ORDER BY name",(user_id,)
            )
            folders=cur.fetchall()
            return folders

def add_fold(user_id,name):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO folders (user_id, name) VALUES (%s, %s)", (user_id, name)
            )
            conn.commit()
    flash(f'Folder "{name}" created.', "success")

def del_fold(user_id,folder_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM folders WHERE id = %s AND user_id = %s RETURNING name",
                (folder_id, user_id),
            )
            row = cur.fetchone()
            conn.commit()
    if row:
        flash(f'Folder "{row["name"]}" deleted.', "success")

def upd_fold(name,folder_id,user_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE folders SET name = %s WHERE id = %s AND user_id = %s",
                (name, folder_id, user_id),
            )
            conn.commit()
    flash(f'Folder renamed to "{name}".', "success")
    

