from flask import render_template,request,redirect,url_for,flash,Blueprint,session,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from  PasswordVaultApp.forms import AddFolderForm
from PasswordVaultApp.models import User,Folder,PasswordEntry
from PasswordVaultApp.extensions import db
from cryptography.fernet import Fernet,InvalidToken
from flask import current_app
from PasswordVaultApp.encrypt import encrypt_password, decrypt_password

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashbd', methods=["GET"])
def db_home():
    #Getting the data of all the folders in the db to display in folder bar
    folders = Folder.query.all()
    #getting the folder_id of the selected folder and assigning it to the parameter
    selected_folder_id = request.args.get('folder_id', type=int)

    #if folder[s] exist
    if folders:
        #auto assigning first folder if none selected
        current_folder = Folder.query.get(selected_folder_id) if selected_folder_id else folders[0]
        #getting all passwords from the folder ie selected
        passwords = PasswordEntry.query.filter_by(folder_id=current_folder.id).all()
        fernet = Fernet(current_app.config['ENCRYPTION_KEY'])
        #list to store passwords after decrypting
        decrypted_passwords = []
        #pwd is accessing each passwd in passwords col from db and this var is used in dashboard.html 
        for pwd in passwords:
            try:
                decrypted_pwd = decrypt_password(pwd.password)
            except InvalidToken:
                decrypted_pwd = "❌ Invalid Key or Corrupted"
            decrypted_passwords.append({
                'id': pwd.id,
                'title': pwd.title,
                'username': pwd.username,
                'password': decrypted_pwd,
                'url': pwd.url
            })
    #If no folder created then None is displayed
    else:
        current_folder = None
        passwords = []

    folder_form = AddFolderForm()
    #debugging print statements
    print("Selected Folder ID:", selected_folder_id)
    print("Current Folder:", current_folder.name if current_folder else None)
    return render_template('dashboard.html',
                           folders=folders,
                           current_folder=current_folder,
                           passwords=decrypted_passwords,
                           folder_form=folder_form)

#This route helps in adding new folders 
@dashboard_bp.route('/add_folder', methods=["POST"])
def add_folder():
    # 'user' is the one ie defined in login route and contains the user.id
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    form = AddFolderForm()
    if form.validate_on_submit():
        #getting the user.id from session cookie and assigning it to user_id
        user_id = session.get('user')
        #creating a newfolder from the user_id and form details
        new_folder = Folder(name=form.folder_name.data, user_id=user_id)
        db.session.add(new_folder)
        db.session.commit()
        flash('Folder created successfully!')
    
    return redirect(url_for('dashboard.db_home'))



#This route is used to delete the folder
@dashboard_bp.route('/delete_folder/<int:folder_id>', methods=["POST"])
def delete_folder(folder_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    folder = Folder.query.get_or_404(folder_id)#.get_or_404 is like query.get command but returns
    # error 404 incase no valid data is found
    db.session.delete(folder)
    db.session.commit()
    flash('Folder deleted.')
    return redirect(url_for('dashboard.db_home'))


#This route is used to add passwds like we write notes
@dashboard_bp.route('/create_password', methods=['POST'])
def create_password():
    if 'user' not in session:
        #This route is called from JavaScript (fetch()), so it doesn’t use a browser redirect.
        return jsonify({'status': 'unauthorized'}), 401
    #  Gets the data from the post request ie nothing but the form which we use to create a passwd
    #  tile and store its data in dictionary form in data
    data = request.get_json()
    folder_id = data.get('folder_id')
    encrypted_password = encrypt_password(data['password'])
    new_entry = PasswordEntry(
        title=data['title'],
        username=data['username'],
        password=encrypted_password,
        url=data.get('url'),
        folder_id=folder_id
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'status': 'success', 'id': new_entry.id})


#This route is used to edit created password
@dashboard_bp.route('/update_password/<int:id>', methods=['POST'])
def update_password(id):
    if 'user' not in session:
        return jsonify({'status': 'unauthorized'}), 401
    #gets the json data ie passed on submit via js in dashboard.html
    data = request.get_json()
    #gets the id passed into the parameter via the hiddenfield editentryid which is obtained from
    #password tile's password db and then Queries the database for a PasswordEntry record with
    #  the given id
    entry = PasswordEntry.query.get_or_404(id)
    entry.title = data.get('title')
    entry.username = data.get('username')
    # user is allowed to leave the password field empty if they don’t want to change it.
    # This if condition ensures:
    # You only update the password if the user entered something new.
    # You don't accidentally overwrite the password with an empty string.
    if data.get('password'):
        entry.password = encrypt_password(data['password'])
    entry.url = data.get('url')
    db.session.commit()
    return jsonify({'status': 'success'})

#Delete Passwords Route
@dashboard_bp.route('/delete_password/<int:entry_id>', methods=["DELETE"])
def delete_password(entry_id):
    if 'user' not in session:
        return jsonify({'status': 'unauthorized'}), 401

    entry = PasswordEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"status": "success", "message": "Password deleted"})

#My Account Route
@dashboard_bp.route('/account')
def account():
    user_id = session.get('user')  # or session.get('user_id'), depending on what you stored
    if not user_id:
        flash("You are not logged in.")
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('auth.login'))

    return render_template('account.html', user=user)

@dashboard_bp.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user']
    user = User.query.get(user_id)

    # Delete all associated folders & passwords first
    for folder in user.folders:
        db.session.delete(folder)

    db.session.delete(user)
    db.session.commit()

    session.pop('user', None)
    flash("Your account has been deleted.", "info")
    return redirect(url_for('auth.login'))
