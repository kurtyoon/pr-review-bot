import os
import sys
import logging
import argparse
from github import Github
from app.chain.review_chain import ReviewChain
from app.utility.github_util import GithubUtil
from app.utility.markdown_util import MarkdownUtil

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('code-review-bot')

def main():
    parser = argparse.ArgumentParser(description="Code Review Bot 🤖")
    parser.add_argument('--pr_number', type=int, default=os.getenv('PR_NUMBER'))
    parser.add_argument('--github_token', default=os.getenv("GITHUB_TOKEN"))
    parser.add_argument('--repo_name', default=os.getenv("GITHUB_REPOSITORY"))
    
    # LLM 제공자 선택 옵션 추가
    parser.add_argument('--llm_provider', default=os.getenv("LLM_PROVIDER", "openai"),
                      choices=["openai", "google"],
                      help="사용할 LLM 제공자 (openai, google)")
    
    # 다양한 API 키 옵션
    parser.add_argument('--openai_api_key', default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument('--google_api_key', default=os.getenv("GOOGLE_API_KEY"))
 
    # 모델 선택 옵션
    parser.add_argument('--model', default=os.getenv("MODEL_NAME"))
    args = parser.parse_args()

    # 필수 파라미터 검사
    if not args.github_token:
        logger.error("GitHub 토큰이 필요합니다.")
        sys.exit(1)
        
    if not args.pr_number:
        logger.error("PR 번호가 필요합니다.")
        sys.exit(1)
        
    if not args.repo_name:
        logger.error("GitHub 레포지토리 이름이 필요합니다.")
        sys.exit(1)
    
    # 선택된 LLM 제공자에 따른 API 키 검증
    if args.llm_provider == "openai" and not args.openai_api_key:
        logger.error("OpenAI API 키가 필요합니다.")
        sys.exit(1)
    elif args.llm_provider == "google" and not args.google_api_key:
        logger.error("Google API 키가 필요합니다.")
        sys.exit(1)

    # 환경 변수 설정
    os.environ["LLM_PROVIDER"] = args.llm_provider
    if args.model:
        os.environ["MODEL_NAME"] = args.model
        
    if args.openai_api_key:
        os.environ["OPENAI_API_KEY"] = args.openai_api_key
    if args.google_api_key:
        os.environ["GOOGLE_API_KEY"] = args.google_api_key

    try:

        github = Github(args.github_token)

        logger.info(f"Get PR #{args.pr_number} information")
        pr_data = GithubUtil.get_pr_info(github, args.repo_name, args.pr_number)
        file_diffs = GithubUtil.get_file_diffs(github, args.repo_name, args.pr_number)

        review_chain = ReviewChain()
        review_chain.ready()

        logger.info(f"PR #{args.pr_number} review started")
        review_result = review_chain.run_code_review(pr_data, file_diffs)

        markdown_result = MarkdownUtil.format_markdown(review_result)

        logger.info(f"PR #{args.pr_number} review completed")
        GithubUtil.post_review_comment(github, args.repo_name, args.pr_number, markdown_result)

        logger.info(f"PR #{args.pr_number} review completed")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)
    
if __name__ == "__main__":
    main()
    