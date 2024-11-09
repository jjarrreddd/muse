from flask import Flask, redirect, request, session, url_for, send_from_directory
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # You should set this to a secure key

# Spotify app credentials
CLIENT_ID = '5d8b3c44a9a54407806a8fa01c89167d'
CLIENT_SECRET = '8f1704d5370c427caef4d870da5beadd'
REDIRECT_URI = 'http://localhost:5000/callback'  # Update this if needed

@app.route("/login")
def login():
    # Redirect user to Spotify's authorization page
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user-read-private user-read-email"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Get the authorization code from the request
    code = request.args.get('code')
    
    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    token_data = response.json()
    access_token = token_data.get('access_token')
    
    # Store the access token in the session
    session['access_token'] = access_token

    return redirect('http://localhost:3000/welcome')

##########
@app.route("/welcome")
def welcome():
    # Check if user is logged in, after login, user is redirected back to page
    if 'access_token' not in session:
        return redirect(url_for('login'))

    # You can use the access token to make requests to the Spotify API here
    response = {
        "name": "morning (flask end)",
        "hello": "Hello World (flask end)"
    }
    
    return response

if __name__ == "__main__":
    app.run(debug=True)
