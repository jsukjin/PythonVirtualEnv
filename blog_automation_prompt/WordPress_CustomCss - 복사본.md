/* [1] 포스팅 본문 내 제목(h2, h3, h4) 스타일 - 라인 복구 */
.entry-content h2,
.entry-content h3,
.entry-content h4,
.inside-article .entry-content h2,
.inside-article .entry-content h3,
.inside-article .entry-content h4,
.separate-containers .inside-article h2,
.separate-containers .inside-article h3,
.separate-containers .inside-article h4 {
  position: relative;
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
  opacity: 1 !important;
  font-weight: 800;
  line-height: 1.28;
  margin: 2.2em 0 1em;
  padding: 0 0 0.45em 0;
  /* 핵심 수정: currentColor 대신 명시적인 회색 적용 (글씨 흰색보다 어둡게) */
  border-bottom: 1px solid #555555 !important; 
  letter-spacing: -0.02em;
  text-shadow: none;
  display: block; /* 라인이 가로로 꽉 차게 보장 */
}

/* 왼쪽 라인 제거 유지 */
.entry-content h2::before, h3::before, h4::before {
  content: none !important;
}

/* 사이트 최상단 메인 헤더 밑줄 (필요 시) */
header#masthead, .site-header {
  border-bottom: 1px solid #333333 !important;
}

/* [2] 표(Table) 디자인 */
.entry-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 2em 0;
  border: 1px solid #444 !important; /* 테두리 강화 */
  background-color: #1a1a1a;
}

.entry-content table th {
  background-color: #2c2c2c;
  color: #ffffff;
  padding: 12px;
  border: 1px solid #444 !important;
  font-weight: 700;
}

.entry-content table td {
  padding: 12px;
  border: 1px solid #333 !important;
  color: #ccc;
}

/*=================================*/


/* 30% 더 밝은 민트 요약 콜아웃 */
.entry-content .summary-callout {
  position: relative;
  margin: 1.8em 0 2.2em;
  padding: 18px 20px 18px 22px;
  background: linear-gradient(
    180deg,
    rgba(150, 255, 240, 0.24) 0%,
    rgba(120, 248, 228, 0.16) 100%
  );
  border: 1px solid rgba(170, 255, 245, 0.78);
  border-left: 4px solid #98fff0;
  border-radius: 10px;
  color: #fcfffe !important;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.10),
    0 0 0 1px rgba(152, 255, 240, 0.08),
    0 10px 28px rgba(90, 235, 210, 0.10);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
}

/* 제목 */
.entry-content .summary-callout .summary-callout-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 10px;
  font-size: 0.98rem;
  font-weight: 800;
  line-height: 1.2;
  color: #ffffff !important;
}

/* 아이콘 */
.entry-content .summary-callout .summary-callout-icon {
  width: 18px;
  height: 18px;
  border: 1px solid rgba(190, 255, 247, 0.95);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #ffffff;
  flex: 0 0 18px;
  background: rgba(255,255,255,0.06);
}

/* 일반 텍스트 */
.entry-content .summary-callout p,
.entry-content .summary-callout li {
  color: #fbfffe !important;
  line-height: 1.72;
}

/* 리스트 */
.entry-content .summary-callout .summary-callout-list {
  margin: 0.7em 0 0 1.2em;
  padding: 0;
}

.entry-content .summary-callout .summary-callout-list li {
  margin: 0.35em 0;
}

/* 링크 */
.entry-content .summary-callout .summary-callout-list li a,
.entry-content .summary-callout .summary-callout-list li a:link,
.entry-content .summary-callout .summary-callout-list li a:visited {
  color: #ffffff !important;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* 링크 hover/focus/active */
.entry-content .summary-callout .summary-callout-list li a:hover,
.entry-content .summary-callout .summary-callout-list li a:focus,
.entry-content .summary-callout .summary-callout-list li a:active {
  color: #ffffff !important;
  opacity: 1;
}

/* 모바일 */
@media (max-width: 768px) {
  .entry-content .summary-callout {
    padding: 16px 16px 16px 18px;
    border-radius: 8px;
  }

  .entry-content .summary-callout .summary-callout-title {
    font-size: 0.95rem;
  }

  .entry-content .summary-callout p,
  .entry-content .summary-callout li {
    font-size: 0.94rem;
  }
}