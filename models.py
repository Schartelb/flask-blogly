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
    __tablename__ = 'blogly'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50))

    image_url = db.Column(db.String(1000
                                    ), default=user_default)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f'<User {u.id}, {u.first_name} {u.last_name}, profile image: {u.image_url}'

    @property
    def full_name(self):
        u = self
        return f'{u.first_name} {u.last_name}'


class Post(db.Model):
    '''Post Model for Blogly'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.String(2000))

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'blogly.id', nullable=False))

    posttags = db.relationship('Tag',
                               secondary='posttags', backref='posts')


class Tag(db.Model):
    '''Tags for posts for Blogly'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(15), nullable=False, unique=True)
    posts = db.relationship('Post',
                            secondary="posts_tags",
                            cascade="all,delete",
                            backref="tags",)


class PostTag(db.Model):
    '''Tags/Post Many/Many relationship'''

    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
