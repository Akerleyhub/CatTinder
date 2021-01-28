"""Cat tinder logic"""

from flask import Flask, redirect,request,render_template, session, flash, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from models import db, connect_db, User, Post, Rating
from forms import NewUser, Login, PostPic, UpdateUser
from werkzeug.exceptions import Unauthorized
from datetime import datetime, timedelta
import os
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug import secure_filename, FileStorage
from sqlalchemy.exc import IntegrityError
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///cattinder')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY","meow")
debug = DebugToolbarExtension(app)

CURR_USER_KEY = "curr_user"
#SET FLASK_ENV=development
app.debug = True
connect_db(app)
db.create_all()

app.config['UPLOADED_PHOTOS_DEST'] = "static"
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
#g.user.id refers to the global current logged in user
#login/logout user,create account

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user by adding userid to the session"""
    session[CURR_USER_KEY] = user.id

@app.route('/<int:id>')
def home(id):
    user = User.query.get_or_404(g.user.id)
    #will get a random post in the db
    num = random.randint(1,Post.query.count())
    posty = Post.query.get_or_404(num)
    useridpost = posty.user_id
    userpost = User.query.get(useridpost)
    r = User.query.filter((Rating.user_idd == user.id)&(Rating.post_idd == posty.id)).first()
    try:
        #if the user has liked it in the past it wont show
        #also wont show if it is the users own post
        if r or posty.user_id == user.id:
            return redirect(f'/{user.id}')
    except IntegrityError:
        flash("you've seen all other cats", 'danger')
        return render_template('errorpage.html')    
    else:
        print(posty.postimg[0:4])
        return render_template('home.html', user = user, posty=posty, userpost=userpost)
@app.route('/newuser', methods = ['GET','POST'])
def createUser():
    '''Will create a new user and add their background/profile pic to static folder'''
    form = NewUser()
    if form.validate_on_submit():
        try:
            if form.password.data != form.reenter.data:
                raise ValueError
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                bio = form.bio.data,
                filename_image = photos.save(form.profilepic.data),
                background_image = photos.save(form.background.data),
            )
            #will save photos to static folder
            db.session.commit()

        except IntegrityError:
            flash("Info is not correctly filled", 'danger')
            return render_template('createuser.html', form = form)
        except ValueError:
            flash("Password must match", 'danger')
            return render_template('createuser.html', form = form)

        do_login(user)
        #adds user to global
        add_user_to_g()

        return redirect(f"/{g.user.id}")

    else:
        return render_template('createuser.html', form = form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login."""
    form = Login()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            add_user_to_g()
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/{g.user.id}")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handles logout of user. Simplely clears session of userid"""
    session.clear()
    return redirect("/newuser")

####################################################################################
############################# Get/Handle Post ######################################
@app.route('/<int:id>/newpost', methods=['GET','POST'])
def newpost(id):
    '''Allows user to create a post. Also will save image to static'''
    form = PostPic()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        npost = Post(title = form.title.data,
                    text = form.blurb.data,
                    postimg = photos.save(form.postimg.data),
                    user_id = user.id)

        db.session.add(npost)
        db.session.commit()
        return redirect(f'/{user.id}')

    else:
        return render_template('createpost.html', form = form, user = user)

@app.route('/like/<int:postid>')
def likepost(postid):
    user = User.query.get(g.user.id)
    post = Post.query.get(postid)

    newrating = Rating(like = 1, user_idd = user.id, post_idd = post.id)
    db.session.add(newrating)
    db.session.commit()
    #user likes then it goes to match route and then to matches will redirect if not
    return redirect(f'/{user.id}/match')

@app.route('/dislike/<int:postid>')
def dislikepost(postid):
    user = User.query.get(g.user.id)
    post = Post.query.get(postid)

    newrating = Rating(dislike = 1, user_idd = user.id, post_idd = post.id)
    db.session.add(newrating)
    db.session.commit()

    return redirect(f'/{user.id}')


######################### PROFILE ############################

@app.route('/<int:id>/profile')
def profile(id):
    user = User.query.get(id)
    return render_template('profile.html', user = user)

#make a route to update existing information
@app.route('/<int:id>/update', methods = ["GET","POST"])
def updateprofile(id):
    '''Update existing user'''
    form = UpdateUser()
    uid = User.query.get_or_404(id)

    if form.validate_on_submit():
        try:
            password=form.password.data
            person = User.checkpass(g.user.username, password)

            if person:
                uid.username=form.username.data,
                uid.password=password,
                uid.email=form.email.data,
                uid.bio = form.bio.data,
                uid.filename_image = form.profilepic.data,
                uid.background_image = form.background_image.data,
                #wouldn't let me save the new img
                #photos.save(form.profilepic.data)

            
                db.session.commit()
        #need to catch if wrong passwword
        except IntegrityError:
            flash("Username already taken", 'danger')
            return redirect(f'/{g.user.id}/update')

        return redirect(f'/{g.user.id}/profile')
    #else:
    return render_template('update.html', form = form, uid = uid)

@app.route('/user/delete', methods=["GET","POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(g.user)
    db.session.commit()
    session.clear()

    return redirect("/newuser")

##################### MATCHING LOGIC #######################
@app.route('/<int:id>/matches')
def matches(id):
    if match == True:
        user = User.query.get(id)
        check = Rating.query.order_by(Rating.id.desc()).first()
        addtomatches = check.post_idd
        postthatwasliked = Post.query.get_or_404(addtomatches)
        user2id = postthatwasliked.user_id
        user2 = User.query.get(user2id)
        print('----------------')
        print(user2)
        print('----------------')
        flash("It's a match!")
        return render_template('matches.html', user2 = user2)

@app.route('/<int:id>/match')
def matched(id):
    global match
    match = False
    user = User.query.get(id)
    #check will get the rating of the last post that was liked
    check = Rating.query.order_by(Rating.id.desc()).first()

    #get user2's id based off the post liked
    user2post = Post.query.get(check.post_idd)
    user2 = User.query.get(user2post.user_id)
    #likes of both the users
    user1posts = Post.query.filter((Post.user_id == user.id)&(Rating.like == 1)).all()
    user2likes = Rating.query.filter((Rating.user_idd == user2.id)&(Rating.like == 1)).all()

    #searches in user2's likes for user1's post
    #if it exists the post will be added to matches
    for m in user2likes:
        for n in user1posts:
            if m.post_idd == n.id:
                print("its a match!")
                match = True
                return redirect(f'/{user.id}/matches')
    return redirect(f'/{id}')
