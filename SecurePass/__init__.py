import os
from flask import Flask
from flask_login import LoginManager
from SecurePass.database.user_db import get_user_by_id


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.secret_key = os.environ["SESSION_SECRET"]

    login_manager = LoginManager()
    login_manager.init_app(app)
    #This is used to redirect user to login page if they try to access a part/section ie login reqd
    login_manager.login_view = "auth.login"
    #Message that is shown to user if login not done
    login_manager.login_message = "Please sign in to access your vault."
    #simply used to decorate the flash message
    login_manager.login_message_category = "info"

    #This is an internal function which helps to get user details using the user_id to allow
    #easier navigation in pages and helps in querying requests from user in different pages easily
    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    from SecurePass.routes import register_blueprints
    register_blueprints(app)
    return app
