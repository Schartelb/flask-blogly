"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
dt = datetime.now()


def connect_db(app):
    db.app = app
    db.init_app(app)


user_default = 'https://bit.ly/user_default'


class User(db.Model):
    '''Model for Users'''
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50))

    image_url = db.Column(db.String(1000
                                    ), default=user_default)

    posts = db.relationship("Post", backref="users",
                            cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f'<User {u.id}, {u.first_name} {u.last_name}, profile image: {u.image_url}'

    @property
    def full_name(self):
        u = self  # unnecessary
        return f'{u.first_name} {u.last_name}'


class Post(db.Model):
    '''Post Model for Blogly'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)  # Solution shows datetime.datetime.now which didn't work

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        p = self
        return f'<Post:{p.title}, {p.content}  by {p.users.full_name}'


class Tag(db.Model):
    '''Tags for posts for Blogly'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(15), nullable=False, unique=True)

    taggedposts = db.relationship('Post',
                                  secondary="posttags",
                                  # cascade="all,delete",  # Not sure why this has the octothorpe which makes it a comment?
                                  backref="poststags",)


class PostTag(db.Model):
    '''Tags/Post Many/Many relationship'''

    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
