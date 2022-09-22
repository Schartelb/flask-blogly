"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''Model for Users'''
    __tablename__ = 'blogly'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50))

    image_url = db.Column(db.String(1000
                                    ), default='https://bit.ly/user_default')

    def __repr__(self):
        u = self
        return f'<User {u.id}, {u.first_name} {u.last_name}, profile image: {u.image_url}'

    # def full_name(self):


class Post(db.Model):
    '''Post Model for Blogly'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.String(2000))

    created_at = db.Column(db.timestamp, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('blogly.user_id'))

    users = db.relationship('User', backref='posts')
