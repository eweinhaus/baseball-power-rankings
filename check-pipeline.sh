#!/bin/bash

# Check GitHub Actions Pipeline Status
# This script checks the status of the GitHub Actions pipeline

REPO="eweinhaus/baseball-power-rankings"
WORKFLOW_NAME="Deploy to AWS"

echo "🔍 Checking GitHub Actions Pipeline Status..."
echo "Repository: $REPO"
echo "Workflow: $WORKFLOW_NAME"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    echo ""
    echo "Alternatively, check the pipeline status at:"
    echo "https://github.com/$REPO/actions"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    echo ""
    echo "Alternatively, check the pipeline status at:"
    echo "https://github.com/$REPO/actions"
    exit 1
fi

echo "✅ GitHub CLI authenticated"
echo ""

# Get the latest workflow run
echo "📊 Latest Workflow Run:"
gh run list --repo $REPO --workflow "$WORKFLOW_NAME" --limit 1

echo ""
echo "🔗 View in browser:"
echo "https://github.com/$REPO/actions" 