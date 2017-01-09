from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from logging.handlers import RotatingFileHandler
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_restless import APIManager

from config import Configuration  # import our configuration data.


app = Flask(__name__)
app.config.from_object(Configuration)  # use values from ourConfiguration object.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# TODO : logging daily
file_handler = RotatingFileHandler('blog.log')
app.logger.addHandler(file_handler)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

api = APIManager(app, flask_sqlalchemy_db=db)


@app.before_request
def _before_request():
    g.user = current_user
