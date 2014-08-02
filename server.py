import json
from flask import Flask, g, session, redirect, request, send_from_directory, render_template
from flask.json import jsonify as send_json
from githubgetter import GitHubAgent as GitHub


app = Flask(__name__)
app.config.update(json.load(open('config.json')))

@app.route('/')
def index():
    r = redirect_if_logged_in()
    if r:
        return r
    return render_template('index.html')


"""
Source: http://github-flask.readthedocs.org/en/latest/
"""
github = GitHub(app)

"""
User session management # todo replace with couchdb
"""
# keyed on username
users = {}
class User(object):

    def __init__(self, username, access_token):
        self.username = username # used in session
        self.access_token = access_token

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
        # return redirect('/g/%s' % g.user.username)
        return redirect('/commitz')

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


@app.route('/user')
def user():
    r = redirect_if_not_logged_in()
    if r:
        return r
    return str(github.get('user'))


@app.route('/repos')
def repos():
    r = redirect_if_not_logged_in()
    if r:
        return r
    return send_json(github.get_all_repositories(g.user.username))


@app.route('/stats')
def stats():
    r = redirect_if_not_logged_in()
    if r:
        return r
    repos = github.get_all_repositories(g.user.username)['data']

    stats = {}
    for repo in repos:
        repo_name = repo['full_name']
        stats[repo_name] = github.get_stats_for_repository(repo_name)['data']
    return send_json(stats)


@app.route('/commitz')
def commitz():
    r = redirect_if_not_logged_in()
    if r:
        return r

    repos = github.get_all_repositories(g.user.username)['data']

    commits = {}
    for repo in repos:
        repo_name = repo['full_name']
        commits[repo_name] = github.get_commits_for_repository(repo_name)['data']

    return send_json(commits)


if __name__ == "__main__":
    app.run(debug=True)

