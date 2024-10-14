# spotify authentication test file
# pip install requests spotipy

from flask import Flask, session
import requests
import json
import os

from spotipy import Spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Spotify App Credentials
REDIRECT_URI = 'https://localhost:3000/callback'
SCOPE = 'user-read-email user-read-private'
CLIENT_ID = '1e0a0d72562e427bbd72753d13924626'
CLIENT_SECRET = 'b8f24873f1514e118ff8b9af4b5a3f54'

# Endpoints
API_BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/authorize/?'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

CACHE_HANDLER = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    REDIRECT_URI = REDIRECT_URI,
    SCOPE = SCOPE,
    CLIENT_ID = CLIENT_ID,
    CLIENT_SECRET = CLIENT_SECRET,
    CACHE_HANDLER = CACHE_HANDLER,
    show_dialog = True
)

@app.route('/login')
def login():
    # Redirect to Spotify for authentication
    auth_parameters = f"{AUTH_URL}response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_parameters)

@app.route('/callback')
def callback():
    # Handle callback after authentication
    auth_code = request.args.get('code')
    auth_token = get_token(auth_code)
    session['auth_token'] = auth_token
    return redirect(url_for('profile'))

def get_token(auth_code):
    # Exchange authorization for access token
    info = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=info)
    token_info = response.json()
    return token_info['access_token']

@app.route('/profile')
def profile():
    # Get user profile information with access token
    headers = {
        'Authorization': f'Bearer {session["auth_token"]}'
    }

    profile_response = requests.get(API_BASE_URL + 'me', headers=headers)
    profile_data = profile_response.json()
    return f"{profile_data['display_name']} {profile_data['email']}"

if __name__ == '__main__':
    app.run(debug=True)