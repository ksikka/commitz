import json
from flask import Flask, g, session, redirect, request, send_from_directory, render_template
from flask.json import jsonify as send_json


app = Flask(__name__)
app.config.update(json.load(open('config.json')))

from githubgetter import GitHubAgent as GitHub
github = GitHub(app)

@app.route('/')
def index():
    r = redirect_if_logged_in()
    if r:
        return r
    return render_template('index.html')

"""
User session management
"""
class User(object):

    def __init__(self, username, access_token):
        self.username = username # used in session
        self.access_token = access_token

# keyed on username
users = {} # TODO replace with couchdb for persistence

@app.before_request
def before_request():
    """
    Populates g.user for all authenticated requests
    """
    g.user = None

    if 'username' in session:
        g.user = users.get(session['username'], None)

        # forget about invalid/expired usernames
        if g.user is None: # user does not exist in DB
            session.pop('username', None)

def redirect_if_logged_in(url=None):
    if g.user is not None:
        return redirect('/g/%s' % g.user.username)

def redirect_if_not_logged_in():
    if g.user is None:
        return redirect('/')

"""
Required for github-flask ext.
    http://github-flask.readthedocs.org/en/latest/#invoking-remote-methods
"""
@github.access_token_getter
def token_getter():
    if g.user is not None:
        return g.user.access_token


@app.route('/login')
def login():
    r = redirect_if_logged_in()
    if r:
        return r
    return github.authorize()


"""
After user authenticates on github.com, github sends 302 here with
    a temporary code which github-flask exchanges for an access token
    then the handler is called with access_token as an argument.
"""
@app.route(app.config['GITHUB_CALLBACK_SHORT_URL'])
@github.authorized_handler
def authorized(access_token):

    # authentication failed
    if access_token is None:
        return redirect('/')

    user = User(None, access_token)
    g.user = user # necessary for token_getter fn to read access token
    username = github.get_user()['login']

    existing_user = users.get(username)
    if existing_user:
        user = existing_user
        g.user = user
        user.access_token = access_token
    else:
        user.username = username
        users[user.username] = user

    session['username'] = user.username

    return redirect_if_logged_in()


@app.route('/logout')
def logout():
    username = session.pop('username', None)
    users.pop(username, None)
    return redirect('/')

"""
These are only used as tests for githubgetter.py
"""
from data_gen import get_all_data as _get_all_data
@app.route('/alldata')
def alldata():
    r = redirect_if_not_logged_in()
    if r:
        return r
    return send_json(_get_all_data(github, g.user.username))


if __name__ == "__main__":
    app.run(debug=True)

