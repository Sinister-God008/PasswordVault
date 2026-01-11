from .homeroute import home_bp
from .Strengthchecker import checkp_bp
from .breach import breach_bp, breachpwnedapi_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(checkp_bp)
    app.register_blueprint(breach_bp)
    app.register_blueprint(breachpwnedapi_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)