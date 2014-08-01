from flask.ext.github import GitHub, GitHubError

class GitHubAgent(GitHub):

    def get_all_repositories(self, username):
        # par1
        repos = self.get('user/repos')
        # repos = self.get('user/%s/repos' % username) # for public repo access

        # par2
        user_orgs = self.get('user/orgs')
        for org in user_orgs:
            repos.extend(self.get('org_reposorgs/%s/repos' % org['login']))

        return repos

    def get_commits_for_repository(self, repo_id):
        "repo id looks like ksikka/commitz"
        owner_username, repo_name = repo_id.split('/')

        data = self.get('repos/%s/%s/commits' % (owner_username, repo_name))
        # list of dicts with keys including commit, author, commiter.
        #   inside commit, is a dict with key message. that's the relevant one.

        return data
