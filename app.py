
from flask import Flask, redirect, render_template, request, flash
from models import db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nothing so secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.app = app
db.init_app(app)


@app.route('/')
def show_users():
    """display list of all the users in the database"""

    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/add_user')
def show_user_form():
    """show the add new user form"""

    return render_template('add_user.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    """adding a new user to the app"""

    first = request.form.get('first_name')
    last = request.form.get('last_name')
    image = request.form.get('image_url')

    new_user = User(first_name = first, last_name = last, image_url = image)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>')
def show_user_detials(user_id):
    """displaying detials of a user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/edit_user/<int:user_id>')
def show_edit_form(user_id):
    """displaying edit form of a user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user, user_id=user_id)

@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    """editing a user information"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url')

    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    """deleting a user from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/add_post/<int:user_id>')
def show_post_form(user_id):
    """display post form"""
    
    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template('add_post.html', user=user, tags=tags)

@app.route('/add_post/<int:user_id>', methods=['POST'])
def add_post(user_id):
    """adding a new post for a user"""

    # user = User.query.get_or_404(user_id)
    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(title = title, content = content, user_id=user_id)
    tag_ids = [int(num) for num in request.form.getlist('checkboxes')]
    new_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/{user_id}")

@app.route('/post/<int:post_id>')
def show_post_detail(post_id):
    """displaying a post detials"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@app.route('/edit_post/<int:post_id>')
def show_edit_post(post_id):
    """displaying edit form of a user"""

    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post = post, tags=tags)

@app.route('/edit_post/<int:post_id>', methods=['POST'])
def edit_post(post_id):
    """editing a user's post """

    post = Post.query.get_or_404(post_id)

    post.title = request.form.get('title')
    post.content = request.form.get('content')
    post.user_id = post.users.id

    tag_ids = [int(num) for num in request.form.getlist('checkboxes')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/{post.users.id}")

@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    """deleting a user post from the database"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'post: {post} deleted.')
    return redirect(f"/{post.user_id}")


@app.route('/tags')
def show_tags():
    """show a list of all of the tags"""

    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/add_tag')
def show_tag_form():
    """display a form to add a new tag"""

    posts = Post.query.all()
    return render_template('add_tag.html', posts=posts)


@app.route('/add_tag', methods=['POST'])
def add_tag():
    """adding the new tag into the database"""

    name = request.form.get('name')
    new_tag = Tag(name=name)

    post_ids = [int(num) for num in request.form.getlist('checkboxes')]
    new_tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tag_details/<int:tag_id>')
def tag_details(tag_id):
    """show tag details and how many posts are tagged"""

    tag = Tag.query.get(tag_id)
    return render_template('tag_details.html', tag = tag)

@app.route('/edit_tag/<int:tag_id>')
def show_edit_tag(tag_id):
    """editing a tag"""

    posts = Post.query.all()
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/add_tag/<int:tag_id>', methods=['POST'])
def edit_tag(tag_id):
    """saving the edited tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form.get('name')

    post_ids = [int(num) for num in request.form.getlist('checkboxes')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/delete_tag/<int:tag_id>')
def delete_tag(tag_id):
    """deleting a tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')



