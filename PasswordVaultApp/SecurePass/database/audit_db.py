#This file is defining functions which can be used in route files for running custom queries related to audit_logs 
from .connectionpostgreSQL import get_db
from SecurePass.models.audit_log import Audit_Log


def create_audit_log(conn,client_ip, user_id, action, resource_name):
  with conn.cursor() as cur:
    cur.execute(
      """
      INSERT INTO audit_logs(user_id, action,resource_name,ip_address)
      VALUES (%s,%s,%s,%s)
      """,
      (user_id,action,resource_name,client_ip),
    )

def get_log_count(user_id, action_filter=None):  
  with get_db() as conn:
    with conn.cursor() as cur:
      if action_filter:
        cur.execute(
           """
           SELECT COUNT(*) AS total
           FROM audit_logs
           WHERE user_id = %s
           AND action = %s
           """,
           (user_id, action_filter)
        )
      else:
        cur.execute(
          """
          SELECT COUNT(*) AS total
          FROM audit_logs
          WHERE user_id = %s
          """,
          (user_id,)
        )
      return cur.fetchone()["total"]

def get_logs(user_id,per_page,offset,action_filter=None):
  with get_db() as conn:
    with conn.cursor() as cur:
      if action_filter:
        cur.execute(
          """
          SELECT * FROM audit_logs
          WHERE user_id=%s
          AND action=%s
          ORDER BY created_at DESC
          LIMIT %s
          OFFSET %s
          """,
          (user_id,action_filter,per_page,offset)
        )
      else:
        cur.execute(
          """
          SELECT * FROM audit_logs
          WHERE user_id=%s
          ORDER BY created_at DESC
          LIMIT %s
          OFFSET %s
          """,
          (user_id,per_page,offset)
        )
      rows=cur.fetchall()
      return [
        Audit_Log(row)
        for row in rows
      ]
#**********************************************************************************************************************************************
#This function is used to run query from dashboard.py

def get_recent_log(conn,user_id,limit=8):
  with conn.cursor() as cur:
    cur.execute(
      """
      SELECT action, resource_name, ip_address, created_at
      FROM audit_logs WHERE user_id=%s
      ORDER BY created_at DESC LIMIT %s
      """,
      (user_id,limit,),
    )
    recent_logs=cur.fetchall()
  return recent_logs


        

