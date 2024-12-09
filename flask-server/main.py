import os
from dotenv import load_dotenv
import sys

from flask import Flask, session, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from urllib.parse import urlencode
import requests

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)   # generating on the fly, ideally a fixed string stored in environment variable
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
if not client_id or not client_secret:
    raise ValueError("Spotify Client ID and Secret must be set in environment variables.")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private' # gets us a users private playlists, to add 'playlist-read-private, streaming, etc'

# OAuth config
cache_handler = FlaskSessionCacheHandler(session) # tell spotipy to store the acess token in the Flask Session
sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = scope,
    cache_handler = cache_handler,
    show_dialog = True  # be able to see login with spotify
)
sp = Spotify(auth_manager=sp_oauth)

# redirect to auth page
@app.route('/login')  # homepage
@cross_origin()
def home():
    url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
    }
    auth_url = (f'{url}?{urlencode(params)}')
    return redirect(auth_url)

# callback and token exchange
@app.route('/callback', methods=['GET', 'POST'])
@cross_origin()
def callback():
   code = request.args.get('code')
#    print('code found', code, file=sys.stderr) # debug
   token_url = 'https://accounts.spotify.com/api/token'
   headers = {
       'Content-Type': 'application/x-www-form-urlencoded'
   }

   data = {
       'grant_type': 'authorization_code',
       'code': code,
       'redirect_uri': redirect_uri,
       'client_id': client_id,
       'client_secret': client_secret
   }

   response = requests.post(token_url, headers=headers, data=data)
   if response.status_code == 200:
       token_info = response.json()
       jsonify({'token_info': token_info})
       return redirect('http://localhost:3000/welcome')
   return jsonify({'error': 'Authorization failed'}), 400

# Search route
@app.route('/search', methods=['GET', 'POST'])
@cross_origin()
def search():
    # Authenticate account if no token is found
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        session['token_info'] = sp_oauth.get_cached_token()
        return redirect(auth_url)
    
    token_info = session.get('token_info')
    access_token = token_info['access_token']
    # If token is missing, redirect to login page
    if not token_info or 'access_token' not in token_info:
        return redirect(auth_url)
    access_token = token_info['access_token']

    sp = Spotify(auth=access_token)
    data = request.json
    query = data.get('query')

    # Searches query
    results = sp.search(q=query, type='track')

    if not results['tracks']['items']:
        return jsonify({'error': 'No track found'}), 404
    
    # Retrieves track info
    track = results['tracks']['items'][0]
    track_info = {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'id': track['id'],
        'url': track['external_urls']['spotify'],
    }

    # Obtains five recommended songs
    recommendations = sp.recommendations(
        seed_tracks = [data['track_id']],
        limit = 5,
        target_danceability = data.get('danceability', 0.5),
        target_energy = data.get('energy', 0.5),
        target_tempo = data.get('tempo', 120),
        target_valence = data.get('valence', 0.5)
    )

    # Compiles recommendations and grabs data about each
    recommendations_list = [
        {
            'name': rec['name'],
            'artist': rec['artists'][0]['name'],
            'url': rec['external_urls']['spotify'],
        }
        for rec in recommendations['tracks']
    ]

    return jsonify({
        'track_info': track_info,
        'recommendations': recommendations_list
    })

@app.route('/logout')
@cross_origin()
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)