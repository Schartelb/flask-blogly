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
                                    ), default='https://powerusers.microsoft.com/t5/image/serverpage/image-id/98171iCC9A58CAF1C9B5B9/image-size/large/is-moderation-mode/true?v=v2&px=999')

    def __repr__(self):
        u = self
        return f'<User {u.id}, {u.first_name} {u.last_name}, profile image: {u.image_url}'
