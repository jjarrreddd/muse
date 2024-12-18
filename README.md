Ensure Flask ('pip install Flask' in venv and flask-server directory) and React are installed as well as:
- axios (npm install axios), framer-motion (npm install framer-motion), react-router-dom (npm install react-router-dom), and bootstrap (npm install bootstrap) in 'front-end' directory.
- python-dotenv, requests, spotipy, flask-cors (pip install python-dotenv requests spotipy flask-cors) in venv in 'flask-server' directory.

To run the full applicatiom, first split terminals:

1. In one terminal, activate the virutal environment and go into the 'flask-server' directory.
   Use the following commands to run the backend:

     python main.py

2. In the other terminal, go into the 'front-end' directory. Then use the following command to
   start the frontend:

     npm start
