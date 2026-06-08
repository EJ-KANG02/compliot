# 체크리스트 딕셔너리
# 구조: {상품유형: {콘텐츠유형: {카테고리: [항목들]}}}

CHECKLIST = {
    "예금성": {
        "공통": {
            "콘텐츠 내용 항목": [
                {
                    "id": "dep_cont_1",
                    "item": "이자율 범위 및 산정방법 명시",
                    "description": "기본금리와 우대금리를 구분하여 명시해야 합니다.\n예시: '연 3.5% (우대조건 충족 시 최대 연 4.5%)'",
                },
                {
                    "id": "dep_cont_2",
                    "item": "이자 지급 시기 명시",
                    "description": "만기일시지급, 월지급 등 이자 지급 방식을 명시해야 합니다.",
                },
                {
                    "id": "dep_cont_3",
                    "item": "가입 기간 및 조건 명시",
                    "description": "상품의 가입 가능 기간과 조건을 명시해야 합니다.",
                },
                {
                    "id": "dep_cont_4",
                    "item": "만기지급금 예시 시 미래 수익 비보장 고지",
                    "description": "구체적 금액 예시를 사용하는 경우에만 해당됩니다.\n예시: '※ 위 금액은 예시이며 실제 지급액과 다를 수 있습니다'",
                },
                {
                    "id": "dep_cont_5",
                    "item": "예금자보호 여부 명시",
                    "description": "예금자보호법에 따른 보호 여부를 명시해야 합니다.",
                },
            ],
            "콘텐츠 형식 항목": [
                {
                    "id": "dep_form_1",
                    "item": "판매업자 명칭 표시",
                    "description": "금융회사 명칭을 명확히 표시해야 합니다.",
                },
                {
                    "id": "dep_form_2",
                    "item": "설명서·약관 읽기 권유 문구",
                    "description": "예시: '자세한 내용은 상품 설명서를 확인해주세요'",
                },
                {
                    "id": "dep_form_3",
                    "item": "혜택과 불이익 균형 전달",
                    "description": "혜택과 주의사항의 글자 크기, 색상이 균형 있게 구성되어야 합니다.",
                },
            ],
        },
        "SNS": {
            "채널별 공시 항목": [
                {
                    "id": "dep_sns_1",
                    "item": "경제적 이해관계 표시 (유료 광고 시)",
                    "description": "인플루언서 등 외부 채널 활용 시 '#광고' 또는 '#유료광고' 표기가 필요합니다.\n공식 계정 게시물은 해당 없음.",
                },
                {
                    "id": "dep_sns_2",
                    "item": "광고임을 명확히 표시",
                    "description": "금융상품 광고임을 소비자가 명확히 인식할 수 있어야 합니다.",
                },
            ],
        },
        "문자": {
            "채널별 공시 항목": [
                {
                    "id": "dep_sms_1",
                    "item": "발신자 명칭 표시",
                    "description": "문자 발신자가 금융회사임을 명확히 표시해야 합니다.",
                },
                {
                    "id": "dep_sms_2",
                    "item": "수신거부 방법 명시",
                    "description": "수신거부 방법을 반드시 포함해야 합니다.\n예시: '수신거부 080-XXX-XXXX'",
                },
            ],
        },
        "이메일": {
            "채널별 공시 항목": [
                {
                    "id": "dep_email_1",
                    "item": "[광고] 표기",
                    "description": "이메일 제목에 '[광고]' 표기가 의무입니다.",
                },
                {
                    "id": "dep_email_2",
                    "item": "수신거부 방법 명시",
                    "description": "이메일 하단에 수신거부 방법을 포함해야 합니다.",
                },
            ],
        },
        "배너": {
            "채널별 공시 항목": [
                {
                    "id": "dep_banner_1",
                    "item": "상세 조건 페이지 연결",
                    "description": "배너 공간 제약으로 조건을 다 명시하기 어려운 경우 상세 조건 페이지 링크를 제공해야 합니다.",
                },
            ],
        },
        "상품소개": {
            "채널별 공시 항목": [
                {
                    "id": "dep_prod_1",
                    "item": "상품 설명서 및 약관 링크 또는 첨부",
                    "description": "상품 설명서와 약관을 확인할 수 있는 경로를 제공해야 합니다.",
                },
            ],
        },
    },

    "대출성": {
        "공통": {
            "콘텐츠 내용 항목": [
                {
                    "id": "loan_cont_1",
                    "item": "금리 범위 명시 (최저~최고)",
                    "description": "대출 금리의 최저~최고 범위를 명시해야 합니다.\n예시: '연 3.5% ~ 15.0% (신용도에 따라 차등 적용)'",
                },
                {
                    "id": "loan_cont_2",
                    "item": "연체이자율 명시",
                    "description": "연체 시 적용되는 이자율을 명시해야 합니다.",
                },
                {
                    "id": "loan_cont_3",
                    "item": "조기상환수수료 명시",
                    "description": "조기상환 시 발생하는 수수료를 명시해야 합니다. 없는 경우 '조기상환수수료 없음' 명시.",
                },
                {
                    "id": "loan_cont_4",
                    "item": "대출 한도 및 기간 명시",
                    "description": "대출 가능 한도와 기간을 명시해야 합니다.",
                },
                {
                    "id": "loan_cont_5",
                    "item": "과도한 대출 경고 문구",
                    "description": "예시: '대출 전 상환 능력을 반드시 확인하세요'",
                },
            ],
            "콘텐츠 형식 항목": [
                {
                    "id": "loan_form_1",
                    "item": "판매업자 명칭 표시",
                    "description": "금융회사 명칭을 명확히 표시해야 합니다.",
                },
                {
                    "id": "loan_form_2",
                    "item": "설명서·약관 읽기 권유 문구",
                    "description": "예시: '자세한 내용은 상품 설명서를 확인해주세요'",
                },
            ],
        },
        "SNS": {
            "채널별 공시 항목": [
                {
                    "id": "loan_sns_1",
                    "item": "경제적 이해관계 표시 (유료 광고 시)",
                    "description": "인플루언서 등 외부 채널 활용 시 '#광고' 표기가 필요합니다.",
                },
            ],
        },
        "문자": {
            "채널별 공시 항목": [
                {
                    "id": "loan_sms_1",
                    "item": "수신거부 방법 명시",
                    "description": "수신거부 방법을 반드시 포함해야 합니다.",
                },
            ],
        },
        "이메일": {
            "채널별 공시 항목": [
                {
                    "id": "loan_email_1",
                    "item": "[광고] 표기",
                    "description": "이메일 제목에 '[광고]' 표기가 의무입니다.",
                },
                {
                    "id": "loan_email_2",
                    "item": "수신거부 방법 명시",
                    "description": "이메일 하단에 수신거부 방법을 포함해야 합니다.",
                },
            ],
        },
        "배너": {
            "채널별 공시 항목": [
                {
                    "id": "loan_banner_1",
                    "item": "상세 조건 페이지 연결",
                    "description": "금리 조건 등 상세 내용을 확인할 수 있는 링크를 제공해야 합니다.",
                },
            ],
        },
        "상품소개": {
            "채널별 공시 항목": [
                {
                    "id": "loan_prod_1",
                    "item": "상품 설명서 및 약관 링크 또는 첨부",
                    "description": "상품 설명서와 약관을 확인할 수 있는 경로를 제공해야 합니다.",
                },
            ],
        },
    },

    "투자성": {
        "공통": {
            "콘텐츠 내용 항목": [
                {
                    "id": "inv_cont_1",
                    "item": "투자 위험 고지",
                    "description": "투자에 따른 위험을 명시해야 합니다.\n예시: '투자 원금의 일부 또는 전부를 잃을 수 있습니다'",
                },
                {
                    "id": "inv_cont_2",
                    "item": "원금손실 가능성 명시",
                    "description": "원금 손실 가능성을 명확히 고지해야 합니다.",
                },
                {
                    "id": "inv_cont_3",
                    "item": "과거 수익률 미래 보장 아님 고지",
                    "description": "과거 운용실적을 포함하는 경우 반드시 포함해야 합니다.\n예시: '과거 수익률이 미래 수익을 보장하지 않습니다'",
                },
                {
                    "id": "inv_cont_4",
                    "item": "투자 전 설명서 확인 권유",
                    "description": "투자설명서를 반드시 읽어볼 것을 권유하는 문구가 필요합니다.",
                },
            ],
            "콘텐츠 형식 항목": [
                {
                    "id": "inv_form_1",
                    "item": "판매업자 명칭 표시",
                    "description": "금융회사 명칭을 명확히 표시해야 합니다.",
                },
                {
                    "id": "inv_form_2",
                    "item": "위험 고지 문구 크기",
                    "description": "위험 고지 문구는 본문 글자 크기 이상으로 표시해야 합니다.",
                },
            ],
        },
        "SNS": {
            "채널별 공시 항목": [
                {
                    "id": "inv_sns_1",
                    "item": "경제적 이해관계 표시 (유료 광고 시)",
                    "description": "인플루언서 등 외부 채널 활용 시 '#광고' 표기가 필요합니다.",
                },
            ],
        },
        "문자": {
            "채널별 공시 항목": [
                {
                    "id": "inv_sms_1",
                    "item": "수신거부 방법 명시",
                    "description": "수신거부 방법을 반드시 포함해야 합니다.",
                },
            ],
        },
        "이메일": {
            "채널별 공시 항목": [
                {
                    "id": "inv_email_1",
                    "item": "[광고] 표기",
                    "description": "이메일 제목에 '[광고]' 표기가 의무입니다.",
                },
                {
                    "id": "inv_email_2",
                    "item": "수신거부 방법 명시",
                    "description": "이메일 하단에 수신거부 방법을 포함해야 합니다.",
                },
            ],
        },
        "배너": {
            "채널별 공시 항목": [
                {
                    "id": "inv_banner_1",
                    "item": "상세 조건 페이지 연결",
                    "description": "투자 위험 등 상세 내용을 확인할 수 있는 링크를 제공해야 합니다.",
                },
            ],
        },
        "상품소개": {
            "채널별 공시 항목": [
                {
                    "id": "inv_prod_1",
                    "item": "투자설명서 및 약관 링크 또는 첨부",
                    "description": "투자설명서와 약관을 확인할 수 있는 경로를 제공해야 합니다.",
                },
            ],
        },
    },

    "보장성": {
        "공통": {
            "콘텐츠 내용 항목": [
                {
                    "id": "ins_cont_1",
                    "item": "보장 내용 및 한도 명시",
                    "description": "주요 보장 내용과 한도를 명시해야 합니다.",
                },
                {
                    "id": "ins_cont_2",
                    "item": "보험료 및 납입 기간 명시",
                    "description": "보험료와 납입 기간을 명시해야 합니다.",
                },
                {
                    "id": "ins_cont_3",
                    "item": "계약 해지 시 보험료 인상 가능성 고지",
                    "description": "기존 계약 해지 후 재가입 시 보험료 인상 가능성을 고지해야 합니다.",
                },
                {
                    "id": "ins_cont_4",
                    "item": "보장 내용 변경 가능성 고지",
                    "description": "보장 내용이 변경될 수 있음을 고지해야 합니다.",
                },
                {
                    "id": "ins_cont_5",
                    "item": "면책사항 명시",
                    "description": "보험금이 지급되지 않는 주요 면책사항을 명시해야 합니다.",
                },
            ],
            "콘텐츠 형식 항목": [
                {
                    "id": "ins_form_1",
                    "item": "판매업자 명칭 표시",
                    "description": "금융회사 명칭을 명확히 표시해야 합니다.",
                },
                {
                    "id": "ins_form_2",
                    "item": "설명서·약관 읽기 권유 문구",
                    "description": "예시: '자세한 내용은 상품 설명서를 확인해주세요'",
                },
            ],
        },
        "SNS": {
            "채널별 공시 항목": [
                {
                    "id": "ins_sns_1",
                    "item": "경제적 이해관계 표시 (유료 광고 시)",
                    "description": "인플루언서 등 외부 채널 활용 시 '#광고' 표기가 필요합니다.",
                },
            ],
        },
        "문자": {
            "채널별 공시 항목": [
                {
                    "id": "ins_sms_1",
                    "item": "수신거부 방법 명시",
                    "description": "수신거부 방법을 반드시 포함해야 합니다.",
                },
            ],
        },
        "이메일": {
            "채널별 공시 항목": [
                {
                    "id": "ins_email_1",
                    "item": "[광고] 표기",
                    "description": "이메일 제목에 '[광고]' 표기가 의무입니다.",
                },
                {
                    "id": "ins_email_2",
                    "item": "수신거부 방법 명시",
                    "description": "이메일 하단에 수신거부 방법을 포함해야 합니다.",
                },
            ],
        },
        "배너": {
            "채널별 공시 항목": [
                {
                    "id": "ins_banner_1",
                    "item": "상세 조건 페이지 연결",
                    "description": "보장 내용 등 상세 내용을 확인할 수 있는 링크를 제공해야 합니다.",
                },
            ],
        },
        "상품소개": {
            "채널별 공시 항목": [
                {
                    "id": "ins_prod_1",
                    "item": "상품 설명서 및 약관 링크 또는 첨부",
                    "description": "상품 설명서와 약관을 확인할 수 있는 경로를 제공해야 합니다.",
                },
            ],
        },
    },
}

# 공통 금지 표현 항목 (모든 상품/콘텐츠 유형에 적용)
FORBIDDEN_EXPRESSION_CHECKLIST = [
    {
        "id": "forbidden_1",
        "item": "최상급 표현 미사용",
        "description": "객관적 근거 없이 '최고', '최저', '최대', '1위', '업계 유일' 등의 표현을 사용할 수 없습니다.",
    },
    {
        "id": "forbidden_2",
        "item": "원금보장 표현 미사용",
        "description": "예금 외 상품에서 '원금보장', '원금보전' 등의 표현을 사용할 수 없습니다.",
    },
    {
        "id": "forbidden_3",
        "item": "근거 없는 비교 표현 미사용",
        "description": "비교 대상과 기준을 명시하지 않은 비교 표현을 사용할 수 없습니다.\n예: '타사 대비 금리 높음' → 비교 근거 필요",
    },
    {
        "id": "forbidden_4",
        "item": "소비자 오인 유발 표현 미사용",
        "description": "소비자가 상품의 위험성이나 조건을 오해할 수 있는 표현을 사용할 수 없습니다.",
    },
    {
        "id": "forbidden_5",
        "item": "과도한 urgency 표현 미사용",
        "description": "'지금 아니면 끝', '오늘만' 등 소비자의 합리적 의사결정을 방해하는 표현을 사용할 수 없습니다.",
    },
]


def get_checklist(product_type: str, content_type: str) -> dict:
    """
    상품 유형과 콘텐츠 유형에 맞는 체크리스트를 반환합니다.
    """
    result = {}

    if product_type not in CHECKLIST:
        return {"error": f"지원하지 않는 상품 유형입니다: {product_type}"}

    product_data = CHECKLIST[product_type]

    # 공통 항목 추가
    if "공통" in product_data:
        for category, items in product_data["공통"].items():
            if category not in result:
                result[category] = []
            result[category].extend(items)

    # 콘텐츠 유형별 항목 추가
    if content_type in product_data:
        for category, items in product_data[content_type].items():
            if category not in result:
                result[category] = []
            result[category].extend(items)

    # 금지 표현 항목 추가 (항상 포함)
    result["금지 표현 항목"] = FORBIDDEN_EXPRESSION_CHECKLIST

    return result


# 지원 유형 목록
PRODUCT_TYPES = ["예금성", "대출성", "투자성", "보장성"]
CONTENT_TYPES = ["SNS", "배너", "문자", "이메일", "상품소개"]