#!/bin/bash

PROJECT_DIR="/Building-CI-CD-Pipeline-Tool"
REPO_URL="https://github.com/devops-bharat05/Building-CI-CD-Pipeline-Tool.git"

# Navigate to project directory
cd $PROJECT_DIR

# Pull the latest changes
git pull $REPO_URL

# Restart Nginx
nginx -s reload

echo "Deployment completed."
