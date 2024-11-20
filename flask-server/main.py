import os

from flask import Flask, session, request, redirect, url_for, render_template_string

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

#####################################################
#Lines 33 - 35 into method, used in almost all paths

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
    return redirect(url_for('welcome'))  #     return redirect(url_for('get_playlists'))  

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    if request.method == 'POST':
        query = request.form.get('song_query')
        results = sp.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'url': track['external_urls']['spotify'],
                'id': track['id']
            }

            # Fetch audio features for the track
            audio_features = sp.audio_features(track_info['id'])[0]
            if audio_features:
                track_info.update({
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'tempo': audio_features['tempo'],
                    'valence': audio_features['valence']
                })

                # Get song recommendations based on these features
                recommendations = sp.recommendations(
                    seed_tracks=[track_info['id']],
                    limit=5,
                    target_danceability=audio_features['danceability'],
                    target_energy=audio_features['energy'],
                    target_tempo=audio_features['tempo'],
                    target_valence=audio_features['valence']
                )

                recommendations_list = [
                    {
                        'name': rec['name'],
                        'artist': rec['artists'][0]['name'],
                        'url': rec['external_urls']['spotify']
                    }
                    for rec in recommendations['tracks']
                ]

                return render_template_string('''
                    <h1>Search Results</h1>
                    <p><strong>Song:</strong> {{ track_info['name'] }}</p>
                    <p><strong>Artist:</strong> {{ track_info['artist'] }}</p>
                    <p><strong>Album:</strong> {{ track_info['album'] }}</p>
                    <p><a href="{{ track_info['url'] }}" target="_blank">Listen on Spotify</a></p>
                    <h2>Audio Features:</h2>
                    <ul>
                        <li><strong>Danceability:</strong> {{ track_info['danceability'] }}</li>
                        <li><strong>Energy:</strong> {{ track_info['energy'] }}</li>
                        <li><strong>Tempo:</strong> {{ track_info['tempo'] }} BPM</li>
                        <li><strong>Valence:</strong> {{ track_info['valence'] }}</li>
                    </ul>
                    <h2>Recommended Songs:</h2>
                    <ul>
                        {% for rec in recommendations_list %}
                            <li>
                                <strong>{{ rec['name'] }}</strong> by {{ rec['artist'] }} -
                                <a href="{{ rec['url'] }}" target="_blank">Listen on Spotify</a>
                            </li>
                        {% endfor %}
                    </ul>
                    <a href="/welcome">Search Again</a>
                ''', track_info=track_info, recommendations_list=recommendations_list)
        else:
            return render_template_string('''
                <h1>No results found for your query.</h1>
                <a href="/welcome">Search Again</a>
            ''')

    return render_template_string('''
        <h1>Welcome to Spotify Song Finder</h1>
        <form method="POST">
            <input type="text" name="song_query" placeholder="Search for a song..." required>
            <button type="submit">Search</button>
        </form>
    ''')



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
