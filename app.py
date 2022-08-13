from flask import Flask
from flask_restful import Api
from flask_jwt import JWT 
import os 
import re

from db import db
from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_EXCEPTIONS'] = True
app.secret_key = 'ryan'
api = Api(app)

# SQLAlchemy 1.4.x has removed support of the postgres:// URI scheme which is what heroku uses so need to update the env var
uri = os.getenv("DATABASE_URL", "sqlite:///data.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=4999, debug=True)  # important to mention debug=True
