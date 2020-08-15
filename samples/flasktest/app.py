import os
from flask import Flask, redirect, request
from flask import render_template_string

from requests_oauthlib import OAuth2Session

from raindropio import *



client_id = os.environ["RAINDROP_CLIENT_ID"]
client_secret = os.environ["RAINDROP_CLIENT_SECRET"]

redirect_uri = 'http://localhost:5000/approved'

app = Flask(__name__)

INDEX = """
<html>
<a href="./login">Click here for login.</a>
</html>
"""


COLLECTIONS = """
<html>
<ul>
{% for collection in collections %}
  <li>{{collection.title}}
{% endfor %}
</ul>
</html>
"""


import requests
@app.route('/approved')
def approved():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    code = request.args.get('code')
    token = oauth.fetch_token(
        API.URL_ACCESS_TOKEN,
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        include_client_id=True)

    with API(**token) as api:
        collections = Collection.get_roots(api)

    return render_template_string(COLLECTIONS, collections=collections)


@app.route('/login')
def login():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, _ = oauth.authorization_url(API.URL_AUTHORIZE)
    return redirect(authorization_url)

@app.route('/')
def index():
    return render_template_string(INDEX)


if __name__ == '__main__':
    app.run(debug=True)