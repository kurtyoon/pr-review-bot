#!/bin/bash

set -e

echo "Starting PR Review Bot..."

# Check if required inputs are provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set"
    exit 1
fi

if [ -z "$PR_NUMBER" ]; then
    echo "Error: PR_NUMBER is not set"
    exit 1
fi

# 선택된 LLM 제공자에 따른 API 키 확인
if [ "$LLM_PROVIDER" = "openai" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY is not set (required for OpenAI provider)"
    exit 1
elif [ "$LLM_PROVIDER" = "google" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY is not set (required for Google provider)"
    exit 1
fi

python main.py \
  --pr_number "$PR_NUMBER" \
  --github_token "$GITHUB_TOKEN" \
  --repo_name "$GITHUB_REPOSITORY" \
  --llm_provider "$LLM_PROVIDER" \
  --model "$MODEL_NAME" \
  --openai_api_key "$OPENAI_API_KEY" \
  --google_api_key "$GOOGLE_API_KEY"