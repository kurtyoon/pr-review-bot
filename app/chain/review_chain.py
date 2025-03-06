from app.config.config import Config
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough
from app.factory.llm_factory import LLMFactory
from typing import Dict, Any

class ReviewChain:

    def __init__(self):
        self.config = Config()
        self.llm = None
        self.chains = {}
        self.prompts = {}

    def ready(self):
        self.llm = LLMFactory.create_llm(self.config)

        self._set_up_prompts()
        self._set_up_chains()

    def run_code_review(self, pr_data: Dict[str, Any], file_diffs: Dict[str, str]) -> Dict[str, str]:
        file_changes_str = "\n".join([
            f"- {filename}: +{info.get('additions', 0)}, -{info.get('deletions', 0)}"
            for filename, info in pr_data.get('files', {}).items()
        ])

        file_diffs_str = ""
        for filename, diff in file_diffs.items():
            file_diffs_str += f"\n## {filename}\n```diff\n{diff}\n```\n"

        input_data = {
            "pr_title": pr_data.get('title', ''),
            'pr_description': pr_data.get('body', ''),
            'base_branch': pr_data.get('base_branch', ''),
            'head_branch': pr_data.get('head_branch', ''),
            'file_changes': file_changes_str,
            'file_diffs': file_diffs_str
        }

        results = self.chains['overall_review'].invoke(input_data)

        return results
        
    def _set_up_prompts(self):

        self.prompts['change_analysis'] = ChatPromptTemplate.from_messages([
            # 1. Role Definition
            SystemMessagePromptTemplate.from_template(
                """
                "You are a highly experienced senior software engineer.
                Your job is to analyze the changes introduced by this Pull Request (PR)
                and understand its purpose and impact."
                """
            ),

            # 2. Language Constraint
            SystemMessagePromptTemplate.from_template(
                """
                "You Must answer me in Korean no matter what language the user asks."
                """
            ),

            # 3. Output Instructions
            SystemMessagePromptTemplate.from_template(
                """
                "Please write your final answer in markdown format.
                Use concise, clear language, but provide enough detail for a thorough analysis."
                """
            ),

            # Final: PR Information
            HumanMessagePromptTemplate.from_template(
                """
                "Here is the PR information:
                - PR Title: {pr_title}
                - PR Description: {pr_description}
                - Branch: {base_branch} -> {head_branch}

                Here is the list of files that were changed:
                {file_changes}

                Here is the diff for each file. Analyze the changes:

                {file_diffs}

                Please analyze the changes in this PR and provide the following information:
                1. The main purpose of the change (what PR is intended to achieve)
                2. Key Implementations (how did the developer solve the problem or implement the new feature)
                3. Impact of the changes (how it will affect the system, including both positive and negative aspects)
                """
            )
        ])

        self.prompts['code_quality'] = ChatPromptTemplate.from_messages([
            # 1. Role Definition
            SystemMessagePromptTemplate.from_template(
                """
                "You are a seasoned code quality specialist, focusing on maintainability, readability, and performance."
                """
            ),

            # 2. Language Constraint
            SystemMessagePromptTemplate.from_template(
                """
                "You Must answer me in Korean no matter what language the user asks."
                """
            ),

            # 3. Output Instructions
            SystemMessagePromptTemplate.from_template(
                """
                "Format your final output in markdown.
                Provide bullet points for each area if it helps clarity."
                """
            ),

            # Final: PR Diff
            HumanMessagePromptTemplate.from_template(
                """
                "Here is the code changed in PR:
                
                {file_diffs}

                Please evaluate the quality of this code and review it from the following perspectives:
                1. Code structure and organization
                2. Readability and Naming Rules
                3. Redundant code and reuseability
                4. Performance Considerations
                5. Testability and Code Coverage

                Please specifically mention what is good and what needs to be improved from each point of view.
                You may suggest an improvment for the code if you think it's necessary with an exmaple of code.
                "
                """
            )
        ])

        self.prompts['summary'] = ChatPromptTemplate.from_messages([
            # 1. Role Definition
            SystemMessagePromptTemplate.from_template(
                """
                "You are a technical lead who synthesizes multiple review perspectives into a concise final summary."
                """
            ),

            # 2. Language Constraint
            SystemMessagePromptTemplate.from_template(
                """
                "You Must answer me in Korean no matter what language the user asks."
                """
            ),
            
            # 3. Format
            SystemMessagePromptTemplate.from_template(
                """
                "Write your final summary in markdown format with short headings for clarity.
                You may use ```suggestion``` blocks if you wnat to propose actual code changes."
                """
            ),

            # Final: Reviews
            HumanMessagePromptTemplate.from_template(
                """
                "Here are the results of the reviews of PR from sevral perspectives 
                
                ## Change Analysis
                {change_analysis}

                ## Code Quality Review
                {code_quality_review}

                Please provide a summary of the results of this review:
                1. Simplified assessment of the overall PR (1-2 sentences)
                2. Key Strengths (3-5 Items)
                3. Key improvements (3-5 Items)
                4. Suggested actions for the developer
                "
                """
            )
        ])



    def _set_up_chains(self):

        self.chains['change_analysis'] = (
            RunnablePassthrough.assign(
                change_analysis=lambda x: self.prompts['change_analysis'].invoke(x) | self.llm
            )
        )

        self.chains['code_quality'] = (
            RunnablePassthrough.assign(
                code_quality_review=lambda x: self.prompts['code_quality'].invoke(x) | self.llm
            )
        )

        self.chains['summary'] = (
            RunnablePassthrough.assign(
                review_summary=lambda x: self.prompts['summary'].invoke(x) | self.llm
            )
        )

        self.chains['overall_review'] = (
            RunnablePassthrough() | 
            self.chains['change_analysis'] | 
            self.chains['code_quality'] | 
            self.chains['summary']
        )