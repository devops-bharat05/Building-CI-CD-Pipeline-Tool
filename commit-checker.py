import requests
import subprocess

GITHUB_REPO = 'devops-bharat05/Building-CI-CD-Pipeline-Tool'
LAST_COMMIT_FILE = '/Building-CI-CD-Pipeline-Tool/index.html'

def get_latest_commit():
    url = f'https://api.github.com/repos/devops-bharat05/commits'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[0]['sha']

def read_last_commit():
    try:
        with open(LAST_COMMIT_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def write_last_commit(commit_sha):
    with open(LAST_COMMIT_FILE, 'w') as file:
        file.write(commit_sha)

def main():
    latest_commit = get_latest_commit()
    last_commit = read_last_commit()

    if latest_commit != last_commit:
        print('New commit detected. Deploying...')
        subprocess.run(['/path/to/your/deploy_script.sh'])
        write_last_commit(latest_commit)
    else:
        print('No new commit.')

if __name__ == "__main__":
    main()
