"""Blogly application."""
from unicodedata import name
from flask import Flask, request, render_template,  redirect, flash, session
from models import db,  connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "dumdumusers"

connect_db(app)


@app.route('/')
def home_page():
    """Shows post list from db"""
    posts = Post.query.all()
    return render_template('home.html', all_posts=posts)


@app.route('/users')
def all_users():
    """List of all users"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def add_user():
    """Form for adding new user"""
    return render_template('adduser.html')


@app.route('/users/new', methods=['POST'])
def push_user_to_db():
    """Adds user to db"""
    f_name = request.form["f_name"]
    l_name = request.form["l_name"]
    imageURL = request.form["image_URL"]

    new_user = User(first_name=f_name, last_name=l_name, image_url=imageURL)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def specific_user(user_id):
    """Specific User information"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("userdetail.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('edituser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def apply_user_changes(user_id):
    """Push user changes to db"""
    thisuser = User.query.get_or_404(user_id)
    if request.form['f_name'] != User.first_name:
        thisuser.first_name = request.form['f_name']
        db.session.add(thisuser)
    if request.form['l_name'] != User.last_name:
        thisuser.last_name = request.form['l_name']
        db.session.add(thisuser)
    if request.form['imageURL'] != User.image_url:
        thisuser.image_url = request.form['imageURL']
        db.session.add(thisuser)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from db"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Add post Form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('addpost.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post_send(user_id):
    """Posts post post-haste"""
    p_title = request.form["p_title"]
    p_body = request.form["p_body"]
    tags = Tag.query.all()
    new_post = Post(title=p_title, content=p_body, user_id=user_id)
    for tag in tags:
        if tag.name in request.form:
            new_post.poststags.append(tag)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def specific_post(post_id):
    """Specific Post information"""
    post = Post.query.get_or_404(post_id)
    tags = post.poststags
    return render_template("postdetail.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edit specific post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('editpost.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def apply_post_changes(post_id):
    """Push post changes to db"""
    thispost = Post.query.get_or_404(post_id)
    for tag in thispost.poststags:
        PostTag.query.get((tag.id, thispost.id)).delete()
    db.session.commit()
    if request.form['p_title'] != Post.title:
        thispost.title = request.form['p_title']
    if request.form['p_body'] != Post.content:
        thispost.content = request.form['p_body']
    tags = Tag.query.all()
    for tag in tags:
        if tag.name in request.form:
            thispost.poststags.append(tag)
    db.session.add(thispost)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post from db"""
    this_post = Post.query.get_or_404(post_id)
    user = this_post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users')


@app.route('/tags')
def all_tags():
    """List of all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """Retrieve all Posts for Tag ID"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.taggedposts
    return render_template('tagdetail.html', tag=tag, posts=posts)


@app.route('/tags/new')
def new_tag():
    """GET tag form"""
    return render_template('addtag.html')


@app.route('/tags/new', methods=['POST'])
def new_tag_push():
    """POST tag to db"""
    name = request.form["tagname"]
    newtag = Tag(name=name)
    db.session.add(newtag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Edit specific tag"""
    tag = Post.query.get_or_404(tag_id)
    return render_template('edittag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def apply_tag_changes(tag_id):
    """Push tag changes to db"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['t_name']
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete tag from db"""
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect(f'/tags')
