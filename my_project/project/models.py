from flask import Flask
import flask_sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toys.db'
db = flask_sqlalchemy.SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    brand_name = db.Column(db.String(300))
    url = db.Column(db.String(300))
    