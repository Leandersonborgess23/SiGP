from flask import Flask
from flask_wtf import CSRFProtect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy() #Criando objeto
csrf = CSRFProtect(app) #Protege os formulários contra ataques CSRF
migrate = Migrate()
login_manager = LoginManager(app)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models

@login_manager.user_loader
def load_user(user_id):
    return models.Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()