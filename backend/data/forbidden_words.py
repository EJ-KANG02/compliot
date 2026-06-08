import re

# =====================================================
# 금지 표현 딕셔너리
# 근거: 금소법 22조, 금융위 광고규제 가이드라인,
#       은행연합회 광고심의 기준, 표시광고법
# =====================================================

# 1. 즉시 감지 금지 키워드 (Rule-based 1차 필터)
FORBIDDEN_KEYWORDS = {
    "원금보장": {
        "keywords": ["원금보장", "원금보전", "원금 보장", "원금 보전"],
        "severity": "즉시수정",
        "reason": "원금보장 표현 금지 (금소법 22조)",
        "suggestion": "예금성 상품의 경우 '예금자보호법에 따라 보호됩니다'로 대체하세요.",
    },
    "최상급표현": {
        "keywords": [
            "최고", "최저", "최대", "최소", "최상", "최초",
            "1위", "업계 1위", "업계 최고", "업계 최저",
            "국내 최고", "국내 최저", "유일한", "업계 유일"
        ],
        "severity": "검토필요",
        "reason": "근거 없는 최상급 표현 금지 (은행연합회 광고심의 기준)",
        "suggestion": "객관적 근거가 있는 경우 출처를 명시하거나 표현을 수정하세요.",
    },
    "수익보장": {
        "keywords": [
            "수익보장", "수익 보장", "이익보장", "이익 보장",
            "확정수익", "확정 수익", "무조건 수익"
        ],
        "severity": "즉시수정",
        "reason": "수익보장 표현 금지 (금소법 22조)",
        "suggestion": "투자 결과는 보장되지 않음을 명시하세요.",
    },
    "과도한urgency": {
        "keywords": [
            "지금 아니면", "오늘만", "마지막 기회", "한정 수량",
            "선착순 마감", "무조건", "반드시", "절대"
        ],
        "severity": "검토필요",
        "reason": "소비자 합리적 의사결정 방해 표현 주의 (금소법)",
        "suggestion": "소비자의 합리적 판단을 유도하는 표현으로 수정하세요.",
    },
    "허위과장": {
        "keywords": [
            "완전 무료", "100% 무료", "절대 손해없음",
            "무조건 승인", "누구나 가능", "조건 없음"
        ],
        "severity": "즉시수정",
        "reason": "허위·과장 광고 금지 (표시광고법)",
        "suggestion": "실제 조건과 제한사항을 명확히 명시하세요.",
    },
}

# 2. 필수 포함 문구 패턴 (정규식)
REQUIRED_PATTERNS = {
    "예금성": {
        "수신거부_문자": {
            "pattern": r"수신거부|080|수신\s*거부",
            "content_types": ["문자"],
            "description": "수신거부 방법 명시 필요",
        },
        "광고표기_이메일": {
            "pattern": r"\[광고\]|\[AD\]",
            "content_types": ["이메일"],
            "description": "[광고] 표기 필요",
        },
        "이자율명시": {
            "pattern": r"연\s*\d+\.?\d*\s*%|금리\s*\d+\.?\d*\s*%|\d+\.?\d*\s*%",
            "content_types": ["SNS", "배너", "문자", "이메일", "상품소개"],
            "description": "이자율 명시 필요",
        },
    },
    "대출성": {
        "수신거부_문자": {
            "pattern": r"수신거부|080|수신\s*거부",
            "content_types": ["문자"],
            "description": "수신거부 방법 명시 필요",
        },
        "광고표기_이메일": {
            "pattern": r"\[광고\]|\[AD\]",
            "content_types": ["이메일"],
            "description": "[광고] 표기 필요",
        },
        "금리범위": {
            "pattern": r"\d+\.?\d*\s*%\s*~\s*\d+\.?\d*\s*%|\d+\.?\d*\s*%",
            "content_types": ["SNS", "배너", "문자", "이메일", "상품소개"],
            "description": "금리 범위 명시 필요",
        },
    },
    "투자성": {
        "수신거부_문자": {
            "pattern": r"수신거부|080|수신\s*거부",
            "content_types": ["문자"],
            "description": "수신거부 방법 명시 필요",
        },
        "광고표기_이메일": {
            "pattern": r"\[광고\]|\[AD\]",
            "content_types": ["이메일"],
            "description": "[광고] 표기 필요",
        },
        "위험고지": {
            "pattern": r"원금\s*손실|투자\s*위험|손실\s*가능|위험성",
            "content_types": ["SNS", "배너", "문자", "이메일", "상품소개"],
            "description": "투자 위험 고지 필요",
        },
    },
    "보장성": {
        "수신거부_문자": {
            "pattern": r"수신거부|080|수신\s*거부",
            "content_types": ["문자"],
            "description": "수신거부 방법 명시 필요",
        },
        "광고표기_이메일": {
            "pattern": r"\[광고\]|\[AD\]",
            "content_types": ["이메일"],
            "description": "[광고] 표기 필요",
        },
        "면책사항": {
            "pattern": r"면책|보장\s*제외|지급\s*제외|보험금\s*미지급",
            "content_types": ["상품소개"],
            "description": "면책사항 명시 필요",
        },
    },
}


def check_forbidden_keywords(text: str) -> list:
    """
    텍스트에서 금지 키워드를 검사합니다.
    반환: [{category, keyword, severity, reason, suggestion}]
    """
    results = []
    for category, data in FORBIDDEN_KEYWORDS.items():
        for keyword in data["keywords"]:
            if keyword in text:
                results.append({
                    "category": category,
                    "keyword": keyword,
                    "severity": data["severity"],
                    "reason": data["reason"],
                    "suggestion": data["suggestion"],
                })
                break  # 카테고리당 첫 번째 매칭만
    return results


def check_required_patterns(
    text: str,
    product_type: str,
    content_type: str
) -> list:
    """
    텍스트에서 필수 포함 문구를 검사합니다.
    반환: [{pattern_name, description, is_present}]
    """
    results = []
    if product_type not in REQUIRED_PATTERNS:
        return results

    for pattern_name, data in REQUIRED_PATTERNS[product_type].items():
        if content_type in data["content_types"]:
            is_present = bool(re.search(data["pattern"], text))
            results.append({
                "pattern_name": pattern_name,
                "description": data["description"],
                "is_present": is_present,
                "severity": "즉시수정" if not is_present else "충족",
            })
    return results


def run_rule_based_check(
    text: str,
    product_type: str,
    content_type: str
) -> dict:
    """
    Rule-based 1차 필터 실행
    금지 키워드 + 필수 문구 패턴 검사
    """
    forbidden = check_forbidden_keywords(text)
    required = check_required_patterns(text, product_type, content_type)

    return {
        "forbidden_keywords": forbidden,
        "required_patterns": required,
        "has_critical_issues": any(
            f["severity"] == "즉시수정" for f in forbidden
        ) or any(
            r["severity"] == "즉시수정" for r in required
        ),
    }