from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager





app = Flask(__name__)
app.config["SECRET_KEY"] = 'ca5d0b8db826115d6e0f9a9bfdb6a4d7'
app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///site.db'
app.config["SQLACHEMY_TRACK_MODIFICATIONS"] = False
app.config["CLIENT_CSV"]='' #put full path of excel_file folder (inside static directory) example in app-guide.txt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category= 'info'
from giveaway import routes


