#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/check.py - SER LLM Wiki 自動化品質門禁腳本
依據 AGENTS.md 第 11 節與使用者修訂規範實作。
唯讀檢查，任何項目失敗結束碼非 0。
支援自訂根目錄 (--root) 與完工檢查標籤 (--final)。
報告同時輸出至終端機並以 UTF-8 寫入 <root>/temp/check-report.txt。
"""

import sys
import os
import re
import argparse
from pathlib import Path
from datetime import datetime

# 確保輸出支援 UTF-8（僅在直接執行時切換，避免被 import 時影響呼叫端）
if sys.platform == "win32" and __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class WikiChecker:
    def __init__(self, root_dir: Path, is_final: bool = False):
        self.root = root_dir.resolve()
        self.is_final = is_final
        self.raw_dir = self.root / "raw"
        self.wiki_dir = self.root / "wiki"
        self.papers_dir = self.wiki_dir / "papers"
        self.entities_dir = self.wiki_dir / "entities"
        self.synthesis_dir = self.wiki_dir / "synthesis"
        self.index_file = self.wiki_dir / "index.md"
        self.log_file = self.wiki_dir / "log.md"
        self.agents_file = self.root / "AGENTS.md"

        self.results = []
        self.has_failure = False

    def log_result(self, item_no: int, name: str, passed: bool, details: list = None, indeterminate: list = None, pending: list = None):
        if details is None:
            details = []
        if indeterminate is None:
            indeterminate = []
        if pending is None:
            pending = []

        status = "PASSED" if passed and not details else "FAILED"
        if not passed:
            self.has_failure = True

        self.results.append({
            "no": item_no,
            "name": name,
            "status": status,
            "passed": passed and not details,
            "fail_count": len(details),
            "details": details,
            "indeterminate": indeterminate,
            "indet_count": len(indeterminate),
            "pending": pending,
            "pending_count": len(pending)
        })

    @staticmethod
    def strip_html_comments(text: str) -> str:
        """移除 <!-- ... -->（含跨行），以等量換行取代，保持原始行號。"""
        return re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.DOTALL)

    def read_md(self, path: Path) -> str:
        """讀取 Markdown 並移除 HTML 註解；所有檢查一律經由此函式讀檔。"""
        text = path.read_text(encoding="utf-8", errors="replace")
        return self.strip_html_comments(text.replace('\r\n', '\n'))

    @staticmethod
    def strip_inline_comment(value: str) -> str:
        """剝除值後面的行尾 # 註解；引號內的 # 不算，# 前須為空白或位於開頭（YAML 規則）。"""
        quote = None
        for i, ch in enumerate(value):
            if quote:
                if ch == quote:
                    quote = None
            elif ch in ('"', "'"):
                quote = ch
            elif ch == "#" and (i == 0 or value[i - 1].isspace()):
                return value[:i].rstrip()
        return value.strip()

    @staticmethod
    def get_section(content: str, heading: str):
        """
        逐行切章節：找到第一個以 heading 開頭的 `## ` 行（其後可接空白或「（英文）」說明），
        章節本文 = 該行之後、到下一個以 `## ` 開頭的行之前。找不到標題回傳 None。
        """
        lines = content.split("\n")
        for i, line in enumerate(lines):
            s = line.rstrip()
            if not s.startswith(heading):
                continue
            rest = s[len(heading):]
            if rest and not (rest[0].isspace() or rest[0] in "（("):
                continue
            body = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                body.append(nxt)
            return "\n".join(body)
        return None

    def parse_frontmatter(self, content: str) -> dict:
        """content 須為已移除 HTML 註解的文字（read_md 的輸出）。"""
        fm = {}
        lines = content.split("\n")
        i = 0
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines) or lines[i].strip() != "---":
            return fm
        for line in lines[i + 1:]:
            if line.strip() == "---":
                break
            s = line.strip()
            if not s or s.startswith("#") or ":" not in s:
                continue
            k, v = s.split(":", 1)
            k = k.strip()
            v = self.strip_inline_comment(v.strip())
            if v.startswith("[") and v.endswith("]"):
                fm[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip().strip("'\"")]
            else:
                fm[k] = v.strip("'\"").strip()
        return fm

    # 1. 雙向連結有效性與孤兒實體頁檢查（排除 index.md）
    def check_links_and_orphans(self):
        broken_links = []
        orphan_entities = []

        all_md_files = {}
        for md in self.wiki_dir.rglob("*.md"):
            all_md_files[md.stem] = md

        # 只納入實體頁
        inbound_links = {md.stem: 0 for md in self.entities_dir.glob("*.md") if md.is_file() and md.name != ".gitkeep"}
        link_pattern = re.compile(r'\[\[([a-zA-Z0-9_\-]+)\]\]')

        # 掃描連結：所有 wiki/*.md（含 index.md、log.md）皆檢查失效連結；
        # 但 index.md 與 log.md 的連結不計入孤兒實體頁的入站連結（孤兒判定只看實質內文）
        for md in sorted(self.wiki_dir.rglob("*.md")):
            if not md.is_file() or md.name == ".gitkeep":
                continue
            counts_as_inbound = md not in (self.index_file, self.log_file)

            content = self.read_md(md)
            for target in link_pattern.findall(content):
                if target not in all_md_files:
                    broken_links.append(f"{md.relative_to(self.root).as_posix()}: 失效連結 [[{target}]] (目標檔案不存在)")
                elif counts_as_inbound and target in inbound_links and md.stem != target:
                    inbound_links[target] += 1

        for entity_stem, count in inbound_links.items():
            if count == 0:
                orphan_entities.append(f"wiki/entities/{entity_stem}.md: 孤兒實體頁 (除 index.md／log.md 外無任何實質頁面連入)")

        details = broken_links + orphan_entities
        self.log_result(1, "雙向連結有效性（含 index.md／log.md）與孤兒實體頁檢查（index.md／log.md 不計入連入）", len(details) == 0, details)

    # 2. 實體與論文清單雙向一致性檢查
    def check_bidirectional_consistency(self):
        inconsistencies = []
        entity_sources = {}
        paper_links = {}

        link_pattern = re.compile(r'\[\[([a-zA-Z0-9_\-]+)\]\]')

        for ent in self.entities_dir.glob("*.md"):
            if not ent.is_file() or ent.name == ".gitkeep":
                continue
            content = self.read_md(ent)
            fm = self.parse_frontmatter(content)
            sources = fm.get("sources", [])
            if isinstance(sources, str):
                sources = [sources] if sources else []
            entity_sources[ent.stem] = sources

        for p in self.papers_dir.glob("*.md"):
            if not p.is_file() or p.name == ".gitkeep":
                continue
            content = self.read_md(p)
            match = re.search(r'## 提及實體清單.*?(?=\n## |\Z)', content, re.DOTALL)
            links = []
            if match:
                links = link_pattern.findall(match.group(0))
            paper_links[p.stem] = links

        for ent_stem, sources in entity_sources.items():
            for src in sources:
                if src in paper_links:
                    if ent_stem not in paper_links[src]:
                        inconsistencies.append(f"實體 wiki/entities/{ent_stem}.md 的 sources 包含 '{src}'，但論文 wiki/papers/{src}.md 的「提及實體清單」未包含 [[{ent_stem}]]")
                else:
                    inconsistencies.append(f"實體 wiki/entities/{ent_stem}.md 的 sources 參照了不存在的論文 '{src}'")

        for paper_stem, links in paper_links.items():
            for ent_link in links:
                if ent_link in entity_sources:
                    if paper_stem not in entity_sources[ent_link]:
                        inconsistencies.append(f"論文 wiki/papers/{paper_stem}.md 提及 [[{ent_link}]]，但該實體 frontmatter 的 sources 遺漏了 '{paper_stem}'")

        self.log_result(2, "實體 sources 與論文清單雙向一致性檢查", len(inconsistencies) == 0, inconsistencies)

    # 3. 欄位名與標題逐字對照及必填檢查
    def check_schema_and_verbatim_headings(self):
        issues = []
        valid_entity_types = {"topic", "taxonomy", "dataset", "feature", "model", "metric"}
        valid_paper_types = {"method", "dataset", "survey", "benchmark"}

        # 規範之精準標題對照表 (AGENTS.md 與 templates)
        required_entity_headings = [
            "## 定義",
            "## 核心屬性與特點",
            "## 在各論文中的應用與實驗表現",
            "## 矛盾／待釐清"
        ]
        always_required_paper_headings = [
            "## 基本資訊",
            "## 研究動機與欲解決問題",
            "## 核心貢獻與作者觀點",
            "## 論文提及之局限性",
            "## 提及實體清單",
            "## 矛盾／待釐清"
        ]

        # 檢查實體頁
        for ent in self.entities_dir.glob("*.md"):
            if not ent.is_file() or ent.name == ".gitkeep":
                continue
            content = self.read_md(ent)
            fm = self.parse_frontmatter(content)

            etype = fm.get("type", "")
            if etype not in valid_entity_types:
                issues.append(f"wiki/entities/{ent.name}: frontmatter type '{etype}' 不合法 (必須是 {valid_entity_types})")

            if not str(fm.get("name", "")).strip():
                issues.append(f"wiki/entities/{ent.name}: frontmatter 'name' 不得為空")

            # 檢查各章節名逐字相同
            for sec in required_entity_headings:
                if sec not in content:
                    issues.append(f"wiki/entities/{ent.name}: 缺少必備逐字標題 '{sec}'")

        # 檢查論文頁
        for p in self.papers_dir.glob("*.md"):
            if not p.is_file() or p.name == ".gitkeep":
                continue
            content = self.read_md(p)
            fm = self.parse_frontmatter(content)

            ptype = fm.get("type", "")
            if ptype not in valid_paper_types:
                issues.append(f"wiki/papers/{p.name}: frontmatter type '{ptype}' 不合法 (必須是 {valid_paper_types})")

            # 檢查逐字欄位名 one_sentence_summary（空字串、只有引號、只有註解皆判失敗）
            if "one_sentence_summary" not in fm:
                issues.append(f"wiki/papers/{p.name}: frontmatter 缺少必填逐字欄位 'one_sentence_summary'")
            elif not str(fm["one_sentence_summary"]).strip().strip("'\"").strip():
                issues.append(f"wiki/papers/{p.name}: frontmatter 必填欄位 'one_sentence_summary' 為空")
            else:
                digits = re.findall(r'[0-9０-９]+', str(fm["one_sentence_summary"]))
                if digits:
                    issues.append(
                        f"wiki/papers/{p.name}: frontmatter 'one_sentence_summary' 不得含阿拉伯數字 "
                        f"(發現 {', '.join(digits)}；摘要會被 index.md 直接引用，無法附 [本文]/[引述] 標籤與頁碼)")

            # frontmatter：title、authors、year、pdf
            if not str(fm.get("title", "")).strip():
                issues.append(f"wiki/papers/{p.name}: frontmatter 'title' 不得為空")
            authors = fm.get("authors", "")
            if (isinstance(authors, list) and len(authors) == 0) or (isinstance(authors, str) and not authors.strip()):
                issues.append(f"wiki/papers/{p.name}: frontmatter 'authors' 不得為空清單")
            year = str(fm.get("year", "")).strip()
            if not re.fullmatch(r'\d{4}', year):
                issues.append(f"wiki/papers/{p.name}: frontmatter 'year' 必須是 4 位數字 (目前為 '{year}')")
            expected_pdf = f"raw/{p.stem}.pdf"
            pdf_val = str(fm.get("pdf", "")).strip()
            if pdf_val != expected_pdf:
                issues.append(f"wiki/papers/{p.name}: frontmatter 'pdf' 必須等於 '{expected_pdf}' (目前為 '{pdf_val}')")

            # 基本資訊：每一條 `- **欄位**：值` 冒號後必須有內容
            basic = self.get_section(content, "## 基本資訊")
            if basic is not None:
                for bline in basic.split("\n"):
                    bm = re.match(r'^\s*[-*]\s+\*\*(.+?)\*\*\s*[：:](.*)$', bline)
                    if bm and not bm.group(2).strip():
                        issues.append(f"wiki/papers/{p.name}: 基本資訊 '{bm.group(1)}' 冒號後不可留空（不知道請寫「論文未提及」）")

            # 檢查正文不該有 ## 一句話摘要 章節
            if "## 一句話摘要" in content:
                issues.append(f"wiki/papers/{p.name}: 正文不應包含 '## 一句話摘要'（必須以 frontmatter 為唯一來源）")

            # 檢查必備逐字標題
            for sec in always_required_paper_headings:
                if sec not in content:
                    issues.append(f"wiki/papers/{p.name}: 缺少必填逐字標題 '{sec}'")

            # 類型特有檢查
            if ptype == "method":
                for sec in ["## 方法與架構", "## 實驗設定", "## 核心數據與成果"]:
                    if sec not in content:
                        issues.append(f"wiki/papers/{p.name} (method): 缺少必填逐字標題 '{sec}'")
            elif ptype == "dataset":
                for sec in ["## 方法與架構", "## 核心數據與成果"]:
                    if sec not in content:
                        issues.append(f"wiki/papers/{p.name} (dataset): 缺少必填逐字標題 '{sec}'")
            elif ptype == "benchmark":
                for sec in ["## 實驗設定", "## 核心數據與成果"]:
                    if sec not in content:
                        issues.append(f"wiki/papers/{p.name} (benchmark): 缺少必填逐字標題 '{sec}'")
            elif ptype == "survey":
                body = self.get_section(content, "## 方法與架構")
                if body is not None:
                    if "不適用" not in body:
                        issues.append(f"wiki/papers/{p.name} (survey): '## 方法與架構' 應標註 '不適用（附理由）'")

        # 模板殘留：papers、entities、synthesis 底下所有 .md（已去除 HTML 註解）不得含 {{ 或 }}
        for sdir in (self.papers_dir, self.entities_dir, self.synthesis_dir):
            for md in sorted(sdir.glob("*.md")):
                if not md.is_file():
                    continue
                for ln, text in enumerate(self.read_md(md).split("\n"), 1):
                    if "{{" in text or "}}" in text:
                        issues.append(f"{md.relative_to(self.root).as_posix()}:{ln}: 含模板殘留 '{{{{' 或 '}}}}': '{text.strip()[:50]}'")

        self.log_result(3, "欄位名與章節標題逐字對照遵從性檢查", len(issues) == 0, issues)

    # 4. 每篇筆記「矛盾／待釐清」標題與內容檢查
    def check_contradictions_heading(self):
        """
        項目 4：必填章節非空（去除 HTML 註解後，以 get_section() 逐行切章節）。
        「矛盾／待釐清」缺標題在此報；其他章節缺標題由項目 3 報，這裡只檢查存在的章節是否為空。
        「論文未提及」「不適用（附理由）」「論文未定義」「無」皆算非空。
        """
        missing = []
        paper_always = ["## 基本資訊", "## 研究動機與欲解決問題", "## 核心貢獻與作者觀點",
                        "## 論文提及之局限性", "## 提及實體清單", "## 矛盾／待釐清"]
        paper_by_type = {
            "method": ["## 方法與架構", "## 實驗設定", "## 核心數據與成果"],
            "dataset": ["## 方法與架構", "## 核心數據與成果"],
            "benchmark": ["## 實驗設定", "## 核心數據與成果"],
        }
        entity_required = ["## 定義", "## 核心屬性與特點", "## 在各論文中的應用與實驗表現", "## 矛盾／待釐清"]

        for p in sorted(self.papers_dir.glob("*.md")):
            if not p.is_file() or p.name == ".gitkeep":
                continue
            content = self.read_md(p)
            ptype = self.parse_frontmatter(content).get("type", "")
            for sec in paper_always + paper_by_type.get(ptype, []):
                body = self.get_section(content, sec)
                if body is None:
                    if sec == "## 矛盾／待釐清":
                        missing.append(f"wiki/papers/{p.name}: 缺少 '## 矛盾／待釐清' 標題")
                elif body.strip() == "":
                    missing.append(f"wiki/papers/{p.name}: '{sec}' 內容不可為空白（無內容請寫「論文未提及」或「不適用（附理由）」）")

        for ent in sorted(self.entities_dir.glob("*.md")):
            if not ent.is_file() or ent.name == ".gitkeep":
                continue
            content = self.read_md(ent)
            for sec in entity_required:
                body = self.get_section(content, sec)
                if body is None:
                    if sec == "## 矛盾／待釐清":
                        missing.append(f"wiki/entities/{ent.name}: 缺少 '## 矛盾／待釐清' 標題")
                elif body.strip() == "":
                    missing.append(f"wiki/entities/{ent.name}: '{sec}' 內容不可為空白（論文未定義請寫「論文未定義」，無衝突請寫「無」）")

        self.log_result(4, "必填章節非空檢查（論文頁依 type、實體頁 4 章節；含「矛盾／待釐清」）", len(missing) == 0, missing)

    # 5. PDF 與論文筆記對齊檢查（拆分為 5a 與 5b）
    def check_pdf_alignment(self):
        orphaned_notes = []
        pending_pdfs = []

        if not self.raw_dir.exists():
            orphaned_notes.append(f"raw/ 目錄不存在: {self.raw_dir}")
            self.log_result(5, "PDF 與論文筆記對齊檢查", False, orphaned_notes)
            return

        pdf_files = [f.stem for f in self.raw_dir.glob("*.pdf")]
        paper_files = [f.stem for f in self.papers_dir.glob("*.md") if f.is_file() and f.name != ".gitkeep"]

        # 5a: 論文頁沒有對應 PDF -> 一律 FAIL
        for p in paper_files:
            if p not in pdf_files:
                orphaned_notes.append(f"wiki/papers/{p}.md 在 raw/ 中找不到對應的 {p}.pdf (孤立論文筆記)")

        # 5b: PDF 沒有對應論文頁 -> 平時標為待 Ingest，加 --final 時 FAIL
        for pdf in pdf_files:
            if pdf not in paper_files:
                msg = f"raw/{pdf}.pdf 尚未完成 Ingest (缺少 wiki/papers/{pdf}.md)"
                if self.is_final:
                    orphaned_notes.append(msg)
                else:
                    pending_pdfs.append(msg)

        passed = len(orphaned_notes) == 0
        self.log_result(5, f"PDF 與論文筆記對齊檢查 (final={self.is_final})", passed, orphaned_notes, pending=pending_pdfs)

    # 6. 實體 sources 建頁門檻檢查 (len(sources) >= 2 或 core_contribution_of)
    def check_entity_threshold(self):
        issues = []
        for ent in self.entities_dir.glob("*.md"):
            if not ent.is_file() or ent.name == ".gitkeep":
                continue
            content = self.read_md(ent)
            fm = self.parse_frontmatter(content)
            sources = fm.get("sources", [])
            if isinstance(sources, str):
                sources = [sources] if sources else []
            core_contrib = fm.get("core_contribution_of", "")

            if len(sources) < 2 and not core_contrib:
                issues.append(f"wiki/entities/{ent.name}: 未達建頁門檻 (sources 數量 {len(sources)} < 2 且未標註 core_contribution_of)")

        self.log_result(6, "實體 sources 建頁門檻檢查 (len(sources) >= 2 或核心貢獻)", len(issues) == 0, issues)

    # 7. 全域索引 index.md 完整性檢查
    def check_index_completeness(self):
        issues = []
        if not self.index_file.exists():
            issues.append("wiki/index.md 檔案不存在")
            self.log_result(7, "全域索引 index.md 完整性檢查", False, issues)
            return

        index_content = self.read_md(self.index_file)

        for p in self.papers_dir.glob("*.md"):
            if not p.is_file() or p.name == ".gitkeep":
                continue
            if f"[[{p.stem}]]" not in index_content:
                issues.append(f"wiki/papers/{p.name} 未登記在 wiki/index.md 中")

        for ent in self.entities_dir.glob("*.md"):
            if not ent.is_file() or ent.name == ".gitkeep":
                continue
            if f"[[{ent.stem}]]" not in index_content:
                issues.append(f"wiki/entities/{ent.name} 未登記在 wiki/index.md 中")

        for syn in self.synthesis_dir.glob("*.md"):
            if not syn.is_file() or syn.name == ".gitkeep":
                continue
            if f"[[{syn.stem}]]" not in index_content:
                issues.append(f"wiki/synthesis/{syn.name} 未登記在 wiki/index.md 中")

        self.log_result(7, "全域索引 index.md 完整性檢查", len(issues) == 0, issues)

    # 8. 操作日誌 log.md 格式與日期檢查
    def check_log_format_and_dates(self):
        issues = []
        if not self.log_file.exists():
            issues.append("wiki/log.md 檔案不存在")
            self.log_result(8, "操作日誌 log.md 格式與日期檢查", False, issues)
            return

        log_content = self.read_md(self.log_file)
        lines = log_content.splitlines()

        header_pattern = re.compile(r'^## \[(\d{4}-\d{2}-\d{2})\]\s+([a-zA-Z]+)\s+\|\s+(.+)$')
        valid_types = {"init", "ingest", "update", "synthesis", "lint", "deck"}

        dates = []
        found_entries = 0
        today_str = datetime.now().strftime("%Y-%m-%d")

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("## ["):
                found_entries += 1
                m = header_pattern.match(line_str)
                if not m:
                    issues.append(f"log.md 格式不符規定: '{line_str}' (格式應為 ## [YYYY-MM-DD] <類型> | <說明>)")
                    continue
                date_str, log_type, desc = m.groups()
                if log_type not in valid_types:
                    issues.append(f"log.md 類型 '{log_type}' 不合法 (必須是 {valid_types})")

                try:
                    entry_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if date_str > today_str:
                        issues.append(f"log.md 日期在未來: {date_str} (不可晚於今天 {today_str})")
                    dates.append(entry_date)
                except ValueError:
                    issues.append(f"log.md 日期非法: {date_str}")

        for i in range(1, len(dates)):
            if dates[i] < dates[i - 1]:
                issues.append(f"log.md 日期未依序遞增: {dates[i].strftime('%Y-%m-%d')} 早於前一筆 {dates[i-1].strftime('%Y-%m-%d')}")

        if found_entries == 0:
            issues.append("log.md 內無任何日誌項目")

        self.log_result(8, "操作日誌 log.md 格式與日期檢查", len(issues) == 0, issues)

    # 9. 核心貢獻與作者觀點標籤檢查
    def check_claims_and_viewpoints(self):
        issues = []
        valid_prefixes = ("[作者聲稱]", "[AI 整理，待核對]")

        for p in self.papers_dir.glob("*.md"):
            if not p.is_file() or p.name == ".gitkeep":
                continue
            body = self.get_section(self.read_md(p), "## 核心貢獻與作者觀點")
            if body is not None:
                for line in body.split("\n"):
                    line = line.strip()
                    if line.startswith("- ") or line.startswith("* "):
                        bullet_content = line[2:].strip()
                        if not any(bullet_content.startswith(pfx) for pfx in valid_prefixes):
                            issues.append(f"wiki/papers/{p.name}: 核心貢獻條列未以 [作者聲稱] 或 [AI 整理，待核對] 開頭: '{line[:40]}...'")

        self.log_result(9, "核心貢獻觀點屬性標籤檢查 ([作者聲稱] / [AI 整理，待核對])", len(issues) == 0, issues)

    # 10. AGENTS.md 長度限制檢查 (<= 12,000 字元)
    def check_agents_length(self):
        issues = []
        if not self.agents_file.exists():
            issues.append("AGENTS.md 檔案不存在")
            self.log_result(10, "AGENTS.md 字元數限制檢查 (<= 12,000)", False, issues)
            return

        content = self.agents_file.read_text(encoding="utf-8", errors="replace")
        char_count = len(content)
        if char_count > 12000:
            issues.append(f"AGENTS.md 字元數超過上限: {char_count} > 12,000")

        self.log_result(10, f"AGENTS.md 字元數檢查 ({char_count} <= 12,000)", len(issues) == 0, issues)

    def run_all(self):
        self.check_links_and_orphans()
        self.check_bidirectional_consistency()
        self.check_schema_and_verbatim_headings()
        self.check_contradictions_heading()
        self.check_pdf_alignment()
        self.check_entity_threshold()
        self.check_index_completeness()
        self.check_log_format_and_dates()
        self.check_claims_and_viewpoints()
        self.check_agents_length()

        report_lines = []
        report_lines.append("=================================================================")
        report_lines.append("           SER LLM WIKI 自動化品質檢查報告 (scripts/check.py)")
        report_lines.append("=================================================================")
        report_lines.append(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"檢查根目錄: {self.root}")
        report_lines.append(f"完工模式 (--final): {self.is_final}")
        report_lines.append("-----------------------------------------------------------------")

        pass_count = 0
        fail_count = 0

        for r in self.results:
            status_symbol = "[ PASS ]" if r["status"] == "PASSED" else "[ FAIL ]"
            if r["passed"]:
                pass_count += 1
            else:
                fail_count += 1
            report_lines.append(f"項目 {r['no']:02d}: {status_symbol} {r['name']}")
            if r["details"]:
                for d in r["details"]:
                    report_lines.append(f"         └── 失敗原因: {d}")
            if r["pending"]:
                for p in r["pending"]:
                    report_lines.append(f"         └── [待 Ingest]: {p}")
            if r["indeterminate"]:
                for ind in r["indeterminate"]:
                    report_lines.append(f"         └── [無法判斷]: {ind}")

        report_lines.append("-----------------------------------------------------------------")
        report_lines.append(f"總結: 通過 {pass_count} 項，失敗 {fail_count} 項")
        report_lines.append("=================================================================")

        report_text = "\n".join(report_lines)
        print(report_text)

        # 寫入 <root>/temp/check-report.txt (UTF-8)
        temp_dir = self.root / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        report_file = temp_dir / "check-report.txt"
        report_file.write_text(report_text, encoding="utf-8")

        return 1 if self.has_failure else 0

def main():
    parser = argparse.ArgumentParser(description="SER LLM Wiki 結構與一致性檢查腳本")
    parser.add_argument("--root", type=str, default=".", help="專案根目錄路徑")
    parser.add_argument("--final", action="store_true", help="完工檢查模式 (所有 PDF 均需有對應論文頁)")
    args = parser.parse_args()

    checker = WikiChecker(Path(args.root), is_final=args.final)
    exit_code = checker.run_all()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
