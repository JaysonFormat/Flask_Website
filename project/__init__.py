import os
import logging
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Message, Mail


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'project', 'employee_files')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.permanent_session_lifetime = timedelta(minutes=30)

# Set up audit logging to a file
app.logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('audit.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

from project.errors.handlers import errors
app.register_blueprint(errors)

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#The secret key is a random string of characters used for cryptographic purposes to secure user sessions
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #'47bd15adbe24b1d8af0dc807514145f2'


# MYSQL DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

#'mysql+pymysql://root:root@localhost/flask_db'
#'mysql+pymysql://galicia:Jayson$$$21@localhost/flask_db'
#'mysql+pymysql://<username created>:<password>@<hostname>/flask_db'
#'CREATE ANOTHER USER FOR DATABASE AND GRANT ALL PRIVILEGES
#'sudo ufw allow http/tcp'
#gunicorn --workers=3 run:app'



db = SQLAlchemy(app)

# migrate = Migrate(app,db)
migrate = Migrate(db=db, app=app, render_as_batch=True, compare_type=True, dialect_name='mysql')



bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from project import routes
# Weird issue

