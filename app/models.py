from typing import List

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()


# SQLALchemy class
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)


class ToDo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(20), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# To get a user id
def get_user(username):
    return User.query.filter_by(username=username).first()


# To get a user to do list
def get_user_todo_list(id_user: str) -> List[str]:
    return ToDo.query.filter_by(id_user=id_user).all()


# To delete a To DO
def get_todo(id_user: str, id: str):
    return ToDo.query.filter_by(id_user=id_user, id=id).first()


# To implement user login authentication
class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserModel(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(username):
        user_db = get_user(username)
        user_data = UserData(
            username=user_db.username,
            password=user_db.password,
        )

        return UserModel(user_data)
