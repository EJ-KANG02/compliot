import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import anthropic

from backend.data.checklist_dict import get_checklist
from backend.data.forbidden_words import run_rule_based_check
from backend.services.rag import search_documents
from backend.services.llm import analyze_compliance, _parse_json

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

router = APIRouter(prefix="/analysis", tags=["analysis"])

# =====================================================
# 요청 모델
# =====================================================
class AnalysisRequest(BaseModel):
    content: str
    product_type: str
    content_type: str


class ChecklistItem(BaseModel):
    id: str
    item: str
    description: str


class CategoryAnalysisRequest(BaseModel):
    content: str
    product_type: str
    content_type: str
    category: str
    items: List[ChecklistItem]


# =====================================================
# 전체 준법 검사
# 용도: [전체 검사하기] 버튼 클릭 시
# =====================================================
@router.post("/full")
def full_analysis(request: AnalysisRequest):
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="콘텐츠를 입력해주세요.")

    # Step 1: Rule-based 1차 필터
    rule_result = run_rule_based_check(
        request.content,
        request.product_type,
        request.content_type,
    )

    # Step 2: 체크리스트 + RAG 검색
    checklist = get_checklist(request.product_type, request.content_type)
    legal_contexts = {}
    for category in checklist.keys():
        legal_contexts[category] = search_documents(
            query=f"{request.product_type} {request.content_type} {category}",
            product_type=request.product_type,
            content_type=request.content_type,
            n_results=3,
        )

    # Step 3: LLM 전체 분석
    llm_result = analyze_compliance(
        content=request.content,
        product_type=request.product_type,
        content_type=request.content_type,
        checklist=checklist,
        legal_contexts=legal_contexts,
    )

    return {
        "product_type": request.product_type,
        "content_type": request.content_type,
        "content": request.content,
        "rule_based": rule_result,
        "llm_analysis": llm_result,
    }


# =====================================================
# 카테고리 단위 검사
# 용도: 체크리스트 카테고리 [검사하기] 버튼 클릭 시
#       카테고리 안 항목들을 LLM 1회 호출로 한 번에 분석
#       결과는 항목별로 반환
# =====================================================
@router.post("/category")
def category_analysis(request: CategoryAnalysisRequest):
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="콘텐츠를 입력해주세요.")

    # RAG 검색
    legal_context = search_documents(
        query=f"{request.product_type} {request.content_type} {request.category}",
        product_type=request.product_type,
        content_type=request.content_type,
        n_results=5,
    )
    legal_context_text = "\n---\n".join(
        [chunk["content"] for chunk in legal_context[:3]]
    ) if legal_context else "관련 법령 조항 없음"

    # 항목 목록
    items_text = json.dumps(
        [{"id": i.id, "item": i.item, "description": i.description}
         for i in request.items],
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
## 관련 법령 조항
{legal_context_text}

## 분석할 카테고리
{request.category}

## 카테고리 내 체크리스트 항목
{items_text}

## 분석할 콘텐츠
상품 유형: {request.product_type}
콘텐츠 유형: {request.content_type}
콘텐츠 내용:
{request.content}

## 출력 규칙 (반드시 준수)
- reason: 핵심 판단 근거만 1~2문장으로 작성. 불필요한 설명 금지.
- suggestion: 미충족 시 "예시: [구체적 수정 문구]" 형태로 1개만. 충족이면 반드시 null.
- legal_basis: 관련 법령 조항명만 간단히. 없으면 null.

위 체크리스트 항목 각각에 대해 콘텐츠가 충족하는지 분석하세요.
제공된 법령 조항만을 근거로 판단하고, 없는 조항은 만들지 마세요.
반드시 아래 JSON 형식으로만 응답하세요.

{{
  "category": "{request.category}",
  "items": [
    {{
      "id": "항목 ID",
      "item": "항목명",
      "status": "충족" | "미충족" | "해당없음",
      "confidence": 0.0 ~ 1.0,
      "reason": "1~2문장",
      "legal_basis": "법령 조항명 또는 null",
      "suggestion": "예시: ... 또는 null"
    }}
  ],
  "category_summary": {{
    "satisfied": 0,
    "unsatisfied": 0,
    "not_applicable": 0
  }}
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(response.content[0].text)