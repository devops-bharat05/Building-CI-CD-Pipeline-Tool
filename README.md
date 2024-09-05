# CI/CD Pipeline for HTML Deployment Using GitHub, Python, Bash, and Cron

## Project Name
**CI-CD Pipeline Demo for Automatic Deployment of an HTML Project**

## Problem Statement
This project aims to demonstrate the creation of a Continuous Integration and Continuous Deployment (CI/CD) pipeline that automatically deploys changes pushed to a GitHub repository to an Nginx web server running on either an AWS EC2 instance or a local Linux machine. The pipeline includes scheduled checks for new commits, deployment automation, and server configuration management.

## Tools and Technologies Used
- **Git**: A version control system used to track changes in the project and facilitate collaboration.
- **GitHub**: A cloud-based platform to host the project repository and trigger the deployment process upon code changes.
- **Nginx**: A high-performance web server that will serve the HTML project.
- **AWS EC2**: A scalable cloud service used to host the Nginx server (alternatively, a local Linux machine can be used).
- **Python**: A scripting language used to check for new commits in the GitHub repository via the GitHub API.
- **Bash**: A scripting language used to automate the deployment of new code and restart the Nginx server.
- **Cron**: A time-based job scheduler used to periodically execute the Python script to check for new commits and trigger deployments.

## Prerequisites
- **GitHub account** with a repository created for the HTML project.
- **AWS EC2 instance** (Ubuntu-based) or a **Linux machine** with Nginx installed and configured.
- **Python** (version 3.x) and **pip** installed on the server.
- **Nginx** installed and running on the server.
- **Git** installed on the server.

## Architectural Diagram
GitHub Repository (HTML Project) -> Python Script (Check for New Commits via GitHub API) -> Cron Job (Scheduled to Run Python Script Every 5 Minutes) -> Bash Script (Deploys the Latest Code and Restarts Nginx) -> Nginx Web Server (Serves Updated HTML Project on AWS EC2 or Linux)


## Project Setup and Steps Performed

### Step 1: Set Up a Simple HTML Project and Push to GitHub
1. Create a basic HTML file `index.html`:
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CI/CD Pipeline Demo</title>
    </head>
    <body>
        <h1>Welcome to the CI/CD Pipeline Demo!</h1>
        <p>This is a simple HTML page deployed via an automated pipeline.</p>
    </body>
    </html>
    ```

2. Push the project to GitHub:
    - Initialize a git repository:
        ```bash
        git init
        git add .
        git commit -m "Initial commit for CI/CD pipeline demo"
        ```
    - Add the remote repository and push the code:
        ```bash
        git remote add origin https://github.com/your_username/your_repo.git
        git push -u origin main
        ```

### Step 2: Set Up an AWS EC2/Local Linux Instance with Nginx
1. **Launch an EC2 instance** (or set up a local Linux machine):
    - Select an Ubuntu image and configure security groups to allow SSH (port 22) and HTTP (port 80) traffic.

2. **Install Nginx on the server**:
    - SSH into the instance:
        ```bash
        ssh -i your_key.pem ubuntu@your_instance_public_ip
        ```
    - Install Nginx:
        ```bash
        sudo apt update
        sudo apt install nginx -y
        ```

3. **Configure Nginx**:
    - Modify the default site configuration to point to the deployment directory:
        ```bash
        sudo nano /etc/nginx/sites-available/default
        ```
    - Change the `root` directive to point to `/var/www/html` (or your preferred directory).
    - Restart Nginx:
        ```bash
        sudo systemctl restart nginx
        ```

### Step 3: Write a Python Script to Check for New Commits Using GitHub API
1. Install the required Python package:
    ```bash
    pip install requests
    ```

2. Create the Python script `check_commits.py`:
    ```python
    import requests
    import subprocess

    GITHUB_REPO = 'your_username/your_repo'
    LAST_COMMIT_FILE = '/tmp/last_commit.txt'

    def get_latest_commit():
        url = f'https://api.github.com/repos/{GITHUB_REPO}/commits'
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
    ```

### Step 4: Write a Bash Script to Deploy the Code and Restart Nginx
1. Create a Bash script `deploy_script.sh`:
    ```bash
    #!/bin/bash

    PROJECT_DIR="/var/www/html"
    REPO_URL="https://github.com/your_username/your_repo.git"

    # Change to the project directory
    cd $PROJECT_DIR

    # Pull the latest changes
    git pull $REPO_URL

    # Restart Nginx to apply changes
    sudo systemctl restart nginx

    echo "Deployment completed."
    ```

2. Make the script executable:
    ```bash
    chmod +x /path/to/your/deploy_script.sh
    ```

### Step 5: Set Up a Cron Job to Run the Python Script
1. Open the crontab editor:
    ```bash
    crontab -e
    ```

2. Add the following line to run the Python script every 5 minutes:
    ```bash
    */5 * * * * /usr/bin/python3 /path/to/your/check_commits.py >> /var/log/deploy.log 2>&1
    ```

### Step 6: Test the Pipeline Setup
1. Make a change to your HTML project:
    - Edit the `index.html` file, e.g., update the content:
        ```html
        <h1>Welcome to the CI/CD Pipeline Demo - Updated!</h1>
        ```

2. Commit and push the changes to GitHub:
    ```bash
    git add .
    git commit -m "Updated HTML content"
    git push
    ```

3. Wait for the cron job to run (or run the Python script manually for testing):
    ```bash
    python3 /path/to/your/check_commits.py
    ```

4. Verify that the changes are deployed by accessing the server's public IP in your browser:
    ```
    http://your_instance_public_ip
    ```

## Conclusion
This project demonstrates how to build a simple but effective CI/CD pipeline for automatically deploying changes from a GitHub repository to a web server. By leveraging Python, Bash, and Cron, the process of deploying new code becomes fully automated, requiring minimal manual intervention once set up.

## References
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Nginx Official Documentation](https://nginx.org/en/docs/)
- [Cron Job Manual](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [AWS EC2 Documentation](https://aws.amazon.com/ec2/documentation/)
