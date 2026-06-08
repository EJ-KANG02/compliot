import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =====================================================
# 시스템 프롬프트 (LLM 역할 및 출력 규칙 정의)
# =====================================================
SYSTEM_PROMPT = """
당신은 대한민국 금융 광고 준법 심의 전문가입니다.
금융소비자보호법(금소법), 금융위원회 광고규제 가이드라인, 공정거래위원회 심사지침을 기반으로 금융 콘텐츠를 심의합니다.

## 역할
- 금융 마케터가 작성한 콘텐츠의 준법 리스크를 분석합니다.
- 반드시 제공된 법령 조항만을 근거로 판단합니다. 없는 조항을 만들어내지 마세요.
- 판단이 불확실한 경우 confidence를 낮게 표시하고 담당자 확인을 요청하세요.

## 출력 규칙 (반드시 준수)
- reason: 핵심 판단 근거만 1~2문장으로 작성. 불필요한 설명 금지.
- suggestion: 미충족 시 "예시: [구체적 수정 문구]" 형태로 1개만. 충족이면 반드시 null.
- legal_basis: 관련 법령 조항명만 간단히. 없으면 null.
"""


# =====================================================
# 전체 준법 검사
# 용도: [전체 검사하기] 버튼 클릭 시 호출
# =====================================================
def analyze_compliance(
    content: str,
    product_type: str,
    content_type: str,
    checklist: dict,
    legal_contexts: dict,
) -> dict:
    # 체크리스트 항목 평탄화
    all_items = []
    for category, items in checklist.items():
        for item in items:
            all_items.append({"category": category, **item})

    # 법령 컨텍스트 정리 (카테고리별 상위 2개)
    legal_context_text = ""
    for chunks in legal_contexts.values():
        for chunk in chunks[:2]:
            legal_context_text += f"\n---\n{chunk['content']}\n"

    prompt = f"""
## 관련 법령 조항
{legal_context_text}

## 체크리스트 항목
{json.dumps(all_items, ensure_ascii=False, indent=2)}

## 분석할 콘텐츠
상품 유형: {product_type}
콘텐츠 유형: {content_type}
콘텐츠 내용:
{content}

위 체크리스트의 각 항목이 콘텐츠에서 충족되는지 분석하고,
전체 맥락에서 소비자 오인 유발 위험도 함께 분석해주세요.
반드시 아래 JSON 형식으로만 응답하세요.

{{
  "checklist_results": [
    {{
      "item_id": "항목 ID",
      "item": "항목명",
      "status": "충족" | "미충족" | "해당없음",
      "confidence": 0.0 ~ 1.0,
      "reason": "1~2문장",
      "legal_basis": "법령 조항명 또는 null",
      "suggestion": "예시: ... 또는 null"
    }}
  ],
  "context_analysis": {{
    "has_overall_risk": true | false,
    "overall_risk_description": "설명 또는 null",
    "confidence": 0.0 ~ 1.0
  }},
  "summary": {{
    "total_items": 0,
    "satisfied": 0,
    "unsatisfied": 0,
    "not_applicable": 0
  }}
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(response.content[0].text)


# =====================================================
# 체크리스트 자동 생성 (RAG 구축 후 1회 실행용)
# 용도: 법령 문서 기반으로 체크리스트 초안 자동 생성
#       관리자 검토·승인 후 checklist_dict.py에 반영
# =====================================================
def generate_checklist_from_laws(legal_text: str) -> dict:
    prompt = f"""
아래 금융 법령 및 가이드라인을 읽고,
금융 광고 콘텐츠 심의 시 필요한 체크리스트 항목을 추출해주세요.

## 법령 내용
{legal_text}

## 출력 형식
아래 JSON 형식으로만 응답하세요.
{{
  "checklist_items": [
    {{
      "category": "필수기재사항" | "형식요건" | "금지표현" | "채널공시",
      "product_type": "예금성" | "대출성" | "투자성" | "보장성" | "공통",
      "content_type": "공통" | "SNS" | "문자" | "이메일" | "배너" | "상품소개",
      "item": "항목명",
      "description": "항목 설명 및 작성 가이드",
      "legal_basis": "근거 법령 조항"
    }}
  ]
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(response.content[0].text)


# =====================================================
# 공통 JSON 파싱 유틸
# =====================================================
def _parse_json(text: str) -> dict:
    try:
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        return {"error": f"응답 파싱 실패: {str(e)}", "raw_response": text}