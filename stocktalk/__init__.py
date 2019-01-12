from flask import Flask
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from stocktalk.constants.app_constants import APP_CONSTANTS


app = Flask(__name__)
app.config.from_envvar(APP_CONSTANTS.CONFIG_FROM_ENV)

csrf = CSRFProtect()
db = MongoEngine()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

from stocktalk.models.user import User

@login_manager.user_loader
def load_user(user_id):
	return User.objects(pk=user_id).first()

csrf.init_app(app)
db.init_app(app)
login_manager.init_app(app)

from stocktalk import routes