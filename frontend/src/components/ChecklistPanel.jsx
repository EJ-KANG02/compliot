import { useState } from "react";

const CATEGORY_ICONS = {
  "콘텐츠 내용 항목": "📋",
  "콘텐츠 형식 항목": "🎨",
  "금지 표현 항목": "🚫",
  "채널별 공시 항목": "📡",
  "사내 규정 항목": "🏢",
};

const STATUS_CONFIG = {
  "충족": { icon: "✅", color: "#006600", bg: "#F0FFF0", border: "#B7EBB7" },
  "미충족": { icon: "⚠️", color: "#CC0000", bg: "#FFF8F8", border: "#FFD0D0" },
  "해당없음": { icon: "—", color: "#888", bg: "#F8F8F8", border: "#E0E0E0" },
};

export default function ChecklistPanel({
  checklist,
  content,
  productType,
  contentType,
}) {
  const [openCategories, setOpenCategories] = useState({});
  const [showDescription, setShowDescription] = useState({});
  const [categoryResults, setCategoryResults] = useState({});
  const [loadingCategories, setLoadingCategories] = useState({});

  const toggleCategory = (category) => {
    setOpenCategories((prev) => ({
      ...prev,
      [category]: !prev[category],
    }));
  };

  const toggleDescription = (itemId) => {
    setShowDescription((prev) => ({
      ...prev,
      [itemId]: !prev[itemId],
    }));
  };

  const checkCategory = async (category, items) => {
    if (!content.trim()) {
      alert("먼저 콘텐츠를 작성해주세요.");
      return;
    }

    setLoadingCategories((prev) => ({ ...prev, [category]: true }));
    setOpenCategories((prev) => ({ ...prev, [category]: true }));

    try {
      const res = await fetch("http://127.0.0.1:8000/analysis/category", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content,
          product_type: productType,
          content_type: contentType,
          category,
          items: items.map((i) => ({
            id: i.id,
            item: i.item,
            description: i.description,
          })),
        }),
      });
      const data = await res.json();
      setCategoryResults((prev) => ({ ...prev, [category]: data }));
    } catch (e) {
      alert("카테고리 검사 중 오류가 발생했습니다.");
    } finally {
      setLoadingCategories((prev) => ({ ...prev, [category]: false }));
    }
  };

  if (!checklist || !checklist.checklist) return null;

  const categories = checklist.checklist;
  const totalItems = checklist.total_items;
  const checkedCategories = Object.keys(categoryResults).length;
  const totalCategories = Object.keys(categories).length;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>준법 체크리스트</h2>
        <span style={styles.totalBadge}>총 {totalItems}개 항목</span>
      </div>
      <p style={styles.desc}>
        카테고리별 [검사하기]를 눌러 항목을 확인하거나,
        작성 완료 후 [전체 검사하기]를 누르세요.
      </p>

      {/* 진행 상황 */}
      {checkedCategories > 0 && (
        <div style={styles.progressBar}>
          <div style={styles.progressLabel}>
            {checkedCategories} / {totalCategories} 카테고리 검사 완료
          </div>
          <div style={styles.progressTrack}>
            <div style={{
              ...styles.progressFill,
              width: `${(checkedCategories / totalCategories) * 100}%`,
            }} />
          </div>
        </div>
      )}

      {Object.entries(categories).map(([category, items]) => {
        const catResult = categoryResults[category];
        const isLoading = loadingCategories[category];
        const summary = catResult?.category_summary;

        return (
          <div key={category} style={styles.categoryBlock}>

            {/* 카테고리 헤더 행 */}
            <div style={styles.categoryRow}>
              {/* 펼치기 버튼 */}
              <button
                style={styles.categoryToggle}
                onClick={() => toggleCategory(category)}
              >
                <span style={styles.categoryIcon}>
                  {CATEGORY_ICONS[category] || "📌"}
                </span>
                <span style={styles.categoryName}>{category}</span>
                <span style={styles.countBadge}>{items.length}</span>
                {summary && (
                  <span style={styles.categorySummary}>
                    {summary.satisfied > 0 && `✅${summary.satisfied} `}
                    {summary.unsatisfied > 0 && `⚠️${summary.unsatisfied} `}
                    {summary.not_applicable > 0 && `—${summary.not_applicable}`}
                  </span>
                )}
                <span style={styles.arrow}>
                  {openCategories[category] ? "▲" : "▼"}
                </span>
              </button>

              {/* 카테고리 단위 검사하기 버튼 */}
              <button
                style={{
                  ...styles.categoryCheckBtn,
                  opacity: isLoading ? 0.6 : 1,
                  background: catResult ? "#E8F4E8" : "#EBF3FB",
                  color: catResult ? "#006600" : "#1F4E79",
                  border: catResult
                    ? "1px solid #B7EBB7"
                    : "1px solid #B0CDE8",
                }}
                onClick={() => checkCategory(category, items)}
                disabled={isLoading}
              >
                {isLoading ? "검사 중..." : catResult ? "재검사" : "[검사하기]"}
              </button>
            </div>

            {/* 항목 목록 (펼쳐졌을 때) */}
            {openCategories[category] && (
              <div style={styles.itemList}>
                {items.map((item) => {
                  const itemResult = catResult?.items?.find(
                    (r) => r.id === item.id
                  );
                  const config = itemResult
                    ? STATUS_CONFIG[itemResult.status] || STATUS_CONFIG["해당없음"]
                    : null;

                  return (
                    <div
                      key={item.id}
                      style={{
                        ...styles.itemBlock,
                        background: config ? config.bg : "#FAFAFA",
                        border: `1px solid ${config ? config.border : "#F0F0F0"}`,
                      }}
                    >
                      {/* 항목 행 */}
                      <div style={styles.itemRow}>
                        <div style={styles.itemLeft}>
                          <span style={styles.statusIcon}>
                            {config ? config.icon : "☐"}
                          </span>
                          <span style={styles.itemName}>{item.item}</span>
                        </div>
                        <button
                          style={styles.descBtn}
                          onClick={() => toggleDescription(item.id)}
                        >
                          {showDescription[item.id] ? "닫기" : "[설명보기]"}
                        </button>
                      </div>

                      {/* 설명 */}
                      {showDescription[item.id] && (
                        <div style={styles.descBox}>
                          {item.description.split("\n").map((line, i) => (
                            <p key={i} style={styles.descLine}>{line}</p>
                          ))}
                        </div>
                      )}

                      {/* 항목별 결과 (카테고리 검사 후) */}
                      {itemResult && (
                        <div style={styles.resultBox}>
                          <div style={styles.resultHeader}>
                            <span style={{
                              color: config.color,
                              fontWeight: "700",
                              fontSize: "0.83rem",
                            }}>
                              {config.icon} {itemResult.status}
                            </span>
                            <span style={styles.confidence}>
                              신뢰도 {Math.round((itemResult.confidence || 0) * 100)}%
                              {(itemResult.confidence || 0) < 0.7 && (
                                <span style={styles.reviewBadge}>담당자 확인 필요</span>
                              )}
                            </span>
                          </div>
                          <p style={styles.resultReason}>{itemResult.reason}</p>
                          {itemResult.legal_basis && (
                            <p style={styles.legalBasis}>📜 {itemResult.legal_basis}</p>
                          )}
                          {itemResult.suggestion && (
                            <div style={styles.suggestionBox}>
                              <p style={styles.suggestion}>{itemResult.suggestion}</p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

const styles = {
  container: {
    background: "#fff",
    borderRadius: "16px",
    padding: "1.5rem",
    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
    maxHeight: "80vh",
    overflowY: "auto",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "0.5rem",
  },
  title: {
    fontSize: "1.15rem",
    fontWeight: "700",
    color: "#1F4E79",
    margin: 0,
  },
  totalBadge: {
    background: "#EBF3FB",
    color: "#1F4E79",
    padding: "0.2rem 0.75rem",
    borderRadius: "100px",
    fontSize: "0.8rem",
    fontWeight: "600",
  },
  desc: {
    fontSize: "0.82rem",
    color: "#888",
    marginBottom: "1rem",
    lineHeight: "1.5",
  },
  progressBar: {
    marginBottom: "1rem",
  },
  progressLabel: {
    fontSize: "0.8rem",
    color: "#555",
    marginBottom: "0.3rem",
    fontWeight: "600",
  },
  progressTrack: {
    background: "#E8EEF4",
    borderRadius: "100px",
    height: "6px",
    overflow: "hidden",
  },
  progressFill: {
    background: "#1F4E79",
    height: "100%",
    borderRadius: "100px",
    transition: "width 0.3s ease",
  },
  categoryBlock: {
    marginBottom: "0.75rem",
    border: "1px solid #E8EEF4",
    borderRadius: "10px",
    overflow: "hidden",
  },
  categoryRow: {
    display: "flex",
    alignItems: "center",
    background: "#F4F8FC",
    padding: "0.4rem 0.75rem 0.4rem 0",
    gap: "0.5rem",
  },
  categoryToggle: {
    flex: 1,
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    padding: "0.5rem 0.5rem 0.5rem 1rem",
    background: "none",
    border: "none",
    cursor: "pointer",
    textAlign: "left",
  },
  categoryIcon: { fontSize: "1rem" },
  categoryName: {
    fontSize: "0.9rem",
    fontWeight: "600",
    color: "#1F4E79",
  },
  countBadge: {
    background: "#1F4E79",
    color: "#fff",
    padding: "0.1rem 0.5rem",
    borderRadius: "100px",
    fontSize: "0.75rem",
    fontWeight: "600",
  },
  categorySummary: {
    fontSize: "0.78rem",
    color: "#555",
  },
  arrow: {
    fontSize: "0.7rem",
    color: "#888",
    marginLeft: "auto",
  },
  categoryCheckBtn: {
    padding: "0.35rem 0.75rem",
    borderRadius: "6px",
    fontSize: "0.78rem",
    fontWeight: "700",
    cursor: "pointer",
    whiteSpace: "nowrap",
    flexShrink: 0,
    marginRight: "0.25rem",
    transition: "all 0.2s",
  },
  itemList: {
    padding: "0.5rem",
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem",
  },
  itemBlock: {
    borderRadius: "8px",
    padding: "0.75rem",
    transition: "all 0.2s",
  },
  itemRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  },
  itemLeft: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    flex: 1,
  },
  statusIcon: {
    fontSize: "1rem",
    minWidth: "1.2rem",
  },
  itemName: {
    fontSize: "0.875rem",
    color: "#333",
    flex: 1,
    lineHeight: "1.4",
  },
  descBtn: {
    background: "none",
    border: "none",
    color: "#888",
    fontSize: "0.75rem",
    cursor: "pointer",
    whiteSpace: "nowrap",
    padding: "0.2rem 0.3rem",
  },
  descBox: {
    background: "#F8FBFF",
    border: "1px solid #D6E4F0",
    borderRadius: "6px",
    padding: "0.6rem",
    marginTop: "0.5rem",
  },
  descLine: {
    fontSize: "0.8rem",
    color: "#555",
    margin: "0.15rem 0",
    lineHeight: "1.5",
  },
  resultBox: {
    marginTop: "0.6rem",
    paddingTop: "0.6rem",
    borderTop: "1px dashed #D0D0D0",
  },
  resultHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "0.3rem",
  },
  confidence: {
    fontSize: "0.75rem",
    color: "#888",
    display: "flex",
    alignItems: "center",
    gap: "0.4rem",
  },
  reviewBadge: {
    background: "#FFF3CD",
    color: "#856404",
    padding: "0.1rem 0.4rem",
    borderRadius: "100px",
    fontSize: "0.7rem",
    fontWeight: "600",
  },
  resultReason: {
    fontSize: "0.82rem",
    color: "#444",
    lineHeight: "1.5",
    margin: "0.25rem 0",
  },
  legalBasis: {
    fontSize: "0.78rem",
    color: "#2E75B6",
    margin: "0.2rem 0",
  },
  suggestionBox: {
    background: "#FFFBF0",
    border: "1px solid #FFE58F",
    borderRadius: "6px",
    padding: "0.6rem",
    marginTop: "0.4rem",
  },
  suggestion: {
    fontSize: "0.82rem",
    color: "#555",
    lineHeight: "1.5",
    margin: 0,
  },
};