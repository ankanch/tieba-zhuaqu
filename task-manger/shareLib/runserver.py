"""
This script runs the CUITHelperAPIX application using a development server.
"""

from os import environ
from flask_cors import CORS, cross_origin
from flask_json  import FlaskJSON, JsonError, json_response, as_json
from CUITHelperAPIX import app
cors = CORS(app, resources={r"/api/*": {"origins":[ "http://cuit.akakanch.com/*","http://127.0.0.1:5000/*"]}})
FlaskJSON(app)


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '172.31.26.26')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
