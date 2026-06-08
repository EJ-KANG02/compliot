const STATUS_CONFIG = {
  "충족": { icon: "✅", color: "#006600", bg: "#F0FFF0", border: "#B7EBB7" },
  "미충족": { icon: "⚠️", color: "#CC0000", bg: "#FFF8F8", border: "#FFD0D0" },
  "해당없음": { icon: "—", color: "#888", bg: "#F8F8F8", border: "#E0E0E0" },
};

export default function AnalysisResult({ result }) {
  const ruleResult = result?.rule_based || {};
  const llmResult = result?.llm_analysis || {};
  const checklistResults = llmResult?.checklist_results || [];
  const summary = llmResult?.summary || {};
  const contextAnalysis = llmResult?.context_analysis || {};
  const forbiddenKeywords = ruleResult?.forbidden_keywords || [];

  const unsatisfiedItems = checklistResults.filter(
    (r) => r.status === "미충족"
  );
  const satisfiedItems = checklistResults.filter(
    (r) => r.status === "충족"
  );
  const notApplicableItems = checklistResults.filter(
    (r) => r.status === "해당없음"
  );

  return (
    <div style={styles.container}>

      {/* 요약 카드 */}
      <div style={styles.summaryGrid}>
        <div style={{ ...styles.summaryCard, borderTop: "3px solid #006600" }}>
          <div style={styles.summaryNum}>{summary.satisfied || 0}</div>
          <div style={styles.summaryLabel}>✅ 충족</div>
        </div>
        <div style={{ ...styles.summaryCard, borderTop: "3px solid #CC0000" }}>
          <div style={styles.summaryNum}>{summary.unsatisfied || 0}</div>
          <div style={styles.summaryLabel}>⚠️ 미충족</div>
        </div>
        <div style={{ ...styles.summaryCard, borderTop: "3px solid #888" }}>
          <div style={styles.summaryNum}>{summary.not_applicable || 0}</div>
          <div style={styles.summaryLabel}>— 해당없음</div>
        </div>
        <div style={{ ...styles.summaryCard, borderTop: "3px solid #1F4E79" }}>
          <div style={styles.summaryNum}>{summary.total_items || 0}</div>
          <div style={styles.summaryLabel}>전체 항목</div>
        </div>
      </div>

      {/* Rule-based 금지표현 */}
      {forbiddenKeywords.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>🚫 감지된 금지 표현</h3>
          {forbiddenKeywords.map((kw, i) => (
            <div key={i} style={styles.forbiddenItem}>
              <div style={styles.forbiddenHeader}>
                <span style={styles.severityBadge}>{kw.severity}</span>
                <span style={styles.keyword}>"{kw.keyword}"</span>
                <span style={styles.reason}>{kw.reason}</span>
              </div>
              <p style={styles.suggestion}>💡 {kw.suggestion}</p>
            </div>
          ))}
        </div>
      )}

      {/* 미충족 항목 */}
      {unsatisfiedItems.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>⚠️ 미충족 항목</h3>
          {unsatisfiedItems.map((item, i) => (
            <div key={i} style={styles.resultItem}>
              <div style={styles.itemHeader}>
                <span style={styles.itemName}>{item.item}</span>
                <div style={styles.itemMeta}>
                  {item.legal_basis && (
                    <span style={styles.legalBasis}>📜 {item.legal_basis}</span>
                  )}
                  <span style={styles.confidence}>
                    신뢰도 {Math.round((item.confidence || 0) * 100)}%
                    {(item.confidence || 0) < 0.7 && (
                      <span style={styles.reviewBadge}>담당자 확인 필요</span>
                    )}
                  </span>
                </div>
              </div>
              <p style={styles.reason}>{item.reason}</p>
              {item.suggestion && (
                <div style={styles.suggestionBox}>
                  <p style={styles.suggestion}>{item.suggestion}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* 충족 항목 */}
      {satisfiedItems.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>✅ 충족 항목</h3>
          <div style={styles.satisfiedList}>
            {satisfiedItems.map((item, i) => (
              <div key={i} style={styles.satisfiedItem}>
                <span style={styles.satisfiedIcon}>✅</span>
                <span style={styles.satisfiedName}>{item.item}</span>
                {item.legal_basis && (
                  <span style={styles.legalBasisSmall}>📜 {item.legal_basis}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 해당없음 항목 */}
      {notApplicableItems.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>— 해당없음 항목</h3>
          <div style={styles.satisfiedList}>
            {notApplicableItems.map((item, i) => (
              <div key={i} style={styles.satisfiedItem}>
                <span style={{ color: "#888" }}>—</span>
                <span style={{ ...styles.satisfiedName, color: "#888" }}>{item.item}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 전체 맥락 오인 유발 분석 */}
      {contextAnalysis.has_overall_risk && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>⚠️ 전체 맥락 오인 유발 분석</h3>
          <div style={styles.contextBox}>
            <p style={styles.reason}>{contextAnalysis.overall_risk_description}</p>
            {(contextAnalysis.confidence || 0) < 0.7 && (
              <span style={styles.reviewBadge}>담당자 확인 필요</span>
            )}
          </div>
        </div>
      )}

      {/* 최종 안내 */}
      <div style={styles.disclaimer}>
        ※ 본 결과는 AI 분석 결과이며, 최종 준법 심의 판단은 준법감시팀 담당자가 수행해야 합니다.
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    gap: "1.25rem",
  },
  summaryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "1rem",
  },
  summaryCard: {
    background: "#fff",
    borderRadius: "12px",
    padding: "1.25rem",
    textAlign: "center",
    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
  },
  summaryNum: {
    fontSize: "2rem",
    fontWeight: "800",
    color: "#1F4E79",
  },
  summaryLabel: {
    fontSize: "0.85rem",
    color: "#666",
    marginTop: "0.25rem",
  },
  section: {
    background: "#fff",
    borderRadius: "16px",
    padding: "1.5rem",
    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
  },
  sectionTitle: {
    fontSize: "1rem",
    fontWeight: "700",
    color: "#1F4E79",
    marginBottom: "1rem",
    margin: "0 0 1rem 0",
  },
  forbiddenItem: {
    background: "#FFF8F8",
    border: "1px solid #FFD0D0",
    borderRadius: "10px",
    padding: "0.875rem 1rem",
    marginBottom: "0.75rem",
  },
  forbiddenHeader: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    marginBottom: "0.4rem",
    flexWrap: "wrap",
  },
  severityBadge: {
    background: "#CC0000",
    color: "#fff",
    padding: "0.15rem 0.6rem",
    borderRadius: "100px",
    fontSize: "0.75rem",
    fontWeight: "700",
    flexShrink: 0,
  },
  keyword: {
    fontWeight: "700",
    color: "#CC0000",
    fontSize: "0.9rem",
  },
  resultItem: {
    background: "#FFF8F8",
    border: "1px solid #FFD0D0",
    borderRadius: "10px",
    padding: "0.875rem 1rem",
    marginBottom: "0.75rem",
  },
  itemHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "0.4rem",
    gap: "0.5rem",
    flexWrap: "wrap",
  },
  itemName: {
    fontSize: "0.95rem",
    fontWeight: "700",
    color: "#CC0000",
  },
  itemMeta: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    flexWrap: "wrap",
  },
  legalBasis: {
    fontSize: "0.78rem",
    color: "#2E75B6",
  },
  legalBasisSmall: {
    fontSize: "0.75rem",
    color: "#2E75B6",
    marginLeft: "auto",
  },
  confidence: {
    fontSize: "0.78rem",
    color: "#888",
    display: "flex",
    alignItems: "center",
    gap: "0.4rem",
  },
  reviewBadge: {
    background: "#FFF3CD",
    color: "#856404",
    padding: "0.1rem 0.5rem",
    borderRadius: "100px",
    fontSize: "0.72rem",
    fontWeight: "600",
  },
  reason: {
    fontSize: "0.875rem",
    color: "#444",
    lineHeight: "1.5",
    margin: "0.25rem 0",
  },
  suggestionBox: {
    background: "#FFFBF0",
    border: "1px solid #FFE58F",
    borderRadius: "8px",
    padding: "0.6rem 0.875rem",
    marginTop: "0.5rem",
  },
  suggestion: {
    fontSize: "0.875rem",
    color: "#555",
    lineHeight: "1.5",
    margin: 0,
  },
  satisfiedList: {
    display: "flex",
    flexDirection: "column",
    gap: "0.4rem",
  },
  satisfiedItem: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    padding: "0.4rem 0.5rem",
    borderRadius: "6px",
    background: "#F8F8F8",
  },
  satisfiedIcon: {
    fontSize: "0.9rem",
    flexShrink: 0,
  },
  satisfiedName: {
    fontSize: "0.875rem",
    color: "#333",
    flex: 1,
  },
  contextBox: {
    background: "#FFF8F8",
    border: "1px solid #FFD0D0",
    borderRadius: "10px",
    padding: "1rem",
  },
  disclaimer: {
    fontSize: "0.8rem",
    color: "#888",
    textAlign: "center",
    padding: "1rem",
    background: "#fff",
    borderRadius: "10px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.04)",
  },
};