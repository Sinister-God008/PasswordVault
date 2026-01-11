from flask import Blueprint,session,render_template,redirect,request,jsonify,url_for
home_bp=Blueprint('home',__name__)
@home_bp.route('/')
def home():
    return render_template('home_passwd_checker.html')