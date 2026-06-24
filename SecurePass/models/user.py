#provides is_authenticated,is_active,is_anonymous,get_id()
from flask_login import UserMixin

#This file defines what Users table contains and how to access the data returned by psycopg2 return
class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.email = row["email"]
        self.name = row["name"]
        self.password_hash = row["password_hash"]
        self.created_at = row["created_at"]
    def get_id(self):
        return str(self.id)