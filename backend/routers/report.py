from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER

router = APIRouter(prefix="/report", tags=["report"])


class ReportRequest(BaseModel):
    product_type: str
    content_type: str
    content: str
    rule_based: dict
    llm_analysis: dict
    created_at: Optional[str] = None


def register_korean_font():
    """한국어 폰트 등록"""
    try:
        # Windows 기본 폰트 경로
        font_paths = [
            "C:/Windows/Fonts/malgun.ttf",    # 맑은 고딕
            "C:/Windows/Fonts/NanumGothic.ttf",
            "C:/Windows/Fonts/gulim.ttc",
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont("Korean", font_path))
                return "Korean"
    except Exception:
        pass
    return "Helvetica"


@router.post("/generate")
def generate_report(request: ReportRequest):
    """
    심의 리포트 PDF 생성 및 반환
    """
    font_name = register_korean_font()

    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf", prefix="compliot_report_"
    ) as tmp:
        tmp_path = tmp.name

    # PDF 생성
    doc = SimpleDocTemplate(
        tmp_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    # 스타일 정의
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        fontName=font_name,
        fontSize=18,
        textColor=colors.HexColor("#1F4E79"),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontName=font_name,
        fontSize=11,
        textColor=colors.HexColor("#666666"),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        "Heading",
        fontName=font_name,
        fontSize=13,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=16,
        spaceAfter=8,
        fontWeight="bold",
    )
    normal_style = ParagraphStyle(
        "Normal",
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=4,
        leading=16,
    )
    warning_style = ParagraphStyle(
        "Warning",
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor("#CC0000"),
        spaceAfter=4,
    )
    success_style = ParagraphStyle(
        "Success",
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor("#006600"),
        spaceAfter=4,
    )

    story = []
    created_at = request.created_at or datetime.now().strftime("%Y년 %m월 %d일 %H:%M")

    # =====================================================
    # 헤더
    # =====================================================
    story.append(Paragraph("Compliot AI 심의 리포트", title_style))
    story.append(Paragraph(f"생성일시: {created_at}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1F4E79")))
    story.append(Spacer(1, 0.3*cm))

    # =====================================================
    # 1. 콘텐츠 기본 정보
    # =====================================================
    story.append(Paragraph("1. 콘텐츠 기본 정보", heading_style))

    info_data = [
        ["상품 유형", request.product_type],
        ["콘텐츠 유형", request.content_type],
        ["생성 일시", created_at],
    ]
    info_table = Table(info_data, colWidths=[4*cm, 13*cm])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D6E4F0")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F4E79")),
        ("FONTWEIGHT", (0, 0), (0, -1), "BOLD"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*cm))

    # 원본 콘텐츠
    story.append(Paragraph("원본 콘텐츠", heading_style))
    content_data = [[request.content]]
    content_table = Table(content_data, colWidths=[17*cm])
    content_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8F8F8")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(content_table)

    # =====================================================
    # 2. AI 심의 요약
    # =====================================================
    story.append(Paragraph("2. AI 심의 요약", heading_style))

    summary = request.llm_analysis.get("summary", {})
    satisfied = summary.get("satisfied", 0)
    unsatisfied = summary.get("unsatisfied", 0)
    not_applicable = summary.get("not_applicable", 0)
    total = summary.get("total_items", 0)

    # Rule-based 결과
    rule_forbidden = request.rule_based.get("forbidden_keywords", [])
    rule_required = request.rule_based.get("required_patterns", [])
    has_critical = request.rule_based.get("has_critical_issues", False)

    summary_data = [
        ["구분", "건수", "비고"],
        ["✅ 충족", str(satisfied), ""],
        ["⚠️ 미충족", str(unsatisfied), "수정 필요"],
        ["— 해당없음", str(not_applicable), ""],
        ["전체 항목", str(total), ""],
    ]
    if rule_forbidden:
        summary_data.append(["🚫 금지표현 감지", str(len(rule_forbidden)), "즉시 수정 필요"])

    summary_table = Table(summary_data, colWidths=[6*cm, 4*cm, 7*cm])
    summary_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTWEIGHT", (0, 0), (-1, 0), "BOLD"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
    ]))
    story.append(summary_table)

    # =====================================================
    # 3. Rule-based 1차 필터 결과
    # =====================================================
    if rule_forbidden or rule_required:
        story.append(Paragraph("3. Rule-based 1차 필터 결과", heading_style))

        if rule_forbidden:
            story.append(Paragraph("🚫 감지된 금지 표현", normal_style))
            for item in rule_forbidden:
                story.append(Paragraph(
                    f"• [{item['severity']}] '{item['keyword']}' — {item['reason']}",
                    warning_style
                ))
                story.append(Paragraph(
                    f"  💡 {item['suggestion']}",
                    normal_style
                ))

        if rule_required:
            story.append(Spacer(1, 0.2*cm))
            story.append(Paragraph("📋 필수 문구 체크", normal_style))
            for item in rule_required:
                status_icon = "✅" if item["is_present"] else "⚠️"
                style = success_style if item["is_present"] else warning_style
                story.append(Paragraph(
                    f"{status_icon} {item['description']} — {'충족' if item['is_present'] else '미충족'}",
                    style
                ))

    # =====================================================
    # 4. 항목별 AI 심의 결과
    # =====================================================
    story.append(Paragraph("4. 항목별 AI 심의 결과", heading_style))

    checklist_results = request.llm_analysis.get("checklist_results", [])

    if checklist_results:
        result_data = [["항목", "상태", "신뢰도", "판단 근거"]]
        for item in checklist_results:
            status = item.get("status", "")
            status_icon = "✅" if status == "충족" else ("⚠️" if status == "미충족" else "—")
            confidence = item.get("confidence", 0)
            result_data.append([
                item.get("item", ""),
                f"{status_icon} {status}",
                f"{int(confidence * 100)}%",
                item.get("reason", "")[:80] + "..." if len(item.get("reason", "")) > 80 else item.get("reason", ""),
            ])

        result_table = Table(result_data, colWidths=[4.5*cm, 2.5*cm, 2*cm, 8*cm])
        result_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
            ("WORDWRAP", (0, 0), (-1, -1), True),
        ]))
        story.append(result_table)

    # =====================================================
    # 5. 수정 제안
    # =====================================================
    unsatisfied_items = [
        r for r in checklist_results if r.get("status") == "미충족"
    ]

    if unsatisfied_items:
        story.append(Paragraph("5. 수정 제안", heading_style))
        for item in unsatisfied_items:
            story.append(Paragraph(
                f"⚠️ {item.get('item', '')}",
                warning_style
            ))
            if item.get("legal_basis"):
                story.append(Paragraph(
                    f"  근거: {item['legal_basis']}",
                    normal_style
                ))
            if item.get("suggestion"):
                story.append(Paragraph(
                    f"  💡 수정 제안: {item['suggestion']}",
                    normal_style
                ))
            story.append(Spacer(1, 0.2*cm))

    # =====================================================
    # 6. 전체 맥락 분석
    # =====================================================
    context_analysis = request.llm_analysis.get("context_analysis", {})
    if context_analysis.get("has_overall_risk"):
        story.append(Paragraph("6. 전체 맥락 오인 유발 분석", heading_style))
        story.append(Paragraph(
            f"⚠️ {context_analysis.get('overall_risk_description', '')}",
            warning_style
        ))
        confidence = context_analysis.get("confidence", 0)
        if confidence < 0.7:
            story.append(Paragraph(
                f"※ AI 신뢰도: {int(confidence * 100)}% — 담당자 직접 확인 필요",
                warning_style
            ))

    # =====================================================
    # 7. 담당자 확인 요청
    # =====================================================
    needs_review_items = [
        r for r in checklist_results if r.get("confidence", 1) < 0.7
    ]

    if needs_review_items or context_analysis.get("confidence", 1) < 0.7:
        story.append(Paragraph("7. 담당자 확인 요청 항목", heading_style))
        story.append(Paragraph(
            "아래 항목은 AI 판단 신뢰도가 낮아 준법팀 담당자의 직접 확인이 필요합니다.",
            warning_style
        ))
        for item in needs_review_items:
            story.append(Paragraph(
                f"• {item.get('item', '')} (신뢰도: {int(item.get('confidence', 0) * 100)}%)",
                normal_style
            ))

    # =====================================================
    # 푸터
    # =====================================================
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC")))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "※ 본 리포트는 AI 분석 결과이며, 최종 준법 심의 판단은 준법감시팀 담당자가 수행해야 합니다.",
        ParagraphStyle("Footer", fontName=font_name, fontSize=8,
                      textColor=colors.HexColor("#888888"), alignment=TA_CENTER)
    ))

    # PDF 빌드
    doc.build(story)

    return FileResponse(
        tmp_path,
        media_type="application/pdf",
        filename=f"compliot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    )