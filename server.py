import json
from flask import Flask, g, session, redirect, request, send_from_directory, render_template
from flask.json import jsonify as send_json
from flask.ext.github import GitHub, GitHubError


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

_uidcnt = 0
def getuid():
    global _uidcnt
    _uidcnt += 1
    return _uidcnt

class User(object):
    def __init__(self, uid, access_token):
        self.id = uid # used in session
        self.access_token = access_token

    def getdata(self):
        try:
            data = github.get('user')
        except GitHubError, e:
            import IPython; IPython.embed()

        """{u'public_repos': 17, u'site_admin': False, u'subscriptions_url': u'https://api.github.com/users/ksikka/subscriptions', u'gravatar_id': u'48f15803578eaef05d9d9625b8c772b1', u'hireable': False, u'id': 1156958, u'followers_url': u'https://api.github.com/users/ksikka/followers', u'following_url': u'https://api.github.com/users/ksikka/following{/other_user}', u'blog': None, u'followers': 13, u'location': None, u'type': u'User', u'email': None, u'bio': None, u'gists_url': u'https://api.github.com/users/ksikka/gists{/gist_id}', u'company': None, u'events_url': u'https://api.github.com/users/ksikka/events{/privacy}', u'html_url': u'https://github.com/ksikka', u'updated_at': u'2014-08-01T18:09:54Z', u'received_events_url': u'https://api.github.com/users/ksikka/received_events', u'starred_url': u'https://api.github.com/users/ksikka/starred{/owner}{/repo}', u'public_gists': 6, u'name': u'Karan Sikka', u'organizations_url': u'https://api.github.com/users/ksikka/orgs', u'url': u'https://api.github.com/users/ksikka', u'created_at': u'2011-10-28T01:16:33Z', u'avatar_url': u'https://avatars.githubusercontent.com/u/1156958?v=1', u'repos_url': u'https://api.github.com/users/ksikka/repos', u'following': 15, u'login': u'ksikka'}"""
        self.username = 'ksikka'

"""
User session management # todo replace with couchdb
"""
# keyed on username
users = {}

@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        g.user = users.get(session['username'], None)

        # forget about invalid/expired usernames
        if g.user is None:
            session.pop('username', None)

        else:
            g.user.getdata()

def redirect_if_logged_in():
    if g.user is not None:
        return redirect('/g/%s' % g.user.username)

"""
Required for github-flask ext.
    http://github-flask.readthedocs.org/en/latest/#invoking-remote-methods
"""
@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.access_token

"""
After user authenticates on github.com, github sends 302 here with
    a temporary code which github-flask exchanges for an access token
    then the handler is called with access_token as an argument.
"""
@app.route(app.config['GITHUB_CALLBACK_SHORT_URL'])
@github.authorized_handler
def authorized(access_token):

    if access_token is None:
        print "authentication failed" # TODO
        return redirect('/')

    uid = getuid()
    user = User(uid, access_token)
    g.user = user
    user.getdata()
    existing_user = users.get(user.username)
    if existing_user:
        user = existing_user
        user.access_token = access_token
    else:
        users[user.username] = user

    # fyi the reason they're here is because username was not in the session, aka they were logged out.
    session['username'] = user.username

    return redirect_if_logged_in()

@app.route('/login')
def login():
    r = redirect_if_logged_in()
    if r:
        return r
    return github.authorize()


@app.route('/logout')
def logout():
    username = session.pop('username', None)
    users.pop(username, None)
    return redirect('/')


@app.route('/user')
def user():
    if session.get('username', None) is None:
        return redirect('/login')
    return str(github.get('user'))


if __name__ == "__main__":
    app.run(debug=True)

