from datetime import datetime

class Folder:
  def __init__(self,row):
    self.id=row["id"]
    self.user_id=row["user_id"]
    self.name=row["name"]
    self.created_at=row["created_at"]