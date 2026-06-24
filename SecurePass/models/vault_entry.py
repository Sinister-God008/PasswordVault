
class Vault_Entry:
  def __init__(self,row):
    self.id=row["id"]
    self.user_id=row["user_id"]
    self.folder_id=row["folder_id"]
    self.type=row["type"]
    self.name=row["name"]
    self.username=row["username"]
    self.url=row["url"]
    self.notes=row["notes"]
    self.encrypted_secret=row["encrypted_secret"]
    self.strength_score=row["strength_score"]
    self.is_breached=row["is_breached"]
    self.rotation_interval_days=row["rotation_interval_days"]
    self.created_at=row["created_at"]
    self.last_changed_at=row["last_changed_at"]