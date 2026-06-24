def get_vault_form_data(request):
  return {
    "name" : request.form.get("name", "").strip(),
    "secret" : request.form.get("secret", ""),
    "username" : request.form.get("username", "").strip() or None,
    "url" : request.form.get("url", "").strip() or None,
    "notes" : request.form.get("notes", "").strip() or None,
    "folder_id" : (
      int(request.form.get("folder_id"))
      if request.form.get("folder_id")
      else None
      ),
    "rotation_days" : (
      int(request.form.get("rotation_days"))
      if request.form.get("rotation_days")
      else None
    ),
  }