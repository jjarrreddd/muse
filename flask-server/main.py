import os
<<<<<<< Updated upstream

from flask import Flask, session, request, redirect, url_for, render_template_string

=======
import 'C:\Users\funko\OneDrive\Documents\GitHub\muse\front-end\src\components\style.css';
from flask import Flask, session, request, redirect, url_for, render_template_string, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
>>>>>>> Stashed changes
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong secret key
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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

# Mock database with hashed passwords
USERS = {
    "admin": bcrypt.generate_password_hash("password123").decode('utf-8'),
    "user1": bcrypt.generate_password_hash("mypassword").decode('utf-8'),
}


# Helper Functions
def is_authenticated():
    """Check if the user is authenticated with Spotify."""
    return sp_oauth.validate_token(cache_handler.get_cached_token())


def get_auth_url():
    """Generate Spotify authorization URL."""
    return sp_oauth.get_authorize_url()


# Routes
@app.route('/')
def home():
    """Homepage: Redirects to Spotify login if not authenticated."""
    if not is_authenticated():
        return redirect(get_auth_url())
    return redirect(url_for('get_playlists'))


@app.route('/callback')
def callback():
    """Spotify OAuth callback: Handles user login and access token."""
    try:
        sp_oauth.get_access_token(request.args['code'])
        return redirect(url_for('welcome'))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    """
    Welcome Page: Search for songs and view recommendations.
    """
    if not is_authenticated():
        return redirect(get_auth_url())

    if request.method == 'POST':
        query = request.form.get('song_query')
        try:
            # Fetching Spotify Track Recommendations based on input
            target_danceability = float(request.form.get('danceability', 0.5))
            target_energy = float(request.form.get('energy', 0.5))
            target_tempo = float(request.form.get('tempo', 120))
            target_valence = float(request.form.get('valence', 0.5))

            # Search for a song on Spotify
            results = sp.search(q=query, type='track', limit=1)
            if not results['tracks']['items']:
                return render_template_string('''
                    <div class="container">
                        <h1>No results found for your query.</h1>
                        <a href="/welcome">Search Again</a>
                    </div>
                ''')

            # Fetch song details
            track = results['tracks']['items'][0]
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'url': track['external_urls']['spotify']
            }

            # Get recommendations
            recommendations = sp.recommendations(
                seed_tracks=[track['id']],
                limit=5,
                target_danceability=target_danceability,
                target_energy=target_energy,
                target_tempo=target_tempo,
                target_valence=target_valence
            )

            # Generate recommendations list
            recommendations_list = [
                {
                    'name': rec['name'],
                    'artist': rec['artists'][0]['name'],
                    'url': rec['external_urls']['spotify']
                } for rec in recommendations['tracks']
            ]

            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Spotify Song Finder</title>
                    <style>
                        body {
                            font-family: 'Arial', sans-serif;
                            background-color: #f4f4f9;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                        }

                        .container {
                            background: #ffffff;
                            padding: 30px;
                            border-radius: 12px;
                            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                            width: 90%;
                            max-width: 700px;
                            text-align: center;
                        }

                        h1 {
                            color: #333;
                            font-size: 28px;
                            margin-bottom: 20px;
                        }

                        form, .results {
                            display: flex;
                            flex-direction: column;
                            gap: 20px;
                        }

                        input[type="text"], input[type="range"] {
                            width: 100%;
                            padding: 10px;
                            border: 1px solid #ddd;
                            border-radius: 6px;
                            font-size: 16px;
                        }

                        label {
                            font-size: 14px;
                            color: #555;
                            text-align: left;
                        }

                        button {
                            background-color: #007bff;
                            color: white;
                            border: none;
                            padding: 12px;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 16px;
                            transition: background-color 0.3s;
                        }

                        button:hover {
                            background-color: #0056b3;
                        }

                        ul {
                            list-style: none;
                            padding: 0;
                            margin: 0;
                        }

                        ul li {
                            padding: 10px;
                            background-color: #f9f9f9;
                            border: 1px solid #eee;
                            border-radius: 6px;
                            margin-bottom: 10px;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        }

                        ul li a {
                            text-decoration: none;
                            color: #007bff;
                            font-weight: bold;
                        }

                        ul li a:hover {
                            text-decoration: underline;
                        }

                        .results-header {
                            text-align: left;
                            margin-bottom: 20px;
                        }

                        @media (max-width: 768px) {
                            .container {
                                width: 95%;
                            }
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Spotify Song Finder</h1>
                        <div class="results-header">
                            <p><strong>Song:</strong> {{ track_info['name'] }}</p>
                            <p><strong>Artist:</strong> {{ track_info['artist'] }}</p>
                            <p><strong>Album:</strong> {{ track_info['album'] }}</p>
                            <p><a href="{{ track_info['url'] }}" target="_blank">Listen on Spotify</a></p>
                        </div>
                        <h2>Recommended Songs:</h2>
                        <ul>
                            {% for rec in recommendations_list %}
                                <li>
                                    <div>
                                        <strong>{{ rec['name'] }}</strong> by {{ rec['artist'] }}
                                    </div>
                                    <a href="{{ rec['url'] }}" target="_blank">Listen</a>
                                </li>
                            {% endfor %}
                        </ul>
                        <a href="/welcome"><button>Search Again</button></a>
                    </div>
                </body>
                </html>
            ''', track_info=track_info, recommendations_list=recommendations_list)

        except Exception as e:
            return render_template_string(f'''
                <div class="container">
                    <h1>Error: {str(e)}</h1>
                    <a href="/welcome">Search Again</a>
                </div>
            ''')

    # Default Search Page
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Spotify Song Finder</title>
            <style>
                body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
                .container { background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); width: 90%; max-width: 700px; text-align: center; }
                h1 { color: #333; font-size: 28px; margin-bottom: 20px; }
                form { display: flex; flex-direction: column; gap: 20px; }
                input[type="text"], input[type="range"] { padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
                label { font-size: 14px; color: #555; text-align: left; }
                button { background-color: #007bff; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Spotify Song Finder</h1>
                <form method="POST">
                    <input type="text" name="song_query" placeholder="Search for a song..." required>
                    <label for="danceability">Danceability (0.0 - 1.0):</label>
                    <input type="range" name="danceability" min="0.0" max="1.0" step="0.1" value="0.5">
                    <label for="energy">Energy (0.0 - 1.0):</label>
                    <input type="range" name="energy" min="0.0" max="1.0" step="0.1" value="0.5">
                    <label for="tempo">Tempo (BPM):</label>
                    <input type="range" name="tempo" min="60" max="200" step="1" value="120">
                    <label for="valence">Valence (0.0 - 1.0):</label>
                    <input type="range" name="valence" min="0.0" max="1.0" step="0.1" value="0.5">
                    <button type="submit">Search</button>
                </form>
            </div>
        </body>
        </html>
    ''')



@app.route('/api/login', methods=['POST'])
def login():
    """
    Handle login requests for JWT authentication.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verify username and password
    if username in USERS and bcrypt.check_password_hash(USERS[username], password):
        access_token = create_access_token(identity=username)
        return jsonify({"success": True, "token": access_token, "message": "Login successful!"}), 200
    return jsonify({"success": False, "message": "Invalid username or password."}), 401

@app.route('/api/register', methods=['POST'])
def register():
    """
    Handle user registration.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    if username in USERS:
        return jsonify({"success": False, "message": "Username already exists."}), 400

    # Hash the password and store it
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    USERS[username] = hashed_password
    return jsonify({"success": True, "message": "Registration successful!"}), 201


@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected route to test JWT authentication.
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome, {current_user}!", "success": True}), 200


@app.route('/get_playlists')
def get_playlists():
    """Get User's Playlists."""
    if not is_authenticated():
        return redirect(get_auth_url())

    playlists = sp.current_user_playlists()
    playlists_info = [
        {"name": pl['name'], "url": pl['external_urls']['spotify']}
        for pl in playlists['items']
    ]

    return render_template_string('''
        <h1>Your Playlists</h1>
        <ul>
            {% for pl in playlists_info %}
                <li>
                    <strong>{{ pl['name'] }}</strong> - 
                    <a href="{{ pl['url'] }}" target="_blank">View on Spotify</a>
                </li>
            {% endfor %}
        </ul>
        <a href="/welcome">Back to Search</a>
    ''', playlists_info=playlists_info)


@app.route('/logout')
def logout():
    """Logout: Clear the session and redirect to the homepage."""
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)