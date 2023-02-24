import os
from github import Github

# Base directory path where repositories will be cloned
BASE_DIR = ""
# Repository Owner. Can be an org the user is part of
OWNER = ""
# The search criteria to match repositories
REPO_PREFIX = ""
# User's GH Token to authenticate the API calls
GH_TOKEN= ""

# Create a Github Client instance using an access token
github_client = Github(login_or_token=GH_TOKEN)
# Get the authenticated organization
github_org = github_client.get_organization(OWNER)
# Get a list of all repositories owned by the organization
org_repos = github_org.get_repos()

# List for all selected repos that matched the search criteria
selected_repos = []
for repo in org_repos:
    if repo.name.startswith(REPO_PREFIX):
        selected_repos.append(repo.name)
        print(f"{repo.name} Matched Search Criteria")

# Define color codes for Success & Error messages
GREEN = '\033[32m'
RED = '\033[31m'

# Loop through each repository and clone it
for repo in selected_repos:
    # Create the directory path for the cloned repository
    repo_dir = os.path.join(BASE_DIR, repo)

    # Clone the repository
    clone_command = f"git clone https://github.com/{OWNER}/{repo}.git {repo_dir}"
    status = os.system(clone_command)
    if status != 0:
        print(f"{RED}Error cloning repository {repo}")
    else:
        print(f"{GREEN}Successfully cloned repository {repo}")
