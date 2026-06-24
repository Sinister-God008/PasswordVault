from .connectionpostgreSQL import get_db
from SecurePass.models.vault_entry import Vault_Entry
def get_vault_data(user_id,folder_filter=None,type_filter=None):
  query ="""
  SELECT v.id, v.type, v.name, v.username, v.url, v.notes,
  v.folder_id, f.name as folder_name,
  v.strength_score, v.is_breached,
  v.rotation_interval_days, v.created_at, v.last_changed_at
  FROM vault_entries v
  LEFT JOIN folders f ON v.folder_id = f.id
  WHERE v.user_id = %s
  """
  params = [user_id]
  if type_filter:
    query += """
    AND v.type = %s
    """
    params.append(type_filter)

  if folder_filter:
    query += """
    AND v.folder_id = %s
    """
    params.append(int(folder_filter))

  query += """
  ORDER BY v.created_at DESC
  """
  with get_db() as conn:
    with conn.cursor() as cur:
      cur.execute(query, params)
      entries= cur.fetchall()
      return entries

def insert_vault_entry(conn,user_id,entry_type,name,username,url,notes,enc_secret,folder_id,rotation_days,score):
  with conn.cursor() as cur:
    cur.execute(
      """
      INSERT INTO vault_entries
      (user_id, type, name, username, url, notes, encrypted_secret,
      folder_id, rotation_interval_days, strength_score)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
      """,
      (user_id, entry_type, name, username, url, notes,
       enc_secret, folder_id, rotation_days, score
      ),
    )
    new_id = cur.fetchone()["id"]
  return new_id

def get_user_vault_entry(conn,entry_id, user_id):
  with conn.cursor() as cur:
    cur.execute(
      """
      SELECT v.*, f.name as folder_name
      FROM vault_entries v LEFT JOIN folders f ON v.folder_id = f.id
      WHERE v.id =%s AND v.user_id=%s
      """,
      (entry_id, user_id),
    )
    entry = cur.fetchone()
  return entry


def get_all_vdata(entry_id,user_id):
  with get_db() as conn:
    with conn.cursor() as cur:
      cur.execute(
         "SELECT * FROM vault_entries WHERE id = %s AND user_id = %s",
          (entry_id, user_id),
      )
      entry = cur.fetchone()
    return entry

def update_vault(conn,entry_id,user_id,updates):
  set_clauses=[]
  params=[]
  for k,v in updates.items():
    if v=="NOW()":
      set_clauses.append(f"{k}= NOW()")
    else:
      set_clauses.append(f"{k}= %s")
      params.append(v)
  params.extend([entry_id,user_id])
  with conn.cursor() as cur:
    cur.execute(
      f"UPDATE vault_entries SET {', '.join(set_clauses)} WHERE id = %s AND user_id = %s",
      params,
    )
    
def del_vault_entry(conn,entry_id,user_id):
  with conn.cursor() as cur:
    cur.execute(
      "DELETE FROM vault_entries WHERE id = %s AND user_id = %s RETURNING name",
      (entry_id, user_id),
    )
    row = cur.fetchone()
  return row

#*************************************************************************************************************************************************
#These functions are used to execute queries for dashboard.py file
def safe_passwd(conn,user_id):
  with conn.cursor() as cur:
    cur.execute(
      """
      SELECT type, strength_score, is_breached, encrypted_secret, last_changed_at
      FROM vault_entries WHERE user_id = %s
      """,
      (user_id,),
    )
    entries=cur.fetchall()
  return entries

def refresh_entry(conn,user_id):
  with conn.cursor() as cur:
    cur.execute(
      """
      SELECT id, name, type, last_changed_at, rotation_interval_days
      FROM vault_entries WHERE user_id=%s
      """,
      (user_id,),
    )
    rotation_entries=cur.fetchall()
  return rotation_entries

def get_type_brkdwn(user_id):
  with get_db () as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT type, COUNT(*) as count
        FROM vault_entries
        WHERE user_id=%s
        GROUP BY type
        """,
        (user_id,),
      )
      type_breakdown=cur.fetchall()
    return type_breakdown


