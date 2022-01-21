"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class User(db.Model):
    """creating a user info table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    first_name = db.Column(db.String(30), nullable = False, unique = True)
    last_name = db.Column(db.String(30), nullable = False)
    image_url = db.Column(db.Text, nullable= True, default = None)

    posts = db.relationship('Post', backref='users', cascade="all, delete-orphan")


    def __repr__(self):
        return f'<User id={self.id}, first={self.first_name}, last={self.last_name}>'

class Post(db.Model):
    """creating a Post Model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.Date, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    posts_tags = db.relationship('PostTag', backref='posts', cascade='all,delete-orphan')

    def __repr__(self):
        return f'<Post id={self.id}, title={self.title}, content={self.content}>'


class Tag(db.Model):
    """creating a tage model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


    def __repr__(self):
        return f'<Tag id={self.id}, name={self.name}>'


class PostTag(db.Model):
    """creating a model for posts and tags"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        return f'<PostTag post_id={self.post_id}, tag_id={self.tag_id}>'
