#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/check_deck.py - 簡報（deck/slides.md 與選用的 deck/index.html）檢查腳本

檢查項目：
1. 投影片切分：以單獨一行的 `---` 分隔；每頁第一個非空行必須是 `# 標題`；總頁數必須在 10–12 之間。
2. 每頁至少一個 [[slug]]；所有 [[slug]] 必須存在於 wiki/papers、wiki/entities、wiki/synthesis。
3. 數字規則同非論文頁：數字後接 [本文] 或 [引述]，再接 [[論文slug]] (p. N...)；頁碼只接受四種格式；
   沿用 check_numbers.py 的例外遮蔽與 scripts/name_exceptions.txt。
   標題行（# 開頭）不得含阿拉伯數字（含全形），數字須放在內文並附標籤與來源。
4. 數字溯源到 wiki（不讀 PDF）：每個帶標籤的數字，必須在 wiki/papers/<論文slug>.md 找到
   「同一個數字、同一個標籤、同一個頁碼」；分辨「數字不在論文頁／標籤不同／頁碼不同／標籤與頁碼皆不同」。
5. 引文行 `> "..." [[slug]] (p. N)`：引號內文字（空白壓縮後）必須是 wiki/papers/<slug>.md 某段引文的逐字子字串。
6. --html <路徑>：單一檔案、無外部資源、投影片數與 slides.md 相同；
   內容比對：去除 <script>、<style> 與所有標籤後，每張投影片中的每個阿拉伯數字都必須出現在對應頁的 slides.md 原文，
   且 slides.md 每頁標題文字必須出現在對應投影片中；
   另以 build_deck.build() 從 slides.md 重新產生 HTML，必須與檔案逐位元組相同（兩邊先統一換行為 \\n）。
   HTML 投影片標記：每張投影片為一個 class 屬性含 `slide` 這個 token 的 <section> 元素，例如 <section class="slide">。
7. 找不到 deck/slides.md 標「無法判斷」；任何失敗或無法判斷，結束碼非 0。

報告寫入 <root>/temp/check-deck-report.txt（UTF-8）。本腳本唯讀，不修改任何檔案（報告除外）。
"""

import sys
import re
import html as htmllib
import argparse
from pathlib import Path
from datetime import datetime

if sys.platform == "win32" and __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_numbers as cn  # noqa: E402

SLIDE_MIN, SLIDE_MAX = 10, 12
LINK_REGEX = re.compile(r'\[\[([a-zA-Z0-9_\-]+)\]\]')
TAG_REGEX = re.compile(r'\[(本文|引述)\]')
HTML_SLIDE_REGEX = re.compile(
    r'<section\b[^>]*\bclass\s*=\s*(["\'])(?:(?!\1).)*\bslide\b(?:(?!\1).)*\1[^>]*>(.*?)</section\s*>',
    re.IGNORECASE | re.DOTALL)
TITLE_DIGIT_REGEX = re.compile(r'[0-9０-９]')
HTML_NUMBER_REGEX = re.compile(r'\d+(?:\.\d+)*')
HTML_MARKER_DESC = '每張投影片為一個 class 屬性含 "slide" token 的 <section> 元素（例如 <section class="slide">）'


def split_slides(lines: list) -> list:
    """回傳 [(起始行號, [(行號, 行文字), ...]), ...]；以 strip 後等於 '---' 的行分隔。"""
    slides, current = [], []
    for i, line in enumerate(lines, 1):
        if line.strip() == "---":
            slides.append(current)
            current = []
        else:
            current.append((i, line))
    slides.append(current)
    return slides


def normalize_ws(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


class DeckChecker:
    def __init__(self, root: Path, html: str = None):
        self.root = root.resolve()
        self.wiki = self.root / "wiki"
        self.slides_path = self.root / "deck" / "slides.md"
        self.html_path = (self.root / html) if html else None
        self.report_path = self.root / "temp" / "check-deck-report.txt"
        self.names = cn.load_name_exceptions(self.root / "scripts" / "name_exceptions.txt")
        self.failed, self.indeterminate, self.passed = [], [], []
        self.paper_cache = {}
        self.slide_count = None
        self.slide_texts = []   # 每頁 slides.md 原文（已去 HTML 註解）
        self.slide_titles = []  # 每頁 `# 標題` 的標題文字（無標題為 None）

    # ---------- wiki 索引 ----------
    def slug_exists(self, slug: str) -> bool:
        return any((self.wiki / d / f"{slug}.md").is_file() for d in ("papers", "entities", "synthesis"))

    def is_paper(self, slug: str) -> bool:
        return (self.wiki / "papers" / f"{slug}.md").is_file()

    def paper_index(self, slug: str) -> dict:
        """回傳 {"numbers": [(num, tag, cite)], "quotes": [正規化後引文]}；略過標題行與「基本資訊」區塊。"""
        if slug in self.paper_cache:
            return self.paper_cache[slug]
        content = (self.wiki / "papers" / f"{slug}.md").read_text(encoding="utf-8", errors="replace")
        numbers, quotes = [], []
        in_basic = False
        for raw in cn.prepare_lines(content):
            line = raw.strip()
            if not line:
                continue
            if line.startswith("## "):
                in_basic = "基本資訊" in line
                continue
            if in_basic or line.startswith("#"):
                continue
            text, at_start = line, True
            if line.startswith(">"):
                parts = cn.split_quote_line(line, True)
                if parts["quote"]:
                    quotes.append(normalize_ws(parts["quote"]))
                text, at_start = parts["remainder"], False
            tagged, _ = cn.scan_plain_line(text, True, self.names, at_start)
            for t in tagged:
                tm = TAG_REGEX.search(t["text"])
                numbers.append((t["num"], f"[{tm.group(1)}]" if tm else "", t["cite"]))
        self.paper_cache[slug] = {"numbers": numbers, "quotes": quotes}
        return self.paper_cache[slug]

    # ---------- 單行檢查 ----------
    def check_links(self, loc: str, text: str):
        for slug in LINK_REGEX.findall(text):
            if not self.slug_exists(slug):
                self.failed.append(f"{loc}: 連結 [[{slug}]] 不存在於 wiki/papers、wiki/entities、wiki/synthesis")

    def trace_number(self, loc: str, num: str, tag: str, slug: str, cite: str):
        desc = f"{num} {tag} [[{slug}]] {cite}"
        if not self.is_paper(slug):
            self.failed.append(f"{loc}: 數字 {desc} 的來源 [[{slug}]] 不是 wiki/papers 下的論文頁，無法溯源")
            return
        entries = [e for e in self.paper_index(slug)["numbers"] if e[0] == num]
        if (num, tag, cite) in entries:
            self.passed.append(f"{loc}: 數字 {desc} 於 wiki/papers/{slug}.md 找到相同數字、標籤與頁碼")
            return
        same_cite = [e for e in entries if e[2] == cite]
        same_tag = [e for e in entries if e[1] == tag]
        if not entries:
            why = f"數字不在論文頁（wiki/papers/{slug}.md 沒有帶標籤的 {num}）"
        elif same_cite:
            why = f"標籤不同（論文頁為 {same_cite[0][1]} {cite}，簡報寫 {tag}）"
        elif same_tag:
            why = f"頁碼不同（論文頁為 {tag} {'、'.join(sorted({e[2] for e in same_tag}))}，簡報寫 {cite}）"
        else:
            found = '、'.join(sorted({f'{e[1]} {e[2]}' for e in entries}))
            why = f"標籤與頁碼皆不同（論文頁為 {found}，簡報寫 {tag} {cite}）"
        self.failed.append(f"{loc}: 數字 {desc} 溯源失敗：{why}")

    def check_plain(self, loc: str, text: str, display: str, at_line_start: bool):
        for m in cn.PAGE_REGEX.finditer(text):
            if not text[:m.start()].rstrip().endswith("]]"):
                self.failed.append(f"{loc}: 引用必須加上來源 [[slug]] (p. N)，不可單獨使用頁碼: '{display[:60]}'")
        tagged, untagged = cn.scan_plain_line(text, False, self.names, at_line_start)
        for t in tagged:
            tm = TAG_REGEX.search(t["text"])
            self.trace_number(loc, t["num"], f"[{tm.group(1)}]", t["slug"], t["cite"])
        for num, hint in untagged:
            msg = f"{loc}: 數字 '{num}' 缺少 [本文]/[引述] 標籤或 [[論文slug]] (p. N): '{display[:60]}'"
            if hint:
                msg += f"（{cn.NAME_HINT}）"
            self.failed.append(msg)

    def check_quote(self, loc: str, line: str):
        parts = cn.split_quote_line(line, False)
        for err in parts["errors"]:
            self.failed.append(f"{loc}: {err}: '{line[:60]}'")
        if parts["quote"] and parts["slug"]:
            slug = parts["slug"]
            if not self.is_paper(slug):
                self.failed.append(f"{loc}: 引文來源 [[{slug}]] 不是 wiki/papers 下的論文頁")
            else:
                q = normalize_ws(parts["quote"])
                if q and any(q in pq for pq in self.paper_index(slug)["quotes"]):
                    self.passed.append(f"{loc}: 引文逐字出現在 wiki/papers/{slug}.md 的引文中")
                else:
                    self.failed.append(f"{loc}: 引文不在 wiki/papers/{slug}.md 的引文中: '{parts['quote'][:40]}'")
        return parts["remainder"]

    # ---------- 主流程 ----------
    def check_slides(self):
        if not self.slides_path.is_file():
            self.indeterminate.append(f"找不到 {self.slides_path.relative_to(self.root).as_posix()}，無法檢查簡報")
            return
        content = self.slides_path.read_text(encoding="utf-8", errors="replace")
        lines = cn.strip_html_comments(content.replace('\r\n', '\n').replace('\r', '\n')).split('\n')
        slides = split_slides(lines)
        self.slide_count = len(slides)
        if SLIDE_MIN <= len(slides) <= SLIDE_MAX:
            self.passed.append(f"總頁數 {len(slides)} 在 {SLIDE_MIN}–{SLIDE_MAX} 之間")
        else:
            self.failed.append(f"總頁數 {len(slides)} 不在 {SLIDE_MIN}–{SLIDE_MAX} 之間")

        for k, slide in enumerate(slides, 1):
            nonempty = [(n, l) for n, l in slide if l.strip()]
            self.slide_texts.append("\n".join(l for _, l in slide))
            if not nonempty:
                self.slide_titles.append(None)
                self.failed.append(f"第 {k} 頁: 沒有內容（第一個非空行必須是 `# 標題`）")
                continue
            first_no, first = nonempty[0]
            if re.match(r'^# \S', first.strip()):
                self.slide_titles.append(first.strip()[2:].strip())
            else:
                self.slide_titles.append(None)
                self.failed.append(f"slides.md:{first_no}（第 {k} 頁）: 第一個非空行必須是 `# 標題`: '{first.strip()[:40]}'")
            if not any(LINK_REGEX.search(l) for _, l in nonempty):
                self.failed.append(f"第 {k} 頁: 沒有任何 [[slug]]")
            for n, raw in nonempty:
                loc = f"slides.md:{n}（第 {k} 頁）"
                line = raw.strip()
                self.check_links(loc, line)
                for cite, why in cn.find_illegal_page_cites(line):
                    self.failed.append(f"{loc}: 頁碼格式非法: '{cite}'（{why}；{cn.LEGAL_FORMATS_DESC}）")
                if line.startswith("#"):
                    if TITLE_DIGIT_REGEX.search(line):
                        self.failed.append(
                            f"{loc}: 標題不得含數字，數字請放在內文並附標籤與來源: '{line[:60]}'")
                    continue
                if line.startswith(">"):
                    remainder = self.check_quote(loc, line)
                    self.check_plain(loc, remainder, line, at_line_start=False)
                else:
                    self.check_plain(loc, line, line, at_line_start=True)

    def check_html(self):
        if self.html_path is None:
            return
        rel = self.html_path.relative_to(self.root).as_posix() if self.html_path.is_relative_to(self.root) else str(self.html_path)
        if not self.html_path.is_file():
            self.failed.append(f"HTML: 找不到 {rel}")
            return
        html = self.html_path.read_text(encoding="utf-8", errors="replace")
        bad = []
        for m in re.finditer(r'\b(src|href)\s*=\s*(["\']?)([^"\'\s>]*)\2', html, re.IGNORECASE):
            val = m.group(3).strip()
            if not (val.startswith("#") or val.lower().startswith("data:")):
                bad.append(f"{m.group(1)}=\"{val[:60]}\"")
        for m in re.finditer(r'url\(\s*(["\']?)([^"\')]*)\1\s*\)', html, re.IGNORECASE):
            val = m.group(2).strip()
            if not (val.startswith("#") or val.lower().startswith("data:")):
                bad.append(f"url({val[:60]})")
        for m in re.finditer(r'@import\b[^;]*', html, re.IGNORECASE):
            bad.append(m.group(0)[:60])
        if bad:
            for b in bad:
                self.failed.append(f"HTML {rel}: 含外部資源或外部檔案參照（只允許頁內錨點 # 與 data: URI）: {b}")
        else:
            self.passed.append(f"HTML {rel}: 無外部資源（src/href/url() 只含頁內錨點或 data: URI，無 @import）")
        body = re.sub(r'<(script|style)\b.*?</\1\s*>', ' ', html, flags=re.IGNORECASE | re.DOTALL)
        sections = [m.group(2) for m in HTML_SLIDE_REGEX.finditer(body)]
        n = len(sections)
        if self.slide_count is None:
            self.indeterminate.append(f"HTML {rel}: slides.md 不存在，無法比對投影片數與內容（HTML 中有 {n} 張）")
            return
        if n == self.slide_count:
            self.passed.append(f"HTML {rel}: 投影片數 {n} 與 slides.md 相同")
        else:
            self.failed.append(f"HTML {rel}: 投影片數不符（HTML {n} 張，slides.md {self.slide_count} 頁）")
        self.check_html_content(rel, sections)
        self.check_html_identical(rel)

    def check_html_identical(self, rel: str):
        """以 build_deck.build() 從 slides.md 重新產生 HTML，與檔案逐位元組比較（兩邊先統一換行為 \\n）。"""
        import build_deck  # 延遲匯入：build_deck 會匯入本模組的 split_slides
        md = self.slides_path.read_text(encoding="utf-8")
        expected = build_deck.build(md).replace('\r\n', '\n').replace('\r', '\n').encode("utf-8")
        actual = self.html_path.read_bytes().replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        if expected == actual:
            self.passed.append(f"HTML {rel}: 與 build_deck.py 由 slides.md 重新產生的輸出逐位元組相同")
            return
        i = next((k for k in range(min(len(expected), len(actual))) if expected[k] != actual[k]),
                 min(len(expected), len(actual)))
        exp_txt = expected.decode("utf-8", errors="replace")
        act_txt = actual.decode("utf-8", errors="replace")
        # 以位元組位置換算成字元位置附近的片段
        ci = len(expected[:i].decode("utf-8", errors="ignore"))
        lo = max(0, ci - 30)
        ctx = lambda t: t[lo:ci + 40].replace("\n", "\\n")
        line_no = expected[:i].count(b'\n') + 1
        self.failed.append(
            f"HTML {rel}: 與 build_deck.py 輸出不一致（第一個不同處約在第 {line_no} 行；"
            f"預期「…{ctx(exp_txt)}…」，實際「…{ctx(act_txt)}…」）")

    @staticmethod
    def section_text(fragment: str) -> str:
        """去除所有標籤並還原 HTML 實體，壓縮空白。"""
        text = re.sub(r'<[^>]+>', ' ', fragment)
        return normalize_ws(htmllib.unescape(text))

    def check_html_content(self, rel: str, sections: list):
        """逐張比對：HTML 中的每個阿拉伯數字須出現在對應頁 slides.md 原文；slides.md 標題須出現在對應 section。"""
        for k, frag in enumerate(sections[:self.slide_count], 1):
            text = self.section_text(frag)
            src_norm = cn.normalize_for_numbers(self.slide_texts[k - 1])
            extra = []
            for num in HTML_NUMBER_REGEX.findall(cn.normalize_for_numbers(text)):
                if not cn.number_in_text(num, src_norm) and num not in extra:
                    extra.append(num)
            for num in extra:
                self.failed.append(f"HTML {rel} 第 {k} 張: 數字 {num} 不在 slides.md 第 {k} 頁原文中")
            if not extra:
                self.passed.append(f"HTML {rel} 第 {k} 張: 所有數字皆出現在 slides.md 第 {k} 頁原文")
            title = self.slide_titles[k - 1]
            if title is None:
                continue
            # 標題中的 **粗體** 記號與 [[slug]] 在 HTML 中會被轉換，只比對其餘文字片段
            parts = [normalize_ws(p) for p in LINK_REGEX.split(title.replace("**", ""))[::2]]
            if all(p in text for p in parts if p):
                self.passed.append(f"HTML {rel} 第 {k} 張: 標題「{title}」與 slides.md 相同")
            else:
                self.failed.append(f"HTML {rel} 第 {k} 張: 標題與 slides.md 不同（slides.md 第 {k} 頁標題為「{title}」，HTML 中找不到）")

    def run(self) -> int:
        self.check_slides()
        self.check_html()
        return self.write_report()

    def write_report(self) -> int:
        status = "FAILED" if self.failed else ("無法判斷" if self.indeterminate else "PASSED")
        r = ["=" * 65, "        SER LLM WIKI 簡報檢查報告 (scripts/check_deck.py)", "=" * 65,
             f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             f"檢查根目錄: {self.root}",
             f"名稱例外清單 (name_exceptions.txt): {len(self.names)} 筆",
             f"HTML 檢查: {self.html_path if self.html_path else '未指定 (--html)'}",
             f"HTML 投影片標記方式: {HTML_MARKER_DESC}",
             "-" * 65,
             f"通過項目: {len(self.passed)} 筆", f"失敗項目: {len(self.failed)} 筆",
             f"無法判斷項目: {len(self.indeterminate)} 筆", "-" * 65]
        if self.failed:
            r.append("[ 失敗項目清單 ]:")
            r += [f"  └── [FAIL] {x}" for x in self.failed]
        if self.indeterminate:
            r.append("[ 無法判斷項目清單 ]:")
            r += [f"  └── [無法判斷] {x}" for x in self.indeterminate]
        if self.passed:
            r.append("[ 通過項目清單 ]:")
            r += [f"  └── [PASS] {x}" for x in self.passed]
        r += ["=" * 65, f"總結判定: [ {status} ] (失敗數: {len(self.failed)}, 無法判斷: {len(self.indeterminate)})", "=" * 65]
        text = "\n".join(r)
        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        self.report_path.write_text(text + "\n", encoding="utf-8")
        print(text)
        return {"PASSED": 0, "FAILED": 1}.get(status, 2)


def main():
    ap = argparse.ArgumentParser(description="檢查 deck/slides.md（與選用的 HTML）")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="專案根目錄")
    ap.add_argument("--html", default=None, help="要檢查的 HTML 路徑（相對於 --root），例如 deck/index.html")
    args = ap.parse_args()
    sys.exit(DeckChecker(Path(args.root), args.html).run())


if __name__ == "__main__":
    main()
