#!/bin/bash

set -e

echo "Starting PR Review Bot..."

# Check if required inputs are provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set"
    exit 1
fi

# Check if required inputs are provided
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY is not set"
    exit 1
fi

if [ -z "$PR_NUMBER" ]; then
    echo "Error: PR_NUMBER is not set"
    exit 1
fi

python main.py --pr-number $PR_NUMBER --github_token $GITHUB_TOKEN --openai_api_key $OPENAI_API_KEY --repo_name $GITHUB_REPOSITORY