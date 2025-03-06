# 🧐 코드 리뷰 봇 (Code Review Bot)

자동으로 GitHub Pull Request를 분석하고 상세한 코드 리뷰를 제공하는 GitHub Action입니다. OpenAI의 GPT 모델을 활용하여 코드 품질, 구조, 가독성에 대한 전문적인 피드백을 제공합니다.

## ✨ 주요 기능

- **코드 변경 분석**: PR에서 변경된 코드를 자동으로 분석하고 주요 목적과 영향 평가
- **품질 평가**: 코드 구조, 가독성, 성능, 재사용성 관점에서 코드 품질 분석
- **종합 리뷰 요약**: 주요 강점과 개선점을 포함한 전체 리뷰 요약 제공
- **자동 PR 코멘트**: 리뷰 결과를 PR에 자동으로 코멘트로 작성
- **한국어 지원**: 모든 피드백은 한국어로 제공됨

## 🚀 사용 방법

### 1. 워크플로우 설정

레포지토리의 `.github/workflows` 디렉토리에 다음 내용의 YAML 파일을 생성하세요:

```yaml
name: Code Review Bot

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Run Code Review Bot
        uses: kurtyoon/pr-review-bot@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          pr_number: ${{ github.event.pull_request.number }}
```

### 2. GitHub Secrets 설정

레포지토리의 Settings > Secrets and variables > Actions 메뉴에서 다음 Secret을 추가하세요:

- `OPENAI_API_KEY`: OpenAI API 키 ([OpenAI 웹사이트](https://platform.openai.com/api-keys)에서 발급 가능)

`GITHUB_TOKEN`은 GitHub Actions에서 자동으로 제공됩니다.

### 3. 사용하기

설정 완료 후 PR을 생성하거나 업데이트하면 코드 리뷰 봇이 자동으로 실행되고, 리뷰 결과가 PR에 코멘트로 추가됩니다.

## 📋 리뷰 결과 예시

코드 리뷰 봇은 다음과 같은 구조의 리뷰를 제공합니다:

```markdown
# 🧐 코드 리뷰 결과

## 📝 종합 평가

이 PR은 사용자 인증 시스템에 새로운 기능을 추가합니다...

### 주요 강점

- 명확한 함수 구조
- 적절한 오류 처리
- 일관된 코딩 스타일

### 개선 필요 사항

- 일부 코드 중복 발견
- 테스트 코드 부족
- 성능 최적화 필요

### 제안 사항

...

## ⚙️ 코드 품질 분석 (세부사항)

...
```

## ⚙️ 기술 스택

- LangChain: 다중 단계 프롬프트 체인 구현
- OpenAI GPT-4o (기본값: gpt-4o-mini): 코드 분석 및 리뷰 생성
- PyGitHub: GitHub API 연동
- Docker: 컨테이너화된 실행 환경

## ⚠️ 제한 사항

- 바이너리 파일(이미지, 실행 파일 등)은 분석하지 않습니다.
- 대규모 PR(파일 변경이 많은 경우)에서는 일부 파일만 분석할 수 있습니다.
- API 사용량에 따라 OpenAI 비용이 발생할 수 있습니다.

## 🤝 기여하기

버그 리포트, 기능 요청, PR 등 모든 형태의 기여를 환영합니다!

---

<sub>이 코드 리뷰 봇은 OpenAI GPT 모델을 활용하여 AI 기반 코드 리뷰를 제공합니다. 항상 정확하지 않을 수 있으므로, 최종 판단은 개발자의 몫입니다.</sub>

```

```
