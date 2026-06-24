class Audit_Log:
  def __init__(self,row):
    self.id=row["id"]
    self.user_id=row["user_id"]
    self.action=row["action"]
    self.resource_name=row["resource_name"]
    self.ip_address=row["ip_address"]
    self.created_at=row["created_at"]