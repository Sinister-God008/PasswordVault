import hashlib
import re
import requests
#This class encapsulates the password checking methods lyk rating,passwd strength,breaches.
class Test_passwd:
    def __init__(self, password):
        self.password = password
        self.strength = 0
#This method checks if the password has been breached already in some other reported breaches
#of the past.
    def check_psswd(self):
        #it encodes the enterred password to sha1
        #format and converts it into uppercase for comparing it with the data fetched from the api.
        hash_1 = hashlib.sha1(self.password.encode()).hexdigest().upper()
        #what we are doing here is splitting the hash_code generated from the above command and passing
        # the first 5 characters of the password to the prefix variable ie passed to the api server
        #to check for breach and maintain the security of the password passed by sending only part of it.
        prefix, suffix = hash_1[:5], hash_1[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": "Error fetching data from HIBP API"}

        hashes = (line.split(':') for line in response.text.splitlines())
        breached = any(suffix == h for h, _ in hashes)

        return {"breached": breached}
    #This method here checks and calculates the strength of the password provided by the user.
    def check_password_strength(self):
        #Check the strength of a password based on length and complexity.
        if len(self.password) >= 8:
            self.strength += 1
        #Checks if password has any uppercase character
        if re.search(r"[A-Z]", self.password):
            self.strength += 1
        #Checks if password has any lowercase character
        if re.search(r"[a-z]", self.password):
            self.strength += 1
        #Checks if password has any digit between 0-9
        if re.search(r"\d", self.password):
            self.strength += 1
        #Checks if password has any pattern passed in the list
        if re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/\\|`~-]", self.password):
            self.strength += 1
#This method provides the final rating as per the strength calculated by the above method.
    def rating(self):
        ratings = {
            5: "Very Strong 💪",
            4: "Strong 🙂",
            3: "Moderate 😐",
            2: "Weak 😟",
            1: "Very Weak 🚨",
            0: "Extremely Weak 🚨🚨"
        }
        return ratings.get(self.strength, "Unknown")
   