# coding=utf-8

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = {
    'person': {'name': 'tom'},
    'book': {'name': 'hello'},
    'todo': {'name': 'profit'}
}

class Users(Resource):
    def get(self, user=None):
        if user:
            return users[user]
        return users

    def delete(self, user):
        del users[user]
        return 'ok'

    def put(self, user):
        pass

api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(debug=True)
