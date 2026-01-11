from flask import render_template,request,redirect,url_for,flash,Blueprint,session
from werkzeug.security import generate_password_hash,check_password_hash
from  PasswordVaultApp.forms import RegistrationForm,LoginForm,ForgotPasswordForm
from PasswordVaultApp.models import User
from PasswordVaultApp.extensions import db
auth_bp=Blueprint('auth',__name__)

@auth_bp.route("/register",methods=['GET','POST'])
def register():
  form=RegistrationForm()
  if form.validate_on_submit():
    username=form.username.data
    email = form.email.data
    password = form.password.data
    hashed_password = generate_password_hash(password)
    #This line creates a new instance of the User model using the form data you got from the user.
    new_user = User(username=username, email=email, password=hashed_password)
    #adds the new_user data to the session
    db.session.add(new_user)
    #this writes the changes permanently to the model
    db.session.commit()
    flash(f"Welcome {username}! Your Registration was successful.")
    return redirect(url_for('auth.login'))
  return render_template('register.html',form=form)

@auth_bp.route("/login",methods=['GET','POST'])
def login():
  form=LoginForm()
  session.pop('_flashes', None)
  if form.validate_on_submit():
    username=form.username.data
    password = form.password.data
    user=User.query.filter_by(username=form.username.data).first()
    #These print statements are written to debug the code and check what is failing
    print("Form validated:", form.validate_on_submit())
    print("Username entered:", username)
    print("User from DB:", user)
    #check_password_hash func is defined in werkzeug library to compare unhashed password with its hashed
    #password which is needed to validate during login.
    #if user else none is to handle cases where the login details are not in db
    print("Password match:", check_password_hash(user.password, password) if user else None)
    if user and check_password_hash(user.password,password):
      #this 'user' is also used in dashboard file to access user_id
      session['user']=user.id#Remember this user between requests by saving their id in the session
      flash("Login Successful!",'success')
      return redirect(url_for('dashboard.db_home'))
    else:
      flash("Invalid username or password",'danger')
  return render_template("login.html",form=form)

@auth_bp.route("/forgot-password",methods=["GET","POST"])
def forgot():
  form= ForgotPasswordForm()
  if form.validate_on_submit():
    #getting the username details entered in the forgotpassword form by the user
    username=form.username.data
    #validating the above username by passing it to the User db and access its data  
    user=User.query.filter_by(username=username).first()
        #These print statements are written to debug the code and check what is failing
    print("Form validated:", form.validate_on_submit())
    print("Username entered:", username)
    print("User from DB:", user)
    if user:
      #access the password enterred by the user in forgot form and hash it
      n_paswd=form.n_password.data
      hashed_psswd=generate_password_hash(n_paswd)
      print("Hash Password Generated")
      #passing the new password from the form and updating it in the db for that username
      user.password=hashed_psswd
      #committing the changes
      db.session.commit()
      print("Password Updated")
      flash(f"The Password Has Been Updated!!","success")
      return redirect(url_for("auth.login"))
    else:
      print("Password Updation Failed!!")
      flash(f"No user exists with the {username} in the database!!","danger")
  return render_template("forgot_pass.html",form=form)

@auth_bp.route("/logout")
def logout():
  session.pop('user',None)
  flash("LOG OUT SUCCESSFUL!!",'info')
  return redirect(url_for("auth.login"))