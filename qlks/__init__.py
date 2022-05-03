from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary


app = Flask("__name__")
app.secret_key = 'SD*(&*SD(Gsa@md98aW&D^@(*HD'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:09022001@localhost/qlks?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name ='quanlykhachsan-cnpm',
    api_key ='429937473125332',
    api_secret ='-k-rg0NZdbrmpo59Q0h10Y-yW2U'
)


login = LoginManager(app=app)