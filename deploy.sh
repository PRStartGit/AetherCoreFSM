#!/bin/bash
# Zynthio Deployment Script
# This script deploys the latest code from main branch to production server

set -e

echo "==================================================================="
echo "Zynthio Production Deployment"
echo "==================================================================="
echo ""

# Check if we're on the right branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# If on development, merge to main first
if [ "$CURRENT_BRANCH" == "development" ]; then
    echo "Switching to main branch and merging development..."
    git checkout main
    git merge development
    git push origin main
    echo "Merged development into main ✓"
elif [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Please run this script from main or development branch"
    exit 1
fi

echo ""
echo "Deploying to production server..."
echo ""

# Deploy to production
ssh zynthio <<'ENDSSH'
    set -e
    cd /root/AetherCoreFSM
    echo "Pulling latest code..."
    git pull origin main

    echo "Building and restarting services..."
    docker compose build backend frontend
    docker compose up -d

    echo ""
    echo "==================================================================="
    echo "Deployment completed successfully!"
    echo "==================================================================="
    echo "Application: https://zynthio.com"
    echo "API Docs: https://zynthio.com/api/docs"
ENDSSH

# Switch back to development if we started there
if [ "$CURRENT_BRANCH" == "development" ]; then
    git checkout development
    echo "Switched back to development branch"
fi

echo ""
echo "All done! ✓"
