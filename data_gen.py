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

def repo_summary(userdata, repo, repo_contributors, repo_commits):
    """
    IN
    userdata : dict
    repo : dict
    repo_contributors : list of dicts
    repo_commits : list of dicts
    """
    username = userdata['login']

    # map from username to number of commits.
    # useful for contribution pie chart.
    contrib_dist = { c['author']['login'] : c['total'] for c in repo_contributors }

    # date of most recent commit as a string in ISO fmt.
    # useful to put repos in chronological order for the user
    last_commit_date = None
    for commit in repo_commits:
        if commit['author'] is None:
            # github did not recognize the author of this commit.
            # check if name matches the github name.
            if commit['commit']['author']['name'].lower() == userdata['name'].lower():
                last_commit_date = commit['commit']['author']['date']
                break
        elif commit['author']['login'] == username:
            last_commit_date = commit['commit']['author']['date']
            break

    data = {'contrib_dist': contrib_dist,
            'last_commit_date': last_commit_date,
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
    username = 'ksikka'

    data = get_all_data(github, username)
    with open('sample_data.json', 'w') as f:
        json.dump(data, f, indent=2)

    userdata = data['userdata']
    summaries = {}
    for repo in data['repos']:
        repo_name = repo['full_name']
        repo_contributors = data['stats'][repo_name]
        repo_commits = data['commits'][repo_name]
        summaries[repo_name] = repo_summary(userdata, repo, repo_contributors, repo_commits)
    print json.dumps(summaries, indent=4)
