from typing import Dict, Any
from github import Github

class GithubUtil:

    @staticmethod
    def get_pr_info(github: Github, repo_name: str, pr_number: int) -> Dict[str, Any]:
        repo = github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        files = GithubUtil.get_pr_files(github, repo_name, pr_number)

        return {
            'title': pr.title,
            'body': pr.body or '',
            'state': pr.state,
            'created_at': pr.created_at.isoformat(),
            'updated_at': pr.updated_at.isoformat(),
            'user': pr.user.login,
            'base_branch': pr.base.ref,
            'head_branch': pr.head.ref,
            'commits_count': pr.commits,
            'additions': pr.additions,
            'deletions': pr.deletions,
            'changed_files': pr.changed_files,
            'files': files,
            'number': pr_number
        }
    
    @staticmethod
    def get_pr_files(github: Github, repo_name: str, pr_number: int) -> Dict[str, Dict[str, Any]]:
        
        repo = github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        files_dict = {}

        for file in pr.get_files():

            if any(file.filename.endswith(ext) for ext in [
                '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', 
                '.zip', '.gz', '.tar', '.jar', '.class', '.dll', '.exe'
            ]):
                continue
            
            files_dict[file.filename] = {
                'status': file.status,
                'additions': file.additions,
                'deletions': file.deletions,
                'changes': file.changes,
                'patch': file.patch if hasattr(file, 'patch') else ""
            }
        
        return files_dict
    
    @staticmethod
    def get_file_diffs(github: Github, repo_name: str, pr_number: int) -> Dict[str, Dict[str, Any]]:
        files_dict = GithubUtil.get_pr_files(github, repo_name, pr_number)

        file_diffs = {}

        for filename, file_info in files_dict.items():
            file_diffs[filename] = file_info.get('patch', '')

        return file_diffs
    
    @staticmethod
    def post_review_comment(github: Github, repo_name: str, pr_number: int, comment: str) -> None:
        repo = github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        pr.create_issue_comment(comment)