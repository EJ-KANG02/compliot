import os
import re
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
import voyageai
from chromadb import PersistentClient
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

# =====================================================
# 설정
# =====================================================
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
CHROMA_DB_PATH = Path(__file__).parent.parent / "db" / "chroma"
DOCS_PATH = Path(__file__).parent.parent.parent / "docs"
COLLECTION_NAME = "compliot_laws"

voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)


# =====================================================
# 1. PDF 파싱
# =====================================================
def parse_pdf(pdf_path: str) -> str:
    """PDF에서 텍스트 추출"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


# =====================================================
# 2. 청킹
# =====================================================
def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list[str]:
    """텍스트를 청크로 분할"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )
    return splitter.split_text(text)


# =====================================================
# 3. 메타데이터 태깅
# =====================================================
def extract_metadata(chunk: str, source: str) -> dict:
    """청크에서 메타데이터 자동 추출"""
    metadata = {
        "source": source,
        "source_type": _get_source_type(source),
        "article": _extract_article(chunk) or "",
        "product_type": _extract_product_type(chunk),
        "content_type": _extract_content_type(chunk),
        "category": _extract_category(chunk),
    }
    return metadata


def _get_source_type(source: str) -> str:
    if "금소법" in source or "금융소비자" in source:
        return "법령"
    elif "가이드라인" in source:
        return "가이드라인"
    elif "심사지침" in source:
        return "심사지침"
    elif "사내" in source:
        return "사내규정"
    return "기타"


def _extract_article(chunk: str) -> Optional[str]:
    """조문 번호 추출 (예: 제22조)"""
    match = re.search(r'제\d+조(?:의\d+)?(?:\s*제\d+항)?', chunk)
    return match.group() if match else None


def _extract_product_type(chunk: str) -> str:
    """상품 유형 추출"""
    if "예금성" in chunk or "예금" in chunk:
        return "예금성"
    elif "대출성" in chunk or "대출" in chunk:
        return "대출성"
    elif "투자성" in chunk or "투자" in chunk or "펀드" in chunk:
        return "투자성"
    elif "보장성" in chunk or "보험" in chunk:
        return "보장성"
    return "공통"


def _extract_content_type(chunk: str) -> str:
    """콘텐츠 유형 추출"""
    if "SNS" in chunk or "소셜" in chunk or "유튜브" in chunk or "블로그" in chunk:
        return "SNS"
    elif "문자" in chunk or "SMS" in chunk:
        return "문자"
    elif "이메일" in chunk or "전자우편" in chunk:
        return "이메일"
    elif "배너" in chunk:
        return "배너"
    return "공통"


def _extract_category(chunk: str) -> str:
    """카테고리 추출"""
    if any(kw in chunk for kw in ["금지", "허위", "과장", "오인", "부당"]):
        return "금지표현"
    elif any(kw in chunk for kw in ["포함", "기재", "명시", "표시", "고지"]):
        return "필수기재사항"
    elif any(kw in chunk for kw in ["형식", "크기", "글자", "색상"]):
        return "형식요건"
    elif any(kw in chunk for kw in ["채널", "매체", "플랫폼"]):
        return "채널공시"
    return "일반"


# =====================================================
# 4. Voyage AI 임베딩
# =====================================================
def embed_texts(texts: list[str]) -> list[list[float]]:
    """Voyage AI로 텍스트 임베딩"""
    result = voyage_client.embed(
        texts,
        model="voyage-3.5",
        input_type="document",
    )
    return result.embeddings


def embed_query(query: str) -> list[float]:
    """쿼리 임베딩"""
    result = voyage_client.embed(
        [query],
        model="voyage-3.5",
        input_type="query",
    )
    return result.embeddings[0]


# =====================================================
# 5. ChromaDB 저장 및 검색
# =====================================================
def get_chroma_client():
    """ChromaDB 클라이언트 반환"""
    return PersistentClient(path=str(CHROMA_DB_PATH))


def store_documents(chunks: list[str], metadatas: list[dict], source_name: str):
    """청크를 ChromaDB에 저장"""
    client = get_chroma_client()

    # 컬렉션 가져오기 또는 생성
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(COLLECTION_NAME)

    # 배치로 임베딩 (Voyage AI 배치 처리)
    batch_size = 128
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]
        batch_ids = [f"{source_name}_{i + j}" for j in range(len(batch_chunks))]

        embeddings = embed_texts(batch_chunks)

        collection.add(
            ids=batch_ids,
            documents=batch_chunks,
            embeddings=embeddings,
            metadatas=batch_metadatas,
        )

    print(f"✅ {source_name}: {len(chunks)}개 청크 저장 완료")


def search_documents(
    query: str,
    product_type: str = None,
    content_type: str = None,
    category: str = None,
    n_results: int = 5,
) -> list[dict]:
    """
    하이브리드 검색 (벡터 + 메타데이터 필터)
    """
    client = get_chroma_client()

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        return []

    # 메타데이터 필터 구성
    where_conditions = []

    if product_type and product_type != "공통":
        where_conditions.append({
            "$or": [
                {"product_type": {"$eq": product_type}},
                {"product_type": {"$eq": "공통"}},
            ]
        })

    if content_type and content_type != "공통":
        where_conditions.append({
            "$or": [
                {"content_type": {"$eq": content_type}},
                {"content_type": {"$eq": "공통"}},
            ]
        })

    if category:
        where_conditions.append({"category": {"$eq": category}})

    where = {"$and": where_conditions} if len(where_conditions) > 1 else (
        where_conditions[0] if where_conditions else None
    )

    # 쿼리 임베딩
    query_embedding = embed_query(query)

    # 검색
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    # 결과 정리
    docs = []
    if results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            docs.append({
                "content": doc,
                "metadata": meta,
                "relevance_score": 1 - dist,  # 거리 → 유사도
            })

    return docs


# =====================================================
# 6. 전체 파이프라인 실행 (초기 세팅용)
# =====================================================
def build_knowledge_base():
    """
    docs/ 폴더의 PDF를 모두 읽어서 ChromaDB에 저장
    최초 1회 실행
    """
    pdf_files = list(DOCS_PATH.glob("*.pdf"))

    if not pdf_files:
        print("❌ docs/ 폴더에 PDF 파일이 없습니다.")
        return

    print(f"📚 {len(pdf_files)}개 PDF 파일 발견")

    for pdf_path in pdf_files:
        print(f"\n처리 중: {pdf_path.name}")

        # 1. PDF 파싱
        text = parse_pdf(str(pdf_path))
        if not text.strip():
            print(f"  ⚠️ 텍스트 추출 실패: {pdf_path.name}")
            continue

        # 2. 청킹
        chunks = chunk_text(text)
        print(f"  📄 {len(chunks)}개 청크 생성")

        # 3. 메타데이터 태깅
        source_name = pdf_path.stem
        metadatas = [extract_metadata(chunk, source_name) for chunk in chunks]

        # 4. 저장
        store_documents(chunks, metadatas, source_name)

    print("\n✅ 지식베이스 구축 완료!")


if __name__ == "__main__":
    build_knowledge_base()