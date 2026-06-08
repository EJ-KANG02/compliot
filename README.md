# ⚖️ Compliot
> **금융 마케터를 위한 AI 준법 자문 Copilot**
> JB금융그룹 Fin:AI Challenge — 지정주제 2 (Compliance AI)

---

## 📌 서비스 소개

Compliot은 금융 콘텐츠 작성 단계에서 AI가 준법 리스크를 점검하고, 준법팀 전달용 심의 리포트를 자동 생성하는 서비스입니다.

```
마케터가 콘텐츠 작성
    ↓
상품·콘텐츠 유형별 맞춤 체크리스트 제공
    ↓
카테고리별 AI 준법 검사 (Rule-based → RAG → LLM)
    ↓
심의 리포트 PDF 생성 → 준법팀 전달
```

---

## 🛠 기술 스택

| 구분 | 기술 |
|---|---|
| 프론트엔드 | React + Vite + Tailwind CSS |
| 백엔드 | FastAPI |
| RAG 프레임워크 | LangChain |
| 벡터 DB | ChromaDB |
| 임베딩 | Voyage AI (voyage-3.5) |
| LLM | Claude API (claude-sonnet-4-5) |
| Rule Engine | Python 딕셔너리 + 정규식 |
| 법령 추적 | 법제처 오픈API + APScheduler |
| PDF 생성 | ReportLab |

---

## ⚙️ 설치 및 실행

### 1. 레포지토리 클론

```bash
git clone https://github.com/EJ-KANG02/compliot.git
cd compliot
```

### 2. 환경변수 설정

루트 폴더에 `.env` 파일 생성:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
VOYAGE_API_KEY=your_voyage_api_key
```

- Anthropic API 키 발급: https://console.anthropic.com
- Voyage AI API 키 발급: https://dash.voyageai.com

### 3. 백엔드 설치 및 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# RAG 지식베이스 구축 (최초 1회 실행)
# docs/ 폴더에 법령 PDF 파일이 있어야 합니다
python backend/services/rag.py

# 백엔드 서버 실행
uvicorn backend.main:app --reload
```

백엔드 서버: http://127.0.0.1:8000
API 문서: http://127.0.0.1:8000/docs

### 4. 프론트엔드 설치 및 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드: http://localhost:5173

---

## 📁 프로젝트 구조

```
compliot/
├── backend/
│   ├── main.py                  # FastAPI 서버 진입점
│   ├── routers/
│   │   ├── checklist.py         # 체크리스트 제공 API
│   │   ├── analysis.py          # 준법 검사 API
│   │   └── report.py            # 심의 리포트 PDF 생성 API
│   ├── services/
│   │   ├── rag.py               # RAG 파이프라인
│   │   └── llm.py               # Claude API 연동
│   └── data/
│       ├── checklist_dict.py    # 체크리스트 딕셔너리
│       └── forbidden_words.py   # 금지 표현 딕셔너리
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── MainPage.jsx     # 메인 페이지
│       └── components/
│           ├── ChecklistPanel.jsx   # 체크리스트 패널
│           ├── AnalysisResult.jsx   # 분석 결과 컴포넌트
│           └── ReportButton.jsx     # 리포트 다운로드 버튼
├── docs/                        # 법령 PDF 문서 (RAG 지식베이스)
├── requirements.txt
└── .env                         # 환경변수 (직접 생성 필요)
```

---

## 📋 주요 기능

### 1. 콘텐츠 설정 및 체크리스트 제공
- 상품 유형 (예금성/대출성/투자성/보장성) + 콘텐츠 유형 (SNS/배너/문자/이메일/상품소개) 선택
- 금소법 22조, 금융위 광고규제 가이드라인 기반 맞춤 체크리스트 자동 제공
- 5가지 분류: 콘텐츠 내용 / 콘텐츠 형식 / 금지 표현 / 채널별 공시 / 사내 규정

### 2. 카테고리별 준법 검사
- 카테고리 단위 [검사하기] 클릭 → LLM 1회 호출로 카테고리 내 항목 한 번에 분석
- Rule-based 1차 필터 → RAG 검색 → LLM 판단 3단계 파이프라인
- 항목별 충족/미충족/해당없음 + 근거 조항 + 수정 제안 제공

### 3. 전체 준법 검사
- 전체 항목 일괄 분석 + 전체 맥락 오인 유발 여부 분석
- 신뢰도 낮은 항목 "담당자 확인 필요" 표시

### 4. 심의 리포트 PDF 다운로드
- 준법팀 전달용 구조화된 리포트 자동 생성
- 항목별 충족 여부 / 근거 조항 / 수정 제안 / 담당자 확인 요청 항목 포함

---

## 🔒 보안 참고사항

- `.env` 파일은 절대 커밋하지 마세요 (`.gitignore`에 포함됨)
- `backend/db/` (ChromaDB 데이터) 는 로컬에서만 유지됩니다
- 실제 금융사 도입 시 Voyage AI / Claude API 온프레미스 배포 전환 권장

---

## 📜 활용 법령 데이터

| 데이터 | 출처 |
|---|---|
| 금융소비자보호법 제22조 | 법제처 국가법령정보 오픈API |
| 금융위원회 금융광고규제 가이드라인 | 금융위원회 |
| 금융상품 표시·광고에 관한 심사지침 | 공정거래위원회 |

---

> ※ Compliot은 AI 분석 결과를 제공하며, 최종 준법 심의 판단은 준법감시팀 담당자가 수행해야 합니다.