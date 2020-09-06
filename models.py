"""Models for cattinder"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

bcrypt = Bcrypt()
db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )


    bio = db.Column(
        db.Text,
    )

    filename_image = db.Column(db.Text)

    background_image = db.Column(db.Text)

    #reach goal is to add location
    # location = db.Column(
    #     db.Text,
    # )


    post = db.relationship('Post')

    #rating = db.relationship('Rating')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, password, email, bio,filename_image,background_image):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            bio = bio,
            filename_image = filename_image,
            background_image=background_image,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def checkpass(cls,username, password):
        user = cls.query.filter_by(username=username).first()
        is_auth = bcrypt.check_password_hash(user.password, password)
        if is_auth:
            return True
        return False


class Post(db.Model):
    """An cat profiles"""

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(50),
        nullable = False
    )
    text = db.Column(
        db.String(140),
        nullable=False,
    )

    postimg = db.Column(db.Text)

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.today()#datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')
    rating = db.relationship('Rating', backref = 'posts', uselist = False)


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)

    like= db.Column(db.Integer)#1meaning true

    dislike = db.Column(db.Integer)#0 meaning false

    comment = db.Column(db.Text)
    #tag? cute, hot or chubbby
    user_idd = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    post_idd = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='cascade')
    )
