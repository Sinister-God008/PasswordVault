from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,HiddenField
from wtforms.validators import DataRequired,Email,Length,EqualTo,URL
class RegistrationForm(FlaskForm):
  username=StringField('Username',validators=[DataRequired(message="The username cannot be empty"),
                                              Length(min=2,max=22)])
  email=StringField('Email',validators=[DataRequired(),Email()])
  password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
  confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message=
  "Password must match")])
  submit=SubmitField("Sign Up")
  
class LoginForm(FlaskForm):
  username=StringField('Username',validators=[DataRequired(),Length(min=2,max=22)])
  password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
  submit=SubmitField("Log In")

class ForgotPasswordForm(FlaskForm):
  username=StringField('Username',validators=[DataRequired(),Length(min=2,max=22)])
  n_password=PasswordField('New Password',validators=[DataRequired(),Length(min=8)])
  confirm_n_password=PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('n_password',message=
  "Password must match")])
  submit = SubmitField('Reset Password')

class AddFolderForm(FlaskForm):
  folder_name=StringField('Foler Name',validators=[DataRequired(),Length(min=4,max=50)])
  submit=SubmitField('Create Folder')


