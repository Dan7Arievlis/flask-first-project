from fakepinterest import database, login_manager
from datetime import datetime, UTC
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(database.Model, UserMixin):
    __tablename__ = "tb_user"
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), nullable=False)
    email = database.Column(database.String(40), nullable=False, unique=True)
    password = database.Column(database.String(128), nullable=False)
    posts = database.relationship("Post", backref="user", lazy=True)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image = database.Column(database.String(128), default='default.png')
    publish_date = database.Column(database.DateTime, nullable=False, default=datetime.now(UTC))
    user_id = database.Column(database.Integer, database.ForeignKey("tb_user.id"), nullable=False)