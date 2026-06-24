from .connectionpostgreSQL import get_db
from SecurePass.models.user import User

def get_user_by_id(user_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            #running sql query to return data about user using userid
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            #storing the output of query from table in row variable
            row = cur.fetchone()
            #returning the User object with row as the parameter for the constructor
            return User(row) if row else None

#used for fetching details from table using email to verify during login in auth.py
def get_user_by_email(email: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            return User(row) if row else None

#creating and storing new user data during register in auth.py 
def create_user(email: str, name: str, password_hash: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s) RETURNING *",
                (email, name, password_hash),
            )
            row = cur.fetchone()
            conn.commit()
            return User(row)