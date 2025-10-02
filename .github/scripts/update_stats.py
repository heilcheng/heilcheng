import os
from github import Github, Auth
from datetime import datetime

# GitHub token for authentication
token = os.environ.get("GH_TOKEN")
if not token:
    print("Error: GH_TOKEN environment variable is not set")
    exit(1)

# Use the new auth parameter instead of deprecated login_or_token
auth = Auth.Token(token)
g = Github(auth=auth)

user = g.get_user("heilcheng")

# Collect basic stats
repos = [r for r in user.get_repos() if not r.fork]
total_stars = sum(r.stargazers_count for r in repos)
total_forks = sum(r.forks_count for r in repos)
contributors = set()

for repo in repos:
    try:
        contributors.update(c.login for c in repo.get_contributors())
    except:
        pass 

stats_block = f""" GitHub Activity Summary (Updated Daily)

- Public repositories: {len(repos)}
- Total stars: {total_stars}
- Total forks: {total_forks}
- Contributors across repos: {len(contributors)}
- Last updated: {datetime.utcnow().strftime('%Y-%m-%d')}
"""

# Inject into README.md
readme_path = "README.md"
with open(readme_path, "r") as f:
    lines = f.readlines()

start, end = None, None
for i, line in enumerate(lines):
    if line.strip() == "<!-- STATS:START -->":
        start = i
    elif line.strip() == "<!-- STATS:END -->":
        end = i

if start is not None and end is not None:
    lines[start+1:end] = [stats_block + "\n"]

with open(readme_path, "w") as f:
    f.writelines(lines)
