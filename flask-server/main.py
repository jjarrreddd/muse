import os

from flask import Flask, session, request, redirect, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)   #generating on the fly, ideally a fixed string stored in environment variable

client_id = '5d8b3c44a9a54407806a8fa01c89167d' # would be best to secure in environment variables or secure credentials store
client_secret = '8f1704d5370c427caef4d870da5beadd' #
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private' # gets us a users private playlists, to add 'playlist-read-private, streaming, etc'

cache_handler = FlaskSessionCacheHandler(session) # tell spotipy to store the acess token in the Flask Session
sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = scope,
    cache_handler = cache_handler,
    show_dialog = True  # be able to see login with spotify
)
sp = Spotify(auth_manager = sp_oauth)

@app.route('/')  # homepage
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code']) # user wont need to continuosly need to login
    return redirect(url_for('get_playlists'))    

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): # ideally extract into its own method, validates token is still valid, not expired
        auth_url = sp_oauth.get_authorize_url()        
        return redirect(auth_url)
    
    playlists = sp.current_user_playlists() # getting the playlists
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']] # all playlist info
    playlists_html = '<br>'.join([f'{name}: {url}' for name, url in playlists_info])

    return playlists_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

############ADD /Welcome


if __name__ == '__main__':
    app.run(debug=True)
