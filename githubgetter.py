from flask.ext.github import GitHub, GitHubError

class GitHubAgent(GitHub):

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

    def get_commits_for_repository(self, repo_id):
        "repo id looks like ksikka/commitz"
        owner_username, repo_name = repo_id.split('/')

        try:
            data = self.get('repos/%s/%s/commits' % (owner_username, repo_name))
        except GitHubError, e:
            if '404: Not Found' in str(e):
                data = []
            else:
                raise
        # list of dicts with keys including commit, author, commiter.
        #   inside commit, is a dict with key message. that's the relevant one.

        # dict necessary for the cache to store in couch
        return {'data':data}

"""
No tests for this because it's hard to programmatically make
a github object. Much easier to just use the web server to test once
and if it works once it generally always works unless the github API screws up
in which case we'll just watch out for it and add that fix later.
"""
