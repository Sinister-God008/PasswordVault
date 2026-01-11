from flask import Blueprint,session,render_template,redirect,request,jsonify,url_for
from PasswordVaultApp.passwd_funcn.testpswdclass import Test_passwd
checkp_bp=Blueprint('check_p',__name__)
@checkp_bp.route("/check_p",methods=['POST']) #API route to check password strength
def check_p():
        #this is used for creating an obj/variable to store the incoming data from the user via http.
        data = request.json
        #This is used to get the password enterred by the user in the webapps frontend.
        password = data.get("password")
        if not password:
            return jsonify({"error": "Password cannot be empty."})
        #checking the password security and breaches from the test_passwd class
        tester = Test_passwd(password)
        breach_result = tester.check_psswd()
        tester.check_password_strength()
        strength_rating = tester.rating()
        if "error" in breach_result:
            return jsonify({"error": breach_result["error"]}), 500
        return jsonify({
            
            "breached": "Yes" if breach_result["breached"] else "No",
            "strength": strength_rating
        })