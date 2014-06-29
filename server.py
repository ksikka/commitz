import json
from flask import Flask, g, session, redirect, request
from flask.ext.github import GitHub

"""
Source: http://github-flask.readthedocs.org/en/latest/
"""

app = Flask(__name__)
app.config.update(json.load(open('config.json')))

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

"""
User session management
"""
users = {}

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        g.user = users.get(session['user_id'], None)

        if g.user is None:
            session.pop('user_id', None)

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
    next_url = request.args.get('next') or '/'

    if access_token is None:
        print "authentication failed"
        return redirect(next_url)

    user = users.get(access_token, None)

    if user is None:
        uid = getuid()
        user = User(uid, access_token)
        users[uid] = user

    else:
        user.access_token = access_token

    session['user_id'] = user.id

    return redirect(next_url)


@app.route('/login')
def login():
    #TODO store next url in session
    return github.authorize()


@app.route('/logout')
def logout():
    user_id = session.pop('user_id', None)
    users.pop(user_id, None)
    return redirect('/')


@app.route('/user')
def user():
    if session.get('user_id', None) is None:
        return redirect('/login')
    return str(github.get('user'))


if __name__ == "__main__":
    app.run()

