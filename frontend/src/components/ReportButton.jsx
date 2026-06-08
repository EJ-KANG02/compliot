import { useState } from "react";

export default function ReportButton({ productType, contentType, content, analysisResult }) {
  const [isGenerating, setIsGenerating] = useState(false);

  const downloadReport = async () => {
    setIsGenerating(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/report/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          product_type: productType,
          content_type: contentType,
          content,
          rule_based: analysisResult.rule_based,
          llm_analysis: analysisResult.llm_analysis,
          created_at: new Date().toLocaleString("ko-KR"),
        }),
      });

      if (!res.ok) throw new Error("리포트 생성 실패");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `compliot_report_${new Date().toISOString().slice(0, 10)}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert("리포트 생성 중 오류가 발생했습니다.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <button
      style={styles.btn}
      onClick={downloadReport}
      disabled={isGenerating}
    >
      {isGenerating ? "생성 중..." : "📄 심의 리포트 다운로드"}
    </button>
  );
}

const styles = {
  btn: {
    background: "#2E75B6",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "0.8rem 1.5rem",
    fontSize: "0.9rem",
    fontWeight: "700",
    cursor: "pointer",
    marginTop: "1rem",
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
  },
};