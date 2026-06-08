from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.data.checklist_dict import get_checklist, PRODUCT_TYPES, CONTENT_TYPES

router = APIRouter(prefix="/checklist", tags=["checklist"])


class ChecklistRequest(BaseModel):
    product_type: str
    content_type: str


class ChecklistItemDetail(BaseModel):
    item_id: str
    description: str


@router.get("/types")
def get_types():
    """지원하는 상품 유형 및 콘텐츠 유형 목록 반환"""
    return {
        "product_types": PRODUCT_TYPES,
        "content_types": CONTENT_TYPES,
    }


@router.post("/get")
def get_checklist_items(request: ChecklistRequest):
    """
    상품 유형 + 콘텐츠 유형에 맞는 체크리스트 반환
    """
    if request.product_type not in PRODUCT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 상품 유형입니다: {request.product_type}"
        )

    if request.content_type not in CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 콘텐츠 유형입니다: {request.content_type}"
        )

    checklist = get_checklist(request.product_type, request.content_type)

    # 전체 항목 수 계산
    total_items = sum(len(items) for items in checklist.values())

    return {
        "product_type": request.product_type,
        "content_type": request.content_type,
        "checklist": checklist,
        "total_items": total_items,
    }


@router.get("/item/{item_id}")
def get_item_detail(item_id: str, product_type: str, content_type: str):
    """
    특정 체크리스트 항목의 상세 설명 반환
    [설명보기] 클릭 시 호출
    """
    checklist = get_checklist(product_type, content_type)

    for category, items in checklist.items():
        for item in items:
            if item["id"] == item_id:
                return {
                    "item_id": item_id,
                    "item": item["item"],
                    "category": category,
                    "description": item["description"],
                }

    raise HTTPException(
        status_code=404,
        detail=f"항목을 찾을 수 없습니다: {item_id}"
    )