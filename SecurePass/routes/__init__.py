from .pages import pages_bp
from .auth import auth_bp
from .vault import vault_bp
from .folders import folders_bp
from .dashboard import dashboard_bp
from .audit import audit_bp
from .breach import breach_bp


def register_blueprints(app):
    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(vault_bp, url_prefix="/vault")
    app.register_blueprint(folders_bp, url_prefix="/folders")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(audit_bp, url_prefix="/audit")
    app.register_blueprint(breach_bp, url_prefix="/breach")
