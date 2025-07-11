from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import login_manager
from flask import Flask
from flask_login import LoginManager
from flask import Flask
from app.extensions import db, login_manager

app = Flask(__name__)

login_manager.init_app(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app import models, routes  


    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

   
    with app.app_context():
        db.create_all()

    return app
