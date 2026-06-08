import { useState } from "react";
import ChecklistPanel from "../components/ChecklistPanel";
import AnalysisResult from "../components/AnalysisResult";
import ReportButton from "../components/ReportButton";

const PRODUCT_TYPES = ["예금성", "대출성", "투자성", "보장성"];
const CONTENT_TYPES = ["SNS", "배너", "문자", "이메일", "상품소개"];

export default function MainPage() {
  const [productType, setProductType] = useState("");
  const [contentType, setContentType] = useState("");
  const [content, setContent] = useState("");
  const [checklist, setChecklist] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [step, setStep] = useState(1); // 1: 설정, 2: 작성, 3: 결과

  const fetchChecklist = async () => {
    if (!productType || !contentType) return;
    try {
      const res = await fetch("http://127.0.0.1:8000/checklist/get", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_type: productType, content_type: contentType }),
      });
      const data = await res.json();
      setChecklist(data);
      setStep(2);
    } catch (e) {
      alert("체크리스트를 불러오는 데 실패했습니다.");
    }
  };

  const runAnalysis = async () => {
    if (!content.trim()) {
      alert("콘텐츠를 입력해주세요.");
      return;
    }
    setIsAnalyzing(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/analysis/full", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content,
          product_type: productType,
          content_type: contentType,
        }),
      });
      const data = await res.json();
      setAnalysisResult(data);
      setStep(3);
    } catch (e) {
      alert("분석 중 오류가 발생했습니다.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const reset = () => {
    setProductType("");
    setContentType("");
    setContent("");
    setChecklist(null);
    setAnalysisResult(null);
    setStep(1);
  };

  return (
    <div style={styles.container}>
      {/* 헤더 */}
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>⚖️</span>
            <span style={styles.logoText}>Compliot</span>
          </div>
          <span style={styles.logoSub}>AI 준법 자문 Copilot</span>
        </div>
      </header>

      <main style={styles.main}>
        {/* Step 인디케이터 */}
        <div style={styles.stepBar}>
          {["콘텐츠 설정", "작성", "검사 결과"].map((label, i) => (
            <div key={i} style={styles.stepItem}>
              <div style={{
                ...styles.stepCircle,
                background: step > i + 1 ? "#2E75B6" : step === i + 1 ? "#1F4E79" : "#E0E0E0",
                color: step >= i + 1 ? "#fff" : "#999",
              }}>
                {step > i + 1 ? "✓" : i + 1}
              </div>
              <span style={{
                ...styles.stepLabel,
                color: step >= i + 1 ? "#1F4E79" : "#999",
                fontWeight: step === i + 1 ? "700" : "400",
              }}>{label}</span>
              {i < 2 && <div style={{
                ...styles.stepLine,
                background: step > i + 1 ? "#2E75B6" : "#E0E0E0",
              }} />}
            </div>
          ))}
        </div>

        {/* Step 1: 콘텐츠 설정 */}
        {step === 1 && (
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>콘텐츠 설정</h2>
            <p style={styles.cardDesc}>심의할 콘텐츠의 상품 유형과 채널을 선택하세요.</p>

            <div style={styles.selectGroup}>
              <label style={styles.label}>상품 유형</label>
              <div style={styles.chipGroup}>
                {PRODUCT_TYPES.map((type) => (
                  <button
                    key={type}
                    style={{
                      ...styles.chip,
                      ...(productType === type ? styles.chipActive : {}),
                    }}
                    onClick={() => setProductType(type)}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>

            <div style={styles.selectGroup}>
              <label style={styles.label}>콘텐츠 유형</label>
              <div style={styles.chipGroup}>
                {CONTENT_TYPES.map((type) => (
                  <button
                    key={type}
                    style={{
                      ...styles.chip,
                      ...(contentType === type ? styles.chipActive : {}),
                    }}
                    onClick={() => setContentType(type)}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>

            <button
              style={{
                ...styles.primaryBtn,
                opacity: productType && contentType ? 1 : 0.5,
                cursor: productType && contentType ? "pointer" : "not-allowed",
              }}
              onClick={fetchChecklist}
              disabled={!productType || !contentType}
            >
              체크리스트 불러오기 →
            </button>
          </div>
        )}

        {/* Step 2: 체크리스트 + 작성 */}
        {step === 2 && checklist && (
          <div style={styles.twoCol}>
            {/* 왼쪽: 체크리스트 */}
            <div style={styles.leftPanel}>
            <ChecklistPanel
                checklist={checklist}
                content={content}
                productType={productType}
                contentType={contentType}
            />
            </div>

            {/* 오른쪽: 콘텐츠 작성 */}
            <div style={styles.rightPanel}>
              <div style={styles.card}>
                <h2 style={styles.cardTitle}>콘텐츠 작성</h2>
                <p style={styles.cardDesc}>
                  왼쪽 체크리스트를 참고하며 콘텐츠를 작성하세요.
                </p>
                <div style={styles.metaInfo}>
                  <span style={styles.badge}>{productType}</span>
                  <span style={styles.badge}>{contentType}</span>
                </div>
                <textarea
                  style={styles.textarea}
                  placeholder={`[${contentType}] ${productType} 상품 광고 콘텐츠를 작성하세요...`}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows={10}
                />
                <div style={styles.charCount}>{content.length}자</div>
                <div style={styles.btnRow}>
                  <button style={styles.secondaryBtn} onClick={reset}>
                    ← 처음으로
                  </button>
                  <button
                    style={{
                      ...styles.primaryBtn,
                      opacity: content.trim() ? 1 : 0.5,
                      cursor: content.trim() ? "pointer" : "not-allowed",
                    }}
                    onClick={runAnalysis}
                    disabled={!content.trim() || isAnalyzing}
                  >
                    {isAnalyzing ? "분석 중..." : "검사하기 →"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: 분석 결과 */}
        {step === 3 && analysisResult && (
          <div style={styles.resultContainer}>
            <div style={styles.resultHeader}>
              <div>
                <h2 style={styles.cardTitle}>준법 심의 결과</h2>
                <div style={styles.metaInfo}>
                  <span style={styles.badge}>{productType}</span>
                  <span style={styles.badge}>{contentType}</span>
                </div>
              </div>
              <div style={styles.btnRow}>
                <button style={styles.secondaryBtn} onClick={() => setStep(2)}>
                  ← 다시 작성
                </button>
                <ReportButton
                  productType={productType}
                  contentType={contentType}
                  content={content}
                  analysisResult={analysisResult}
                />
              </div>
            </div>
            <AnalysisResult
              result={analysisResult}
              content={content}
              productType={productType}
              contentType={contentType}
            />
          </div>
        )}
      </main>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "#F4F6FA",
    fontFamily: "'Pretendard', 'Apple SD Gothic Neo', sans-serif",
  },
  header: {
    background: "#1F4E79",
    padding: "0 2rem",
    height: "64px",
    display: "flex",
    alignItems: "center",
    boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
  },
  headerInner: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    width: "100%",
    maxWidth: "1200px",
    margin: "0 auto",
  },
  logo: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
  },
  logoIcon: { fontSize: "1.5rem" },
  logoText: {
    fontSize: "1.4rem",
    fontWeight: "800",
    color: "#fff",
    letterSpacing: "-0.5px",
  },
  logoSub: {
    fontSize: "0.85rem",
    color: "rgba(255,255,255,0.6)",
    marginLeft: "0.5rem",
  },
  main: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "2rem",
  },
  stepBar: {
    display: "flex",
    alignItems: "center",
    marginBottom: "2rem",
    background: "#fff",
    borderRadius: "12px",
    padding: "1.25rem 2rem",
    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
  },
  stepItem: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
  },
  stepCircle: {
    width: "32px",
    height: "32px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "0.85rem",
    fontWeight: "700",
    transition: "all 0.3s",
  },
  stepLabel: {
    fontSize: "0.9rem",
    transition: "all 0.3s",
  },
  stepLine: {
    width: "60px",
    height: "2px",
    margin: "0 0.75rem",
    transition: "all 0.3s",
  },
  card: {
    background: "#fff",
    borderRadius: "16px",
    padding: "2rem",
    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
  },
  cardTitle: {
    fontSize: "1.25rem",
    fontWeight: "700",
    color: "#1F4E79",
    marginBottom: "0.5rem",
  },
  cardDesc: {
    fontSize: "0.9rem",
    color: "#666",
    marginBottom: "1.5rem",
  },
  selectGroup: {
    marginBottom: "1.5rem",
  },
  label: {
    display: "block",
    fontSize: "0.85rem",
    fontWeight: "600",
    color: "#444",
    marginBottom: "0.75rem",
  },
  chipGroup: {
    display: "flex",
    gap: "0.5rem",
    flexWrap: "wrap",
  },
  chip: {
    padding: "0.5rem 1.25rem",
    borderRadius: "100px",
    border: "1.5px solid #D0D0D0",
    background: "#fff",
    color: "#555",
    fontSize: "0.9rem",
    cursor: "pointer",
    transition: "all 0.2s",
    fontWeight: "500",
  },
  chipActive: {
    border: "1.5px solid #1F4E79",
    background: "#1F4E79",
    color: "#fff",
  },
  primaryBtn: {
    background: "#1F4E79",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "0.8rem 2rem",
    fontSize: "0.95rem",
    fontWeight: "700",
    cursor: "pointer",
    transition: "all 0.2s",
    marginTop: "1rem",
  },
  secondaryBtn: {
    background: "#fff",
    color: "#1F4E79",
    border: "1.5px solid #1F4E79",
    borderRadius: "10px",
    padding: "0.8rem 1.5rem",
    fontSize: "0.9rem",
    fontWeight: "600",
    cursor: "pointer",
    marginTop: "1rem",
  },
  twoCol: {
    display: "grid",
    gridTemplateColumns: "1fr 1.3fr",
    gap: "1.5rem",
    alignItems: "start",
  },
  leftPanel: {},
  rightPanel: {},
  textarea: {
    width: "100%",
    padding: "1rem",
    border: "1.5px solid #E0E0E0",
    borderRadius: "10px",
    fontSize: "0.95rem",
    lineHeight: "1.6",
    resize: "vertical",
    outline: "none",
    fontFamily: "inherit",
    color: "#333",
    boxSizing: "border-box",
  },
  charCount: {
    textAlign: "right",
    fontSize: "0.8rem",
    color: "#999",
    marginTop: "0.25rem",
  },
  btnRow: {
    display: "flex",
    gap: "0.75rem",
    alignItems: "center",
  },
  metaInfo: {
    display: "flex",
    gap: "0.5rem",
    marginBottom: "1rem",
  },
  badge: {
    background: "#EBF3FB",
    color: "#1F4E79",
    padding: "0.25rem 0.75rem",
    borderRadius: "100px",
    fontSize: "0.8rem",
    fontWeight: "600",
  },
  resultContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem",
  },
  resultHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    background: "#fff",
    borderRadius: "16px",
    padding: "1.5rem 2rem",
    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
  },
};