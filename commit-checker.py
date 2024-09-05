import requests
import subprocess
import os

# GitHub repository details
GITHUB_REPO = 'devops-bharat05/Building-CI-CD-Pipeline-Tool'
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/commits'
GITHUB_TOKEN = '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' # Optional, but recommended for higher rate limits

# File to store the last checked commit SHA
LAST_COMMIT_FILE = '/Building-CI-CD-Pipeline-Tool/last_commit.txt'

def get_latest_commit():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'  # Optional, add if using a GitHub token
    }

    try:
        # Fetch the latest commits
        response = requests.get(GITHUB_API_URL, headers=headers)
        response.raise_for_status()
        latest_commit_sha = response.json()[0]['sha']
        return latest_commit_sha
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commits: {e}")
        return None

def read_last_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as file:
            return file.read().strip()
    return None

def write_last_commit(commit_sha):
    with open(LAST_COMMIT_FILE, 'w') as file:
        file.write(commit_sha)

def deploy_code():
    # Run your bash deployment script
    subprocess.run(['//Building-CI-CD-Pipeline-Tool/deploy_script.sh'], check=True)
    print("Deployment completed.")

def main():
    latest_commit = get_latest_commit()
    if not latest_commit:
        print("Unable to fetch the latest commit.")
        return

    last_commit = read_last_commit()

    if latest_commit != last_commit:
        print(f"New commit detected: {latest_commit}. Deploying...")
        deploy_code()
        write_last_commit(latest_commit)
    else:
        print("No new commit. Nothing to deploy.")

if __name__ == "__main__":
    main()
