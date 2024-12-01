import os
from dotenv import load_dotenv

from flask import Flask, session, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from urllib.parse import urlencode
import requests

import sys

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)   #generating on the fly, ideally a fixed string stored in environment variable
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

client_id = os.getenv('CLIENT_ID') # would be best to secure in environment variables or secure credentials store
client_secret = os.getenv('CLIENT_SECRET') #
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
   print('code found', code, file=sys.stderr) # debug
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

@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        session['token_info'] = sp_oauth.get_cached_token()
        return redirect(auth_url)
    
    token_info = session.get('token_info')
    access_token = token_info['access_token']
    if 'access_token' not in session:
        return redirect('http://localhost:3000/welcome')
    
    sp = Spotify(auth=access_token)
    # data = request.json
    # query = data.get('query')
    # results = sp.search(q=query, type='track')
    results = sp.current_user_top_tracks(limit=5)

    if not results['tracks']['items']:
        return jsonify({'error': 'No track found'}), 404
    
    track = results['tracks']['items'][0]
    track_info = {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'id': track['id'],
        'url': track['external_urls']['spotify'],
    }
    return jsonify(track_info)

@app.route('/recommendations', methods=['POST'])
@cross_origin()
def recommendations():
    token_info = session.get('token_info')
    access_token = token_info['access_token']
    if not token_info:
        return jsonify({'error': 'User not authenticated'}), 401
    
    sp = Spotify(auth=access_token)
    data = request.json

    recommendations = sp.recommendations(
        seed_tracks = [data['track_id']],
        limit = 5,
        target_danceability = data.get('danceability', 0.5),
        target_energy = data.get('energy', 0.5),
        target_tempo = data.get('tempo', 120),
        target_valence = data.get('valence', 0.5)
    )

    results = [
        {
            'name': rec['name'],
            'artist': rec['artists'][0]['name'],
            'url': rec['external_urls']['spotify'],
        }
        for rec in recommendations['tracks']
    ]
    return jsonify(results)

@app.route('/token', methods=['POST'])
@cross_origin()
def getToken():
    token_info = session.get('token_info')
    if token_info and not sp_oauth.is_token_expired(token_info):
        return jsonify(token_info)
    else:
        return jsonify({"error": "token missing"}), 401

# @app.route('/welcome', methods=['GET', 'POST'])
# @cross_origin()
# def welcome():
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
    
#     if request.method == 'POST':
#     # Get values from form
#         query = request.form.get('song_query')
#         target_danceability = float(request.form.get('danceability', 0.5))
#         target_energy = float(request.form.get('energy', 0.5))
#         target_tempo = float(request.form.get('tempo', 120))
#         target_valence = float(request.form.get('valence', 0.5))

#         # Search for a song
#         results = sp.search(q=query, type='track', limit=1)
#         if results['tracks']['items']:
#             track = results['tracks']['items'][0]
#             track_info = {
#                 'name': track['name'],
#                 'artist': track['artists'][0]['name'],
#                 'album': track['album']['name'],
#                 'url': track['external_urls']['spotify'],
#                 'id': track['id']
#             }

#             # Get recommendations based on input attributes
#             recommendations = sp.recommendations(
#                 seed_tracks=[track_info['id']],
#                 limit=5,
#                 target_danceability=target_danceability,
#                 target_energy=target_energy,
#                 target_tempo=target_tempo,
#                 target_valence=target_valence
#             )

#             recommendations_list = [
#                 {
#                     'name': rec['name'],
#                     'artist': rec['artists'][0]['name'],
#                     'url': rec['external_urls']['spotify']
#                 }
#                 for rec in recommendations['tracks']
#             ]

#             return jsonify({
#                 'track_info': track_info,
#                 'recommendations': recommendations_list
#             })
        
#         else:
#             return jsonify({'No results found for your query.'})

#     # return render_template_string('''
#     #     <h1>Welcome to Spotify Song Finder</h1>
#     #     <form method="POST">
#     #         <input type="text" name="song_query" placeholder="Search for a song..." required>
#     #         <label for="danceability">Danceability (0.0 - 1.0):</label>
#     #         <input type="range" name="danceability" min="0.0" max="1.0" step="0.1" value="0.5">
#     #         <label for="energy">Energy (0.0 - 1.0):</label>
#     #         <input type="range" name="energy" min="0.0" max="1.0" step="0.1" value="0.5">
#     #         <label for="tempo">Tempo (BPM):</label>
#     #         <input type="range" name="tempo" min="60" max="200" step="1" value="120">
#     #         <label for="valence">Valence (0.0 - 1.0):</label>
#     #         <input type="range" name="valence" min="0.0" max="1.0" step="0.1" value="0.5">
#     #         <button type="submit">Search</button>
#     #     </form>
#     # ''')




@app.route('/get_playlists')
@cross_origin()
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): # ideally extract into its own method, validates token is still valid, not expired
        auth_url = sp_oauth.get_authorize_url()        
        return redirect(auth_url)
    
    playlists = sp.current_user_playlists() # getting the playlists
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']] # all playlist info
    playlists_html = '<br>'.join([f'{name}: {url}' for name, url in playlists_info])

    return playlists_html

@app.route('/logout')
@cross_origin()
def logout():
    # session.clear()
    return redirect('/')

############ADD /Welcome


if __name__ == '__main__':
    app.run(debug=True)
