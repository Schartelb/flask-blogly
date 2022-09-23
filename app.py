"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from models import db,  connect_db, User, Post

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
    l_name = request.form["l_name"]
    imageURL = request.form["image_URL"]

    new_user = User(first_name=f_name, last_name=l_name, image_url=imageURL)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def specific_user(user_id):
    '''Specific User information'''
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("detail.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Edit specific user'''
    user = User.query.get_or_404(user_id)
    return render_template('edituser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def apply_user_changes(user_id):
    '''Push user changes to db'''
    thisuser = User.query.get_or_404(user_id)
    if request.form['f_name'] != User.first_name:
        thisuser.first_name = request.form['f_name']
        db.session.add(thisuser)
        print('f_name')
    if request.form['l_name'] != User.last_name:
        thisuser.last_name = request.form['l_name']
        db.session.add(thisuser)
        print('l_name')
    if request.form['iconURL'] != User.image_url:
        thisuser.image_url = request.form['imageURL']
        db.session.add(thisuser)
        print('image')
    db.session.commit()
    return render_template(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete user from db'''
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    '''Add post Form'''
    user = User.query.get_or_404(user_id)
    return render_template('addpost.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post_send(user_id):
    '''Posts post post-haste'''
    p_title = request.form["p_title"]
    p_body = request.form["p_body"]
    new_post = Post(title=p_title, content=p_body, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def specific_post(post_id):
    '''Specific Post information'''
    post = Post.query.get_or_404(post_id)
    return render_template("postdetail.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''Edit specific post'''
    post = Post.query.get_or_404(post_id)
    return render_template('editpost.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def apply_post_changes(post_id):
    '''Push post changes to db'''
    thispost = Post.query.filter(Post.id == post_id)
    if request.form['p_title'] != Post.title:
        thispost.first_name = request.form['p_title']
        db.session.add(thispost)
    if request.form['p_body'] != Post.content:
        thispost.last_name = request.form['p_body']
        db.session.add(thispost)
    db.session.commit()
    return render_template('/posts')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete post from db'''
    this_post = Post.query.get_or_404(post_id)
    user = this_post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user}')
