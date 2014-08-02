import json

def get_all_data(github, username):
    userdata = github.get_user_cached(username)

    assert userdata is not None, "Plz run webserver, authenticate, and go to /alldata route to cache these values."

    repos = github.get_all_repositories(username)['data']

    stats = {}
    commits = {}

    for repo in repos:
        repo_name = repo['full_name']

        stats[repo_name] = github.get_stats_for_repository(repo_name)['data']

        commits[repo_name] = github.get_commits_for_repository(repo_name)['data']

    data = {'userdata':userdata,
            'repos':repos,
            'stats':stats,
            'commits':commits
            }
    return data

if __name__ == '__main__':
    """
    Note: this will only work after
    using the web app
    in order to populate the cache.
    """
    from githubgetter import GitHubAgent as GitHub
    github = GitHub(None)
    data = get_all_data(github, 'ksikka')
    with open('sample_data.json', 'w') as f:
        json.dump(data, f, indent=2)
