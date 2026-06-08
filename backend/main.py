from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import checklist, analysis, report

app = FastAPI(
    title="Compliot API",
    description="금융 마케터를 위한 AI 준법 자문 Copilot",
    version="0.1.0",
)

# CORS 설정 (React 프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(checklist.router)
app.include_router(analysis.router)
app.include_router(report.router)


@app.get("/")
def root():
    return {
        "service": "Compliot",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}