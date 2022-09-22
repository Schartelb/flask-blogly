"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from models import db,  connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "dumdumusers"

connect_db(app)


@app.route('/')
def list_users():
    '''Shows user list from db'''
    return redirect('/users')


@app.route('/users')
def all_users():
    '''List of all users'''
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def add_user():
    '''Form for adding new user'''
    return render_template('adduser.html')


@app.route('/users/new', methods=['POST'])
def push_user_to_db():
    '''Adds user to db'''
    f_name = request.form["f_name"]
    # l_name = request.form["l_name"] These are failing
    # imageURL = request.form["image_url"]

    # new_user = User(first_name=f_name, last_name=l_name, image_url=iconURL)
    # db.session.add(new_user)
    # db.session.commit()
    return f'You added {f_name}'


@app.route('/users/<int:user_id>')
def specific_user(user_id):
    '''Specific User information'''
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Edit specific user'''
    user = User.query.get_or_404(user_id)
    return render_template('edituser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def apply_user_changes(user_id):
    '''Push user changes to db'''
    user = User.query.filter_by(id=user_id)
    if request.form['f_name']:
        user.first_name = request.form['f_name']
        db.session.add()
    if request.form['l_name']:
        user.last_name = request.form['l_name']
        db.session.add()
    if request.form['iconURL']:
        user.image_url = request.form['iconURL']
        db.session.add()
    db.session.commit()
    return render_template('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete user from db'''
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')
