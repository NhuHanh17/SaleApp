from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:111111@localhost/saledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'tranthinhuhanh'
app.config['PAGE_SIZE'] = 10

db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(cloud_name='dinusoo6h',
                    api_key='113676918263236',
                    api_secret='4XJvP2A8bOzrRetOrVard941L_Q')