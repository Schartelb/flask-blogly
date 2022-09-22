from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
dudley = User(first_name='Dudley', last_name="Do-Right")
magilla = User(first_name='Magilla', last_name="Gorilla")
fred = User(first_name='Fred', last_name="Flintstone")

# Add new objects to session, so they'll persist
db.session.add(dudley)
db.session.add(magilla)
db.session.add(fred)

# Commit--otherwise, this forces error on Posts!
db.session.commit()

# Add posts
welcome = Post(title='Welcome!', content='Welcome to the Blogly!')
add_post = Post(title='Adding Posts',
                content='Add and Edit posts to your liking!')

# Add new posts to session, so they'll persist
db.session.add(welcome)
db.session.add(add_post)

# Commit--to save!
db.session.commit()
