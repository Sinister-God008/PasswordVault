from flask import Blueprint,session,render_template,redirect,request,jsonify,url_for
import requests
import hashlib
import re
HIBP_API_URL = "https://haveibeenpwned.com/api/v3/breaches"
#This headers dictionary is used to verify the api that the request is being made by a legit and authorised user with a proper api_key to allow the api server to check for the data asked (here) it is the info about the breaches(as mentioned in the above url)
HEADERS = {"User-Agent": "CyberSafeApp", "hibp-api-key": "YOUR_API_KEY_HERE"}
breach_bp=Blueprint('Breach_data',__name__)
@breach_bp.route("/breachdata")  # Load the page first WITHOUT breach data
def breach():
    return render_template("breach_2.html")
breachpwnedapi_bp=Blueprint('Breach_pwned',__name__)
@breachpwnedapi_bp.route("/get_breach_data")  # API route to fetch breach data dynamically
def get_breach_data():
    #This is used to show the breach data available on the HaveIBeenPwned API on the website.
    response = requests.get(HIBP_API_URL, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())  # Send JSON response to frontend
    else:
        return jsonify([])  # Return empty list if API fails