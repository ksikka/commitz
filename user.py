from githubgetter import GitHubError

class User(object):
    def __init__(self, uid, access_token):
        self.id = uid # used in session
        self.access_token = access_token

    def getdata(self, github):
        try:
            data = github.get('user')
        except GitHubError, e:
            import IPython; IPython.embed()

        """{u'public_repos': 17, u'site_admin': False, u'subscriptions_url': u'https://api.github.com/users/ksikka/subscriptions', u'gravatar_id': u'48f15803578eaef05d9d9625b8c772b1', u'hireable': False, u'id': 1156958, u'followers_url': u'https://api.github.com/users/ksikka/followers', u'following_url': u'https://api.github.com/users/ksikka/following{/other_user}', u'blog': None, u'followers': 13, u'location': None, u'type': u'User', u'email': None, u'bio': None, u'gists_url': u'https://api.github.com/users/ksikka/gists{/gist_id}', u'company': None, u'events_url': u'https://api.github.com/users/ksikka/events{/privacy}', u'html_url': u'https://github.com/ksikka', u'updated_at': u'2014-08-01T18:09:54Z', u'received_events_url': u'https://api.github.com/users/ksikka/received_events', u'starred_url': u'https://api.github.com/users/ksikka/starred{/owner}{/repo}', u'public_gists': 6, u'name': u'Karan Sikka', u'organizations_url': u'https://api.github.com/users/ksikka/orgs', u'url': u'https://api.github.com/users/ksikka', u'created_at': u'2011-10-28T01:16:33Z', u'avatar_url': u'https://avatars.githubusercontent.com/u/1156958?v=1', u'repos_url': u'https://api.github.com/users/ksikka/repos', u'following': 15, u'login': u'ksikka'}"""
        self.username = 'ksikka'
