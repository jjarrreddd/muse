# In order to launch full web app, split terminal and run FLASK
# in one terminal and REACT in the other terminal.
# To run: python main.py
# Or: flask --app main run

from flask import Flask

app = Flask(__name__)

@app.route("/welcome")
def main():
    response = {
        "name": "morning (flask end)",
        "hello": "Hello World (flask end)"
    }

    return response

if __name__ == "__main__":
    app.run(debug=True)