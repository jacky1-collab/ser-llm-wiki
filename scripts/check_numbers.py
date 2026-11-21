#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/check_numbers.py - 數字溯源與頁碼邊界檢查腳本
依據 AGENTS.md 第 11 節與使用者修訂規範實作。
只掃描 wiki/papers、wiki/entities、wiki/synthesis。
檢查包含：
1. 引文與數字的正規化 (NFKC、去軟連字號、合併行尾連字號斷詞、壓縮空白、大小寫、變音符號分離寬鬆比對)。
2. 數字邊界精準比對：前後不得緊鄰「數字」或「小數點加數字」，允許句尾句點；PDF 千分位逗號先移除。
3. 頁碼格式只接受 (p. N)、(p. N, Table M)、(p. N, Fig. M)、(pp. N–M)（en dash 且 N < M），其餘一律非法。
4. (pp. N–M) 範圍內任一頁找到即通過；N、M 皆不得超過 PDF 總頁數。
5. 引述行驗證完引文後，遮蔽「引文＋頁碼」，剩下的文字照一般行做數字檢查。
6. 人工例外豁免 scripts/number_waivers.txt（使用者專用，AI 不得新增或修改）。
7. 例外 6 名稱清單 scripts/name_exceptions.txt（使用者專用，AI 不得新增條目）。
8. 掃描前移除 HTML 註解（含跨行），報告行號一律為原始檔案行號（含 frontmatter）。
9. 找不到數字或引文一律 FAIL；非論文頁缺少 [[slug]] 一律 FAIL。
10. 無待掃描檔案或缺 pypdf 時標記「無法判斷」（結束碼非 0）。
11. 報告寫入 <root>/temp/check-numbers-report.txt 並追加至 <root>/temp/check-report.txt。
"""

import sys
import re
import unicodedata
import argparse
from pathlib import Path
from datetime import datetime

# 確保輸出支援 UTF-8（僅在直接執行時切換，避免被 import 時影響呼叫端）
if sys.platform == "win32" and __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


# ==============================================================================
# 共用常數
# ==============================================================================

# 嚴格頁碼格式（只接受四種）：(p. N)、(p. N, Table M)、(p. N, Fig. M)、(pp. N–M)
PAGE_PATTERN = r'\((?:p\. \d+(?:, (?:Table|Fig\.) \d+)?|pp\. \d+–\d+)\)'
PAGE_REGEX = re.compile(PAGE_PATTERN)
# 寬鬆偵測「看起來像頁碼」的括號，用來抓出非法格式（例如 (p.1)、(pp. 1-2)、(p. 1–2)）
LOOSE_PAGE_REGEX = re.compile(r'\(\s*pp?\s*\.?\s*\d[^()]*\)')
LEGAL_FORMATS_DESC = "只接受 (p. N)、(p. N, Table M)、(p. N, Fig. M)、(pp. N–M)；範圍須用 en dash「–」且 N < M"

# 單位詞定義：不含空白、標點符號與數字，最多 8 字元（允許 %）
_PUNCT_CHARS = r',.!?;:\'"()\[\]{}<>/\\|`~@#$^&*+=_\-，。！？、；：、（）「」『』—《》【】…～'
UNIT_PATTERN = rf'(?:%|[^\s\d{re.escape(_PUNCT_CHARS)}]{{1,8}})'

# 論文頁: 數字 + (可選單位詞) + 標籤 + 頁碼
PAPER_TAGGED_REGEX = re.compile(
    r'(\b\d+(?:\.\d+)?)\s*(?:' + UNIT_PATTERN + r')?\s*(\[(?:本文|引述)\])\s*(' + PAGE_PATTERN + r')'
)
# 非論文頁: 數字 + (可選單位詞) + 標籤 + [[slug]] + 頁碼
NON_PAPER_TAGGED_REGEX = re.compile(
    r'(\b\d+(?:\.\d+)?)\s*(?:' + UNIT_PATTERN + r')?\s*(\[(?:本文|引述)\])\s*(?:\[\[([a-zA-Z0-9_\-]+)\]\]\s*)(' + PAGE_PATTERN + r')'
)

# 剩餘孤立數字：從「前一字元不是數字」處開始，吃完整個數字（含小數、版本號式多段小數與 %）
ORPHAN_NUMBER_REGEX = re.compile(r'(?<!\d)\d+(?:\.\d+)*%?')

NAME_HINT = "若為模型／資料集／指標名稱，請使用者將名稱加入 scripts/name_exceptions.txt"


# ==============================================================================
# 文本正規化
# ==============================================================================

def normalize_text(text: str) -> str:
    """
    文本正規化流程（第一階段）：
    1. 移除 spacing accents (如 ¨ 等，防 NFKC 展開出多餘空白)
    2. Unicode NFKC (展開 ligatures 如 ﬁ -> fi, ﬂ -> fl)
    3. 移除軟連字號 (­)
    4. 合併行尾連字號斷詞 (例如 'emo-\n    tional' -> 'emotional')
    5. 壓縮多餘空白 (包含 \r, \n, \t)
    6. 轉小寫
    """
    if not text:
        return ""
    t = re.sub(r'[¨ˉ´`]', '', text)
    res = unicodedata.normalize('NFKC', t)
    res = res.replace('­', '')
    res = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', res)
    res = re.sub(r'\s+', ' ', res)
    return res.strip().lower()


def normalize_text_strict(text: str) -> str:
    """
    文本正規化流程（第二階段，更寬鬆）：
    在第一階段基礎上，額外移除所有剩餘空白與連字號，
    處理 PDF 抽文中的 'se\ngmented'、'tech -\nniques' 等複雜斷詞。
    """
    base = normalize_text(text)
    res = re.sub(r'-\s*', '', base)
    res = re.sub(r'\s+', '', res)
    return res


def strip_diacritics(text: str) -> str:
    """將變音符號分離移除 (Nöth / N¨oth -> noth)"""
    t = re.sub(r'[¨̈ˉ´`]', '', text)
    nfd = unicodedata.normalize('NFKD', t)
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')


def normalize_for_numbers(text: str) -> str:
    """
    數字比對用的 PDF 文字正規化：
    1. normalize_text（NFKC 等）
    2. 移除千分位逗號（1,102 -> 1102）
    3. 「數字 %」壓縮為「數字%」（51 % 與 51% 視為相同）
    """
    t = normalize_text(text)
    t = re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', t)
    t = re.sub(r'(\d)\s+%', r'\1%', t)
    return t


# ==============================================================================
# 原始檔前處理（HTML 註解、frontmatter，皆保持原始行號）
# ==============================================================================

def strip_html_comments(text: str) -> str:
    """移除 <!-- ... -->（含跨行），以等量換行取代，使後續行號與原始檔案一致。"""
    return re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.DOTALL)


def blank_frontmatter(lines: list) -> list:
    """將 frontmatter（含前後 ---）各行清成空字串，不刪行，保持原始行號。"""
    lines = list(lines)
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip() == "---":
        for j in range(i + 1, len(lines)):
            if lines[j].strip() == "---":
                for k in range(i, j + 1):
                    lines[k] = ""
                break
    return lines


def prepare_lines(content: str) -> list:
    """回傳 list，索引 i 對應原始檔案第 i+1 行。"""
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    return blank_frontmatter(strip_html_comments(content).split('\n'))


# ==============================================================================
# 名稱例外（例外 6）
# ==============================================================================

def load_name_exceptions(path: Path) -> list:
    names = []
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            names.append(s)
    # 長名稱優先遮蔽，避免短名稱先吃掉長名稱的一部分
    return sorted(set(names), key=len, reverse=True)


def mask_names(line: str, names: list) -> str:
    """把清單內的名稱精確（區分大小寫、前後不得接英數或小數）遮蔽為 [NAME]。"""
    for name in names:
        pat = r'(?<![A-Za-z0-9])' + re.escape(name) + r'(?![A-Za-z0-9])(?!\.\d)'
        line = re.sub(pat, '[NAME]', line)
    return line


# ==============================================================================
# 頁碼與比對函式（供 test_normalization.py 直接測試）
# ==============================================================================

def parse_page_cite(cite: str):
    """解析嚴格格式頁碼，回傳 (start, end)；非四種合法格式回傳 None。"""
    if not PAGE_REGEX.fullmatch(cite):
        return None
    m = re.match(r'\((pp?)\. (\d+)(?:–(\d+))?', cite)
    start = int(m.group(2))
    end = int(m.group(3)) if m.group(3) else start
    return start, end


def page_cite_problem(cite: str):
    """合法回傳 None；非法回傳原因字串。"""
    if not PAGE_REGEX.fullmatch(cite):
        return "格式不符"
    if cite.startswith("(pp."):
        start, end = parse_page_cite(cite)
        if start >= end:
            return f"範圍起始頁 {start} 必須小於結束頁 {end}"
    return None


def find_illegal_page_cites(text: str) -> list:
    """回傳 [(cite, 原因)]：所有看起來像頁碼、但不屬於四種合法格式（或範圍 N ≥ M）的括號。"""
    out = []
    for m in LOOSE_PAGE_REGEX.finditer(text):
        why = page_cite_problem(m.group(0))
        if why:
            out.append((m.group(0), why))
    return out


def number_in_text(num: str, norm_text: str) -> bool:
    """
    數字邊界比對：前後不得緊鄰「數字」或「小數點加數字」；允許句尾句點（62.3. 可吻合 62.3）。
    norm_text 須先經 normalize_for_numbers。
    """
    raw = num.replace("%", "").strip()
    pat = r'(?<!\d)(?<!\d\.)' + re.escape(raw) + r'(?!\d)(?!\.\d)'
    return re.search(pat, norm_text) is not None


def find_number_in_pages(num: str, pages_text: dict, start: int, end: int):
    """在 start..end 任一頁找到即回傳該頁碼，否則 None。"""
    for p in range(start, end + 1):
        if number_in_text(num, normalize_for_numbers(pages_text.get(p, ""))):
            return p
    return None


def match_quote(quote: str, page_raw: str):
    """回傳 (matched, reason)。reason 為空字串表示第一階段即吻合。"""
    norm_quote = normalize_text(quote)
    norm_pdf = normalize_text(page_raw)
    if norm_quote and norm_quote in norm_pdf:
        return True, ""
    strict_quote = normalize_text_strict(quote)
    if strict_quote and strict_quote in normalize_text_strict(page_raw):
        return True, "寬鬆比對: 移除所有空白與連字號"
    if any(ord(c) > 127 for c in quote):
        stripped_q = strip_diacritics(norm_quote).strip()
        # 去除變音符號後必須仍有內容，否則空字串會「吻合」任何頁面（例如引文只有 "¨"）
        if stripped_q and stripped_q in strip_diacritics(norm_pdf):
            return True, "寬鬆比對: 變音符號分離"
    return False, ""


def match_quote_in_pages(quote: str, pages_text: dict, start: int, end: int):
    """(pp. N–M) 時把範圍內頁面依序串接後比對（引文可能跨頁）。"""
    joined = "\n".join(pages_text.get(p, "") for p in range(start, end + 1))
    return match_quote(quote, joined)


def mask_exceptions(line: str, at_line_start: bool = True) -> str:
    """遮蔽 AGENTS.md 第 3 節的例外（例外 6 名稱另由 mask_names 處理）。"""
    m = line
    # 例外 1: 引用頁碼本身（合法格式）；非法格式已另行報錯，這裡一併遮蔽避免重複報出括號內數字
    m = PAGE_REGEX.sub('[PAGE_REF]', m)
    m = LOOSE_PAGE_REGEX.sub('[BAD_PAGE_REF]', m)
    # 例外 3: 連結 [[slug]] 與檔名
    m = re.sub(r'\[\[[a-zA-Z0-9_\-]+\]\]', '[LINK]', m)
    m = re.sub(r'[\w./\\\-]+\.(?:pdf|md|txt|py|html)\b', '[FILE]', m)
    # 例外 5: Table M / Fig. M
    m = re.sub(r'\b(?:Table|Fig\.)\s*\d+\b', '[TABLE_FIG]', m)
    # 例外 4 & 7: 標題編號、有序清單的編號記號（只遮蔽「1.」「2)」記號本身，不吃後面的數字；
    # 無序清單 - / * 後面的內容一律不遮蔽）
    if at_line_start:
        m = re.sub(r'^#{1,6}\s+\d+(?:\.\d+)*\b', '[HEADING_NUM]', m)
        m = re.sub(r'^(\s*)\d+[.)](?=\s)', r'\1[LIST_MARK]', m)
    m = re.sub(r'第\s*\d+\s*節', '[SECTION_NO]', m)
    return m


def find_untagged_numbers(masked_line: str) -> list:
    """回傳 [(數字字串, 是否需加名稱提示)]；緊鄰英文字或連字號者需提示。"""
    out = []
    for mt in ORPHAN_NUMBER_REGEX.finditer(masked_line):
        before = masked_line[mt.start() - 1] if mt.start() > 0 else ""
        after = masked_line[mt.end()] if mt.end() < len(masked_line) else ""
        hint = bool(re.match(r'[A-Za-z\-]', before) or re.match(r'[A-Za-z\-]', after))
        out.append((mt.group(0), hint))
    return out


def scan_plain_line(line: str, is_paper_page: bool, names: list, at_line_start: bool = True):
    """
    處理一般文字：回傳 (tagged_matches, untagged)。
    tagged_matches: list of dict(num, slug, cite, text)
    untagged: list of (num, hint)
    """
    work = mask_names(line, names)
    active = PAPER_TAGGED_REGEX if is_paper_page else NON_PAPER_TAGGED_REGEX
    tagged = []
    masked = work
    for tm in active.finditer(work):
        if is_paper_page:
            tagged.append({"num": tm.group(1), "slug": None, "cite": tm.group(3), "text": tm.group(0)})
        else:
            tagged.append({"num": tm.group(1), "slug": tm.group(3), "cite": tm.group(4), "text": tm.group(0)})
        masked = masked.replace(tm.group(0), "[TAGGED_NUMBER]", 1)
    masked = mask_exceptions(masked, at_line_start)
    return tagged, find_untagged_numbers(masked)


def split_quote_line(line: str, is_paper_page: bool):
    """
    拆解引述行（以 > 開頭）。回傳 dict：
      quote: 引文文字或 None（找不到雙引號）
      cite / slug: 緊接在引文後的合法頁碼與（非論文頁）來源 slug，找不到為 None
      remainder: 遮蔽「引文＋頁碼」後剩下、需照一般行檢查的文字（引號前若有文字也併入，不丟棄）
      errors: 結構錯誤訊息清單（空清單表示無結構錯誤）
    """
    body = line[1:]
    qm = re.search(r'["“](.*?)["”]', body)
    if not qm:
        return {"quote": None, "cite": None, "slug": None, "remainder": body,
                "errors": ["引述格式未以雙引號包含英文原句"]}
    prefix = body[:qm.start()]
    quote = qm.group(1).strip()
    after = body[qm.end():]

    # 規則 A1：> 之後（只允許空白）第一個字元必須是雙引號；引號前的文字不可丟掉，併入剩餘文字照一般行檢查
    if prefix.strip():
        return {"quote": None, "cite": None, "slug": None, "remainder": prefix + " " + after,
                "errors": ["引述行必須以雙引號開頭，引號前不得有其他文字"]}

    errors = []
    cite = slug = None
    if is_paper_page:
        cm = re.match(r'\s*(' + PAGE_PATTERN + r')', after)
        if cm:
            cite, remainder = cm.group(1), after[cm.end():]
        else:
            remainder = after
            errors.append("引述後未緊接合法頁碼 (引述未附合法頁碼)")
    else:
        cm = re.match(r'\s*\[\[([a-zA-Z0-9_\-]+)\]\]\s*(' + PAGE_PATTERN + r')', after)
        if cm:
            slug, cite, remainder = cm.group(1), cm.group(2), after[cm.end():]
        else:
            remainder = after
            errors.append("非論文頁之引述缺少來源連結 [[slug]] (p. N)")

    # 規則 A2：引文之後的剩餘文字不得再出現雙引號
    if re.search(r'["“”]', remainder):
        errors.append("一行只能有一段引述，請另起一行")

    return {"quote": quote, "cite": cite, "slug": slug, "remainder": remainder, "errors": errors}


# ==============================================================================
# 主檢查器
# ==============================================================================

class NumberChecker:
    def __init__(self, root_dir: Path):
        self.root = root_dir.resolve()
        self.raw_dir = self.root / "raw"
        self.wiki_dir = self.root / "wiki"
        self.papers_dir = self.wiki_dir / "papers"
        self.entities_dir = self.wiki_dir / "entities"
        self.synthesis_dir = self.wiki_dir / "synthesis"
        self.waivers_file = self.root / "scripts" / "number_waivers.txt"
        self.names_file = self.root / "scripts" / "name_exceptions.txt"

        self.pdf_cache = {}
        self.waivers = self.load_waivers()
        self.names = load_name_exceptions(self.names_file)

        self.failed_items = []
        self.indeterminate_items = []
        self.passed_items = []

    def load_waivers(self) -> set:
        waivers = set()
        if self.waivers_file.exists():
            for line in self.waivers_file.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    waivers.add((parts[0], parts[1], parts[2]))
        return waivers

    def load_pdf(self, pdf_path: Path):
        if not PYPDF_AVAILABLE or not pdf_path.exists():
            return None
        if pdf_path in self.pdf_cache:
            return self.pdf_cache[pdf_path]
        try:
            reader = pypdf.PdfReader(str(pdf_path))
            pages_text = {}
            for i, page in enumerate(reader.pages):
                try:
                    pages_text[i + 1] = page.extract_text() or ""
                except Exception:
                    pages_text[i + 1] = ""
            self.pdf_cache[pdf_path] = {"total_pages": len(reader.pages), "pages_text": pages_text}
            return self.pdf_cache[pdf_path]
        except Exception:
            return None

    def wiki_relative_parts(self, md_file: Path):
        """回傳相對於 wiki/ 的路徑分段；不在 wiki/ 底下回傳 ()。"""
        try:
            return Path(md_file).resolve().relative_to(self.wiki_dir).parts
        except ValueError:
            return ()

    def is_paper_page(self, md_file: Path) -> bool:
        """以相對於 wiki/ 的路徑判斷：wiki/papers/<檔名>.md 才是論文頁（與上層資料夾名稱無關）。"""
        parts = self.wiki_relative_parts(md_file)
        return len(parts) == 2 and parts[0] == "papers"

    def find_target_pdf(self, md_file: Path, source_slug: str = None):
        if self.is_paper_page(md_file):
            return self.raw_dir / f"{Path(md_file).stem}.pdf"
        if source_slug:
            return self.raw_dir / f"{source_slug}.pdf"
        return None

    def resolve_pages(self, loc: str, what: str, cite: str, md_file: Path, slug: str):
        """共用：解析頁碼、找 PDF、檢查頁碼邊界。成功回傳 (pdf_path, pdf_data, start, end)，失敗回傳 None（已記錄）。"""
        if page_cite_problem(cite):
            # 非法格式／範圍已由 find_illegal_page_cites 在本行報錯，這裡不重複報，只停止比對
            return None
        start, end = parse_page_cite(cite)
        if not PYPDF_AVAILABLE:
            self.indeterminate_items.append(f"{loc}: 缺少 pypdf 套件，無法進行 PDF {what}比對")
            return None
        pdf_path = self.find_target_pdf(md_file, slug)
        if not pdf_path or not pdf_path.exists():
            self.failed_items.append(f"{loc}: 找不到{what}對應之 PDF 檔案: {pdf_path}")
            return None
        pdf_data = self.load_pdf(pdf_path)
        if not pdf_data:
            self.failed_items.append(f"{loc}: 無法讀取 PDF 內容: {pdf_path.name}")
            return None
        total = pdf_data["total_pages"]
        if start > total or end > total:
            pages_desc = f"p. {start}" if start == end else f"pp. {start}–{end}"
            self.failed_items.append(f"{loc}: {what}標註頁碼 {pages_desc} 超過 {pdf_path.name} 總頁數 ({total})")
            return None
        return pdf_path, pdf_data, start, end

    def check_quote(self, loc: str, line: str, md_file: Path, is_paper: bool) -> str:
        """驗證引文，回傳遮蔽「引文＋頁碼」後需照一般行檢查的剩餘文字。"""
        parts = split_quote_line(line, is_paper)
        for err in parts["errors"]:
            self.failed_items.append(f"{loc}: {err}: '{line}'")
        if parts["quote"] is None or parts["cite"] is None:
            # 結構錯誤時不做引文比對，但剩餘文字（含引號前文字）仍交回一般行檢查
            return parts["remainder"]

        resolved = self.resolve_pages(loc, "引述", parts["cite"], md_file, parts["slug"])
        if resolved:
            pdf_path, pdf_data, start, end = resolved
            pages_desc = f"p. {start}" if start == end else f"pp. {start}–{end}"
            matched, reason = match_quote_in_pages(parts["quote"], pdf_data["pages_text"], start, end)
            if matched:
                tag = f" ({reason})" if reason else ""
                self.passed_items.append(f"{loc}: 引述在 {pdf_path.name} {pages_desc} 吻合{tag}")
            else:
                self.failed_items.append(f"{loc}: 引述在 {pdf_path.name} {pages_desc} 查無吻合文字: '{parts['quote'][:35]}...'")
        return parts["remainder"]

    def check_plain(self, loc: str, line_no: int, text: str, display: str, md_file: Path, is_paper: bool, at_line_start: bool):
        if not is_paper:
            for m in PAGE_REGEX.finditer(text):
                if not text[:m.start()].rstrip().endswith("]]"):
                    self.failed_items.append(
                        f"{loc}: 非論文頁之引用必須加上來源 [[slug]] (p. N)，不可單獨使用頁碼: '{display[:50]}...'")

        tagged, untagged = scan_plain_line(text, is_paper, self.names, at_line_start)

        for t in tagged:
            num_val = t["num"]
            if (md_file.name, str(line_no), num_val) in self.waivers:
                self.passed_items.append(f"{loc}: 數字 {num_val} 符合人工例外豁免清單 (WAIVER)")
                continue
            resolved = self.resolve_pages(loc, f"數字 {num_val} ", t["cite"], md_file, t["slug"])
            if not resolved:
                continue
            pdf_path, pdf_data, start, end = resolved
            pages_desc = f"p. {start}" if start == end else f"pp. {start}–{end}"
            found = find_number_in_pages(num_val, pdf_data["pages_text"], start, end)
            if found is not None:
                self.passed_items.append(f"{loc}: 數字 {num_val} 成功於 {pdf_path.name} p. {found} 溯源比對")
            else:
                self.failed_items.append(f"{loc}: 數字 {num_val} 在 {pdf_path.name} {pages_desc} 查無完全吻合 (未找到獨立數字)")

        for num, hint in untagged:
            if (md_file.name, str(line_no), num) in self.waivers:
                self.passed_items.append(f"{loc}: 數字 {num} 符合人工例外豁免清單 (WAIVER)")
                continue
            msg = f"{loc}: 數字 '{num}' 缺少 [本文]/[引述] 標籤或未在同一句/格附帶頁碼: '{display[:60]}...'"
            if hint:
                msg += f"（{NAME_HINT}）"
            self.failed_items.append(msg)

    def run_check(self):
        if not PYPDF_AVAILABLE:
            self.indeterminate_items.append("缺少 pypdf 套件：所有 PDF 文字比對（數字、引文、頁碼上限）無法判斷；其他檢查照常執行")

        target_files = []
        for sdir in [self.papers_dir, self.entities_dir, self.synthesis_dir]:
            if sdir.exists():
                target_files.extend(f for f in sorted(sdir.glob("*.md")) if f.is_file())

        if not target_files:
            self.indeterminate_items.append(
                "未找到任何可掃描的檔案 (wiki/papers, wiki/entities, wiki/synthesis 為空或無檔案)")
            return self.write_report()

        for md_file in target_files:
            content = md_file.read_text(encoding="utf-8", errors="replace")
            is_paper = self.is_paper_page(md_file)
            lines = prepare_lines(content)
            in_basic_info = False

            for idx, raw_line in enumerate(lines):
                line_no = idx + 1  # 原始檔案行號（含 frontmatter）
                loc = f"{md_file.name}:{line_no}"
                line = raw_line.strip()
                if not line:
                    continue

                if line.startswith("## "):
                    in_basic_info = "基本資訊" in line
                    continue
                if in_basic_info or line.startswith("#"):
                    continue

                # 頁碼格式：所有行（引述行與一般行）一律檢查
                for cite, why in find_illegal_page_cites(line):
                    self.failed_items.append(f"{loc}: 頁碼格式非法: '{cite}'（{why}；{LEGAL_FORMATS_DESC}）")

                if line.startswith(">"):
                    remainder = self.check_quote(loc, line, md_file, is_paper)
                    # 引文＋頁碼已遮蔽，剩下的文字照一般行檢查（不可略過整行）
                    self.check_plain(loc, line_no, remainder, line, md_file, is_paper, at_line_start=False)
                else:
                    self.check_plain(loc, line_no, line, line, md_file, is_paper, at_line_start=True)

        return self.write_report()

    def write_report(self):
        r = []
        r.append("=================================================================")
        r.append("       SER LLM WIKI 數字溯源與頁碼邊界報告 (scripts/check_numbers.py)")
        r.append("=================================================================")
        r.append(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        r.append(f"檢查根目錄: {self.root}")
        r.append(f"名稱例外清單 (name_exceptions.txt): {len(self.names)} 筆")
        r.append("-----------------------------------------------------------------")
        r.append(f"比對通過項目: {len(self.passed_items)} 筆")
        r.append(f"驗證失敗項目: {len(self.failed_items)} 筆")
        r.append(f"無法判斷項目: {len(self.indeterminate_items)} 筆")
        r.append("-----------------------------------------------------------------")

        if self.passed_items:
            # 列出通過明細，寬鬆比對（可能因抽字格式差異造成誤報）會在括號內明確標示
            r.append("[ 通過項目清單 ]:")
            for item in self.passed_items:
                r.append(f"  └── [PASS] {item}")
        if self.failed_items:
            r.append("[ 失敗項目清單 ]:")
            for item in self.failed_items:
                r.append(f"  └── [FAIL] {item}")
        if self.indeterminate_items:
            r.append("[ 無法判斷項目清單 ]:")
            for item in self.indeterminate_items:
                r.append(f"  └── [INDET] {item}")

        if self.failed_items:
            status_str = "FAILED"
        elif self.indeterminate_items:
            status_str = "無法判斷"
        else:
            status_str = "PASSED"
        r.append("=================================================================")
        r.append(f"總結判定: [ {status_str} ] (失敗數: {len(self.failed_items)}, 無法判斷: {len(self.indeterminate_items)})")
        r.append("=================================================================")

        report_text = "\n".join(r)
        print(report_text)

        temp_dir = self.root / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        (temp_dir / "check-numbers-report.txt").write_text(report_text, encoding="utf-8")
        with (temp_dir / "check-report.txt").open("a", encoding="utf-8") as f:
            f.write("\n\n" + report_text)

        return 0 if status_str == "PASSED" else 1


def main():
    parser = argparse.ArgumentParser(description="SER LLM Wiki 數字溯源檢查腳本")
    parser.add_argument("--root", type=str, default=".", help="專案根目錄路徑")
    args = parser.parse_args()
    sys.exit(NumberChecker(Path(args.root)).run_check())


if __name__ == "__main__":
    main()
