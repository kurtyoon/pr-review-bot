from typing import Dict
from datetime import datetime

class MarkdownUtil:

    @staticmethod
    def format_markdown(review_result: Dict[str, str]) -> str:

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        header = f"""
    # 🧐 코드 리뷰 결과

    > 🕒 **리뷰 시간**: {current_time}

    """
        summary_section = f"""
    ## 📝 종합 평가

    {review_result.get('review_summary', '리뷰 요약을 생성할 수 없습니다.')}

    ---
    """
        
        # 코드 품질 섹션
        quality_section = f"""
    <details>
    <summary><strong>⚙️ 코드 품질 분석</strong></summary>

    {review_result.get('code_quality_review', '코드 품질 분석을 생성할 수 없습니다.')}
    </details>

    """
        
        # 바닥글
        footer = """
    ---

    <sub>이 리뷰는 LLM 기반 코드 리뷰 봇에 의해 자동으로 생성되었습니다.</sub>
    """

        return header + summary_section + quality_section + footer