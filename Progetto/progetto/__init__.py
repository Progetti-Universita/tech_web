from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = '03b6fc16dc76a0541b3d03da5a53f497'

client = MongoClient('mongodb://mongo:27017')
db = client.progetto

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'area_clienti'
login_manager.login_message_category = 'info'

# viene dichiarato alla fine perchè quando importa routes 
# il comando app ancora non è stato inizializzato?

from progetto import routes
