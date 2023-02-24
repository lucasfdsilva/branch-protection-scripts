import requests
import json

OWNER = ""
GH_TOKEN = ""
REPOS = [""]


def create_branch_protection_rule(owner, repo, branch, gh_token, config):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {gh_token}"
    }
    data = config
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(
            f"Branch protection rule for {repo}-{branch} created successfully")
    else:
        print(
            f"Error creating branch protection rule for {repo}-{branch}: {response.text}")


for REPO in REPOS:
    MAIN_CONFIG = {
        "required_status_checks": {
            "strict": True,
            "contexts": [
                f"{REPO}"
            ]
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 2,
            "require_last_push_approval": True
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": False,
        "lock_branch": False,
        "allow_fork_syncing": True
    }

    QA_CONFIG = {
        "required_status_checks": {
            "strict": True,
            "contexts": [
                f"{REPO}"
            ]
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 2,
            "require_last_push_approval": True
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": False,
        "lock_branch": False,
        "allow_fork_syncing": True
    }

    DEV_CONFIG = {
        "required_status_checks": None,
        "enforce_admins": False,
        "required_pull_request_reviews": None,
        "restrictions": None,
        "required_linear_history": False,
        "allow_deletions": False,
        "allow_fork_syncing": True
    }

    create_branch_protection_rule(OWNER, REPO, "main", GH_TOKEN, MAIN_CONFIG)
    create_branch_protection_rule(OWNER, REPO, "qa", GH_TOKEN, QA_CONFIG)
    create_branch_protection_rule(OWNER, REPO, "dev", GH_TOKEN, DEV_CONFIG)
