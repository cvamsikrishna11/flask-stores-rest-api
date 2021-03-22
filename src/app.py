from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os
from datetime import timedelta
from security import authenticate, identity
from src.resources.user import UserRegister
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from src.models.db import db

app = Flask(__name__)
# this is API key, need to be stored at some secure places like env or SSM param store
app.secret_key = os.environ.get('SECRET_KEY',
                                'vamsi#123')

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


@app.before_first_request
def create_tables():
    db.create_all()


# db import for SQL Alchemy
db.init_app(app)

# for JWT token
jwt = JWT(app, authenticate, identity)  # /aut --> /login

# API resources
api.add_resource(Item, '/item/<string:name>')  # http:127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')  # http:127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')  # http:127.0.0.1:5000/items
api.add_resource(Store, '/store/<string:name>')  # http:127.0.0.1:5000/store/gachibowli
api.add_resource(StoreList, '/stores')  # http:127.0.0.1:5000/store/1
if __name__ == '__main__':
    app.run(port=5000, debug=True)
