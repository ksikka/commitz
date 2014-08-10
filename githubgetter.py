# http://github-flask.readthedocs.org/en/latest/
# https://github.com/cenkalti/github-flask
from flask.ext.github import GitHub, GitHubError 
from cache import memoized

class GitHubAgent(GitHub):

    def get_user(self):
        data = self.get('user')

        """{u'public_repos': 17, u'site_admin': False, u'subscriptions_url': u'https://api.github.com/users/ksikka/subscriptions', u'gravatar_id': u'48f15803578eaef05d9d9625b8c772b1', u'hireable': False, u'id': 1156958, u'followers_url': u'https://api.github.com/users/ksikka/followers', u'following_url': u'https://api.github.com/users/ksikka/following{/other_user}', u'blog': None, u'followers': 13, u'location': None, u'type': u'User', u'email': None, u'bio': None, u'gists_url': u'https://api.github.com/users/ksikka/gists{/gist_id}', u'company': None, u'events_url': u'https://api.github.com/users/ksikka/events{/privacy}', u'html_url': u'https://github.com/ksikka', u'updated_at': u'2014-08-01T18:09:54Z', u'received_events_url': u'https://api.github.com/users/ksikka/received_events', u'starred_url': u'https://api.github.com/users/ksikka/starred{/owner}{/repo}', u'public_gists': 6, u'name': u'Karan Sikka', u'organizations_url': u'https://api.github.com/users/ksikka/orgs', u'url': u'https://api.github.com/users/ksikka', u'created_at': u'2011-10-28T01:16:33Z', u'avatar_url': u'https://avatars.githubusercontent.com/u/1156958?v=1', u'repos_url': u'https://api.github.com/users/ksikka/repos', u'following': 15, u'login': u'ksikka'}"""
        self.get_user_cached(data['login'], user_data=data)
        return data


    @memoized('commitz_users', 1)
    def get_user_cached(self, username, user_data=None):
        """caching noop"""
        return user_data


    @memoized('commitz_repos', 1)
    def get_all_repositories(self, username):
        # par1
        repos = self.get('user/repos')
        # repos = self.get('user/%s/repos' % username) # for public repo access

        # par2
        user_orgs = self.get('user/orgs')
        for org in user_orgs:
            repos.extend(self.get('orgs/%s/repos' % org['login']))

        # dict necessary for the cache to store in couch
        return {'data':repos}

    @memoized('commitz_stats', 1)
    def get_stats_for_repository(self, repo_id):
        "repo id looks like ksikka/commitz"
        owner_username, repo_name = repo_id.split('/')

        try:
            data = self.get('repos/%s/%s/stats/contributors' % (owner_username, repo_name))
            if hasattr(data,'status_code') and data.status_code == 204:
                # this means that the repo exists in GH but is not initialized with a git repo.
                # this will eventually be filtered out.
                data = []
        except GitHubError, e:
            if '404: Not Found' in str(e):
                data = []
            else:
                raise
        # list of dicts with keys including total and author -> login

        # dict necessary for the cache to store in couch
        return {'data':data}

    @memoized('commitz_commits', 1)
    def get_commits_for_repository(self, repo_id):
        "repo id looks like ksikka/commitz"
        owner_username, repo_name = repo_id.split('/')

        try:
            data = self.get('repos/%s/%s/commits' % (owner_username, repo_name))
        except GitHubError, e:
            if '409: Git Repository is empty' in str(e):
                data = []
            elif '404: Not Found' in str(e):
                data = []
            else:
                raise
        # list of dicts with keys including commit, author, commiter.
        #   inside commit, is a dict with key message. that's the relevant one.

        # dict necessary for the cache to store in couch
        return {'data':data}


if __name__ == '__main__':
    """
    No tests for this because it's hard to programmatically make
    a github object. Much easier to just use the web server to test once
    and if it works once it generally always works unless the github API screws up
    in which case we'll just watch out for it and add that fix later.
    """
    pass
