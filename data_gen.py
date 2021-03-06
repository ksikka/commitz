import json

def get_github_data(github, username):
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

    num_my_commits = contrib_dist.get(username, 0)
    num_total_commits = sum(contrib_dist.values())
    if num_total_commits == 0:
        contrib_percent = 0
    else:
        contrib_percent = round(float(num_my_commits) / num_total_commits * 100)

    data = {'contrib_dist': contrib_dist,
            'last_commit_date': last_commit_date,
            'num_my_commits': num_my_commits,
            'num_total_commits': num_total_commits,
            'contrib_percent': contrib_percent
            }

    return data

def get_all_data(github, username):
    github_data = get_github_data(github, username)

    data = {}
    userdata = github_data['userdata']

    data['userdata'] = userdata

    overview = {}
    overview['num_repos_contributed_to'] = 0
    overview['total_commits'] = 0

    repos = github_data['repos']
    filtered_repos = []
    for repo in repos:
        repo_name = repo['full_name']
        repo_contributors = github_data['stats'][repo_name]
        repo_commits = github_data['commits'][repo_name]
        summary = repo_summary(userdata, repo, repo_contributors, repo_commits)
        repo['summary'] = summary

        num_commits_mine = summary['contrib_dist'].get(username, 0)
        if num_commits_mine == 0:
            continue
        else:
            filtered_repos.append(repo)

        # count number of repositories with nonzero commits by the user.
        if summary['last_commit_date'] is not None:
            overview['num_repos_contributed_to'] += 1

        # count total commits over all repos
        overview['total_commits'] += summary['contrib_dist'].get(username, 0)
        # delete all the url crap.
        for key in repo.keys():
            if key.endswith('_url'):
                del repo[key]
        for key in repo['owner'].keys():
            if key.endswith('_url'):
                del repo['owner'][key]


    overview['timespan'] = 1 + 2014 - int(userdata['created_at'][:4]) # ie "2011-10-28T01:16:33Z" => 2011

    # sort descending chronological
    filtered_repos.sort(reverse=True, key=lambda x: x['summary']['last_commit_date'])

    data['repos'] = filtered_repos
    data['overview'] = overview

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

    # tests get_github_data
    all_data = get_github_data(github, username)
    with open('test_github_data.json', 'w') as f:
        json.dump(all_data, f, indent=2)

    # tests get_all_data
    final_data = get_all_data(github, username)
    with open('test_final_data.json', 'w') as f:
        json.dump(final_data, f, indent=2)
