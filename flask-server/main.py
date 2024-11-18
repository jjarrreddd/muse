from flask import Flask, redirect, request, session, url_for
from flask_cors import CORS  # Import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (you can customize this if needed)
app.secret_key = os.urandom(24)  # You should set this to a secure key

# Spotify app credentials
CLIENT_ID = '5d8b3c44a9a54407806a8fa01c89167d'
CLIENT_SECRET = '8f1704d5370c427caef4d870da5beadd'
REDIRECT_URI = 'http://localhost:5000/callback'  # Update this if needed

@app.route("/login")
def login():
    try:
        print(f"Session before redirecting: {session}")

        if 'access_token' in session:
            print("User is already logged in.")
            return redirect(url_for('welcome'))
        # Redirect user to Spotify's authorization page
        auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user-read-private user-read-email"
        return redirect(auth_url)
    except:
        print(f"Error during login: {e}")
        return {"error": "An error has occurred."}, 500

@app.route("/callback")
def callback():
    # Get the authorization code from the request
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return {"error": "An error has occurred. Please try again."}
    
    if not code:
        return {"error": "Authorization code not provided."}, 400
    
    try:
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
        refresh_token = token_data.get('refresh_token')
        
        print(f"Access Token: {access_token}")  # Debugging line
        print(f"Session: {session}")

        # Store the access and refresh token in the session
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

        return redirect('http://localhost:3000/welcome')
    
    except requests.exceptions.RequestException:
        return {"error": "A possible network error has occurred. Please try again."}
    except Exception as e:
        return {"error": "Failed to log in."}, 500

@app.route("/logout", methods=["POST"])
def logout():
    print(f"Session before logout: {session}")
    # Remove the access and refresh token from the session
    session.pop('access_token', None)
    session.pop('refresh_token', None)
    print(f"Session after logout: {session}")
    return {"message": "Log out successful!"}, 200

@app.route("/search-song", methods=["POST"])
def search_song():
    if 'access_token' not in session:
        return redirect(url_for('login'))

    song_name = request.json.get("song_name")

    if not song_name:
        return {"error": "No song name provided"}, 400

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    search_url = f'https://api.spotify.com/v1/search?q={song_name}&type=track'
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to search for the song. Status code: {response.status_code}"}, 500

    search_data = response.json()

    if search_data.get('tracks') and search_data['tracks']['items']:
        track = search_data['tracks']['items'][0]
        song_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'uri': track['uri']
        }
        return song_info
    else:
        return {"error": "No results found for the song."}, 404

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
