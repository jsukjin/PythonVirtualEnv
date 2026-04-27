/*Fonts 하얗게*/
/* body 대신 .entry-content 내부로만 한정 */
.entry-content,
.entry-content p,
.entry-content li,
.entry-content td,
.entry-content th,
.entry-content span {
  color: #ffffff !important;
}

h1, h2, h3, h4, h5, h6,
.entry-title,
.entry-content h1,
.entry-content h2,
.entry-content h3 {
  color: #ffffff !important;
}

.entry-meta,
.posted-on,
.byline,
.author {
  color: #cccccc !important;
}

.entry-content a {
  color: #7db8f0 !important;
}

.callout p,
.callout-title {
  color: #ffffff !important;
}

.callout-summary {
  background: #1a1a1a;                  /* 더 검정에 가깝게 */
  border-left: 4px solid #666;
  border-radius: 6px;
  padding: 14px 18px;
  margin: 20px 0;
  color: #e8e8e8;               /* 더 밝은 글씨 */
  font-size: 0.95em;
  line-height: 1.7;
}

/* callout-summary 내 링크 안 strong - 민트 + 굵게 */
.callout-summary a strong {
  color: #2dd4bf !important;
  font-weight: 800;
}

.callout-summary .callout-title {
  color: #ffffff;               /* 제목은 순백색 */
  font-weight: bold;
  display: block;
  margin-bottom: -20px;
}

/*==============================*/
/*==============================*/
/*==============================*/

/*H2,H3 - 글씨 밝게 + 밑에 라인 그리기 */
.entry-content h2,
.entry-content h3 {
  color: #ffffff !important;
  font-weight: 700 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.6);
  padding-bottom: 0.5rem;
  margin-top: 2.5rem !important;
}


/*==============================*/
/*==============================*/
/*==============================*/

.callout {
  background: #020d1f !important;
  border: 1px solid #1e40af !important;
  border-left: 3px solid #3b82f6 !important;
  border-radius: 8px !important;
  padding: 1rem 1.25rem;
  margin: 1rem 0;
}
.callout-title {
  font-size: 18px !important;
  font-weight: 700;
  text-transform: none !important;
  letter-spacing: 0 !important;
  margin-bottom: 10px;
  color: #ffffff !important;
}

/*링크 컬러*/
.callout a {
  color: #2dd4bf !important;
  text-decoration: underline;
}

.callout p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #e0f0ff !important;
}

/*==============================*/
/*==============================*/
/*==============================*/

/*링크 - 색깔 민트 */
.entry-content a {
  color: #2dd4bf !important;
}


/*==============================*/
/*==============================*/
/*==============================*/

/* table */
.entry-content table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.entry-content table thead tr {
  background: #1a1a1a;
}

.entry-content table th {
  border: 1px solid #444444;
  padding: 10px 14px;
  color: #ffffff;
  font-weight: 700;
  text-align: left;
}

.entry-content table td {
  border: 1px solid #444444;
  padding: 10px 14px;
  color: #dddddd;
}

.entry-content table tbody tr:nth-child(odd) {
  background: #111111;
}

.entry-content table tbody tr:nth-child(even) {
  background: #1e1e1e;
}

/*==============================*/
/*==============================*/
/*==============================*/

/*fotter - color (mint)*/
.entry-footer,
.entry-footer a,
.entry-footer span,
.cat-links,
.cat-links a,
.tags-links,
.tags-links a,
.post-navigation a,
.nav-links a {
  color: #2dd4bf !important;
}

/*==============================*/
/*==============================*/
/*==============================*/

/* 댓글 섹션 */
#comments,
.comment-respond {
  color: #ffffff !important;
}

#comments h2,
.comment-reply-title {
  color: #ffffff !important;
  font-weight: 700;
}

.comment-notes,
.logged-in-as {
  color: #cccccc !important;
}

.logged-in-as a {
  color: #2dd4bf !important;
}

/* 댓글 입력창 */
#comment {
  background: #0d1117 !important;
  border: 1px solid #333333 !important;
  color: #ffffff !important;
  border-radius: 6px;
}

/* 댓글 달기 버튼 */
#submit {
  background: #0a1f3d !important;
  color: #2dd4bf !important;
  border: 1px solid #2dd4bf !important;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
}

#submit:hover {
  background: #2dd4bf !important;
  color: #000000 !important;
}

/* 푸터 */
.site-footer,
.site-info,
.site-info a {
  color: #888888 !important;
}


/*==============================*/
/*==============================*/
/*==============================*/
/*사이드바 위젯 (배경 변경)*/

.widget {
  background: #0d1117 !important;
  border-radius: 8px;
  padding: 1.2rem 1.4rem !important;
  margin-bottom: 1.5rem;
}

.widget-title {
  color: #ffffff !important;
  font-weight: 700;
  margin-bottom: 0.8rem;
}

.widget a {
  color: #2dd4bf !important;
}

/*==============================*/
/*==============================*/
/*==============================*/
/*code snippet */
pre {
  background: #2b2b2b !important;
  border-radius: 8px;
  padding: 16px 20px;
  overflow-x: auto;
}

pre code {
  color: #cdd6f4 !important;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.9em;
  line-height: 1.6;
}

/*==============================*/
/*==============================*/
/*==============================*/
/* li highlight */
.highlight-list {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 14px 18px 14px 40px;
  margin: 20px 0;
  list-style: disc;
  color: #ccc;
  line-height: 1.7;
}

/* highlight-list 항목 간격 축소 */
.highlight-list li {
  margin-bottom: 2px !important;
}

.highlight-list li p {
  margin-bottom: 0 !important;
  line-height: 1.6;
}


/*bold*/
strong {
  color: #ffffff;
  font-weight: 700;
}

/*margin bottom*/
.entry-content p {
  line-height: 1.9;
  margin-bottom: 1.6em;
}


/* callout 내부 리스트 간격 축소 */
.callout ul li p {
  margin-bottom: 0.2em !important;
  line-height: 1.5;
}

.callout ul li {
  margin-bottom: 2px !important;
}

/* callout 내부 리스트 점 제거 */
.callout ul {
  list-style: none !important;
  padding-left: 0 !important;
  margin: 0 !important;
}

/*==============================*/
/*==============================*/
/*==============================*/

.kurtnote-related-posts {
  background-color: #0e6655 !important;
  border-left: 5px solid #0a4f42 !important;
  border-radius: 8px !important;
  padding: 20px 24px !important;
  margin: 32px 0 !important;
}

.kurtnote-related-posts h3 {
  color: #ffffff !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  margin-bottom: 12px !important;
}

.kurtnote-related-posts ul a {
  color: #ffffff !important;
  text-decoration: none !important;
}

.kurtnote-related-posts ul a:hover {
  color: #a2d9ce !important;
  text-decoration: underline !important;
}

.kurtnote-related-posts ul li {
  color: #ffffff !important;
}

/*==========================*/
/*테이블에 bold/하이퍼링크 색깔 표시 (민트)*/
/*==========================*/

/* 테이블 내 링크 + strong 조합 - 민트 + 굵게 */
.entry-content table a strong {
  color: #2dd4bf !important;
  font-weight: 800;
}

/* 테이블 내 일반 링크도 민트로 */
.entry-content table a {
  color: #2dd4bf !important;
  text-decoration: underline;
}


/*==========================*/
/*highlight-list에 bold/하이퍼링크 색깔 표시 (민트)*/
/*==========================*/
/* highlight-list 내 링크 + strong 조합 - 민트 + 굵게 */
.highlight-list a strong {
  color: #2dd4bf !important;
  font-weight: 800;
}

/* highlight-list 내 일반 링크도 민트로 */
.highlight-list a {
  color: #2dd4bf !important;
  text-decoration: underline;
}


/*==========================*/
/*===== 본문 링크도 link 민트표시*/
/*==========================*/

/* 본문 일반 링크 + strong 조합 - 민트 + 굵게 */
.entry-content a strong {
  color: #2dd4bf !important;
  font-weight: 800;
}

/* 본문 일반 링크 - 민트 */
.entry-content a {
  color: #2dd4bf !important;
}