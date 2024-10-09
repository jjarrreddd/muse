Ensure Flask ('pip install Flask' in venv and flask-server directory) and React are installed as well as:
- axios (npm install axios) in 'front-end' directory.
- python-dotenv (pip install python-dotenv) and requests (pip install requests) in venv in 'flask-server' directory.

To run the full applicatiom, first split terminals:

1. In one terminal, activate the virutal environment and go into the 'flask-server' directory.
   Use the following commands to run the backend:

     python main.py OR flask --app main run

2. In the other terminal, go into the 'front-end' directory. Then use the following command to
   start the frontend:

     npm start
