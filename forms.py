from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, PasswordField, FileField
from wtforms.validators import InputRequired, Optional, URL, Email, EqualTo, ValidationError, Length
#from project import images

class NewUser(FlaskForm):

    username = StringField("Username:")

    password = PasswordField("Password:")

    reenter = PasswordField("Retype Password")

    email = StringField("Email:")

    bio = StringField("Bio:") #start with no bio add it on the profile page instead?

    #validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    profilepic = FileField("Profile Pic:") 

    background = FileField("Background Pic:")
    #location = StringField("General location:")



class Login(FlaskForm):
    username = StringField("Username:")

    password = StringField("Password:")

    
class PostPic(FlaskForm):

    title = StringField("Title of pic:")

    blurb = StringField("Description of kitty:")

    postimg = FileField("Post Kat Pic:")
    #tags

class UpdateUser(FlaskForm):

    username = StringField("Username:")

    password = PasswordField("Password:")

    email = StringField("Email:")

    profilepic = FileField("Profile Pic:")

    background_image = FileField("Backhground Pic:")

    bio = StringField("Bio:") 
