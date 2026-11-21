#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/test_check_deck.py - check_deck.py 的案例測試

每個案例在 <專案>/temp/check_deck_tests/<案例名>/ 建立臨時 wiki、deck 與 scripts/name_exceptions.txt
（皆為測試用假資料，非論文內容），以子程序執行 check_deck.py --root <臨時目錄>，
比對結束碼與報告中的預期訊息；變異以 replace_in() 套用，若內容未改變即判定案例無效。
不讀取、不修改正式 wiki/、deck/ 與使用者清單。任一案例失敗結束碼為 1。
"""

import sys
import shutil
import subprocess
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
WORK = ROOT / "temp" / "check_deck_tests"
CHECKER = SCRIPTS / "check_deck.py"
PAPER = "2021-pepino-wav2vec2-ser"

PAPER_MD = """<!-- 測試用假資料，非論文內容 -->
---
title: "Test Paper"
year: 2021
type: method
---

# Test Paper

## 基本資訊
- **發表年份**：2021

## 核心數據與成果（Key Results & Metrics）
- Wav2vec2-PT 所有層：IEMOCAP 67.2 [本文] (p. 3, Table 1)。
- 他人結果 60.7 [引述] (p. 4, Table 2)。
- 使用 12 個 [本文] (p. 1) transformer blocks。
> "features extracted from pre-trained wav2vec 2.0 models are used as input to shallow neural networks" (p. 1)
"""

ENTITY_MD = """<!-- 測試用假資料 -->
---
name: "wav2vec 2.0"
type: model
sources: ["2021-pepino-wav2vec2-ser"]
core_contribution_of: ""
---

# wav2vec 2.0
"""

SYNTH_MD = "<!-- 測試用假資料 -->\n# 評測與基準矩陣\n"


def slide(k: int, body: str) -> str:
    return f"# 第{'一二三四五六七八九十'[k - 1] if k <= 10 else '附'}頁標題\n\n{body}\n"


def valid_slides() -> list:
    s = [
        "什麼是 SER：見 [[benchmark-matrix]]。",
        "IEMOCAP 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)。",
        "他人結果 60.7 [引述] [[2021-pepino-wav2vec2-ser]] (p. 4, Table 2)。",
        "模型使用 wav2vec 2.0，見 [[wav2vec2]]。",
        "> \"pre-trained wav2vec 2.0 models are used as input\" [[2021-pepino-wav2vec2-ser]] (p. 1)",
        "資料集：見 [[benchmark-matrix]]。",
        "特徵：見 [[wav2vec2]]。",
        "模型：見 [[2021-pepino-wav2vec2-ser]]。",
        "評估：見 [[benchmark-matrix]]。",
        "兒童挑戰：見 [[benchmark-matrix]]。",
        "總結：見 [[2021-pepino-wav2vec2-ser]]。",
    ]
    return [slide(i, b) for i, b in enumerate(s, 1)]


BUILDER = SCRIPTS / "build_deck.py"


def run_build(d: Path) -> str:
    p = subprocess.run([sys.executable, str(BUILDER), "--root", str(d)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise AssertionError(f"build_deck.py 失敗：{p.stdout}{p.stderr}")
    return (d / "deck" / "index.html").read_text(encoding="utf-8")


def build(case: str, slides: list = None, names: str = "wav2vec 2.0\n", html: str = None, no_slides=False) -> Path:
    d = WORK / case
    if d.exists():
        shutil.rmtree(d)
    (d / "wiki" / "papers").mkdir(parents=True)
    (d / "wiki" / "entities").mkdir(parents=True)
    (d / "wiki" / "synthesis").mkdir(parents=True)
    (d / "deck").mkdir(parents=True)
    (d / "scripts").mkdir(parents=True)
    (d / "wiki" / "papers" / f"{PAPER}.md").write_text(PAPER_MD, encoding="utf-8")
    (d / "wiki" / "entities" / "wav2vec2.md").write_text(ENTITY_MD, encoding="utf-8")
    (d / "wiki" / "synthesis" / "benchmark-matrix.md").write_text(SYNTH_MD, encoding="utf-8")
    (d / "scripts" / "name_exceptions.txt").write_text("# 測試用臨時清單\n" + names, encoding="utf-8")
    if not no_slides:
        (d / "deck" / "slides.md").write_text("---\n".join(slides if slides is not None else valid_slides()),
                                              encoding="utf-8")
    if html is not None:
        (d / "deck" / "index.html").write_text(html, encoding="utf-8")
    return d


def replace_in(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"變異無效：{path.name} 中找不到 {old!r}")
    out = text.replace(old, new, 1)
    if out == text:
        raise AssertionError(f"變異無效：{path.name} 未改變")
    path.write_text(out, encoding="utf-8")


def run(d: Path, html: bool = False):
    cmd = [sys.executable, str(CHECKER), "--root", str(d)]
    if html:
        cmd += ["--html", "deck/index.html"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    report = (d / "temp" / "check-deck-report.txt").read_text(encoding="utf-8")
    return p.returncode, report


results = []


def case(name, desc, setup, expect_code, expect_msgs, forbid_msgs=(), html=False):
    try:
        d = setup()
        code, report = run(d, html)
        ok_code = (code == 0) if expect_code == 0 else (code != 0)
        missing = [m for m in expect_msgs if m not in report]
        present = [m for m in forbid_msgs if m in report]
        ok = ok_code and not missing and not present
        detail = f"結束碼 {code}"
        if missing:
            detail += f"；缺少預期訊息 {missing}"
        if present:
            detail += f"；出現不應有的訊息 {present}"
    except AssertionError as e:
        ok, detail = False, str(e)
    results.append((name, desc, "0" if expect_code == 0 else "非 0", " / ".join(expect_msgs), ok, detail))


def mutate(case_name, old, new, **kw):
    def _s():
        d = build(case_name, **kw)
        replace_in(d / "deck" / "slides.md", old, new)
        return d
    return _s


NUM = "67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)"

case("C01", "合法簡報（11 頁）通過", lambda: build("C01"), 0, ["總結判定: [ PASSED ]", "總頁數 11"])
case("C02", "數字不在 wiki 論文頁", mutate("C02", NUM, NUM.replace("67.2", "67.9")), 1,
     ["溯源失敗：數字不在論文頁", "總結判定: [ FAILED ]"])
case("C03", "標籤不同（[本文] 寫成 [引述]）", mutate("C03", NUM, NUM.replace("[本文]", "[引述]")), 1,
     ["溯源失敗：標籤不同"])
case("C04", "頁碼不同（p. 3, Table 1 寫成 p. 4, Table 2）",
     mutate("C04", NUM, NUM.replace("(p. 3, Table 1)", "(p. 4, Table 2)")), 1, ["溯源失敗：頁碼不同"])
case("C05", "數字缺標籤", mutate("C05", NUM, NUM.replace(" [本文]", "")), 1,
     ["數字 '67.2' 缺少 [本文]/[引述] 標籤或 [[論文slug]]"])
case("C06", "數字缺 [[slug]]", mutate("C06", NUM, NUM.replace(" [[2021-pepino-wav2vec2-ser]]", "")), 1,
     ["引用必須加上來源 [[slug]] (p. N)", "數字 '67.2' 缺少"])
case("C07", "某頁沒有任何 [[slug]]", mutate("C07", "資料集：見 [[benchmark-matrix]]。", "資料集：見綜合頁。"), 1,
     ["第 6 頁: 沒有任何 [[slug]]"])
case("C08", "連到不存在的 slug", mutate("C08", "特徵：見 [[wav2vec2]]。", "特徵：見 [[no-such-page]]。"), 1,
     ["連結 [[no-such-page]] 不存在"])
case("C09", "只有 9 頁", lambda: build("C09", slides=valid_slides()[:9]), 1, ["總頁數 9 不在 10–12 之間"])
case("C10", "13 頁", lambda: build("C10", slides=valid_slides() + [slide(11, "補充：見 [[wav2vec2]]。")] * 2), 1,
     ["總頁數 13 不在 10–12 之間"])
case("C11", "引文不在 wiki 論文頁",
     mutate("C11", "pre-trained wav2vec 2.0 models are used as input", "fine-tuned wav2vec 2.0 models are used as input"),
     1, ["引文不在 wiki/papers/2021-pepino-wav2vec2-ser.md 的引文中"])
case("C12", "name_exceptions 內的 wav2vec 2.0 不被誤判（正向）", lambda: build("C12"), 0,
     ["總結判定: [ PASSED ]", "名稱例外清單 (name_exceptions.txt): 1 筆"], forbid_msgs=["'2.0'", "'2'"])
case("C13", "對照：清單移除 wav2vec 2.0 後即被判失敗（證明 C12 靠清單）", lambda: build("C13", names=""), 1,
     ["數字 '2.0' 缺少", "名稱例外清單 (name_exceptions.txt): 0 筆"])
case("C14", "第一個非空行不是 # 標題", mutate("C14", "# 第三頁標題", "## 第三頁標題"), 1,
     ["第一個非空行必須是 `# 標題`"])


def built(case_name, edits=()):
    """建立合法案例 → build_deck.py 產生 HTML → 依序套用 (old, new) 變異。"""
    def _s():
        d = build(case_name)
        run_build(d)
        for old, new in edits:
            replace_in(d / "deck" / "index.html", old, new)
        return d
    return _s


LAST_SECTION_OPEN = '<section class="slide">\n<h1>第附頁標題</h1>'

case("C15", "--html：加入頁內錨點與 data: URI 時外部資源檢查通過，但與 build 輸出不一致而整體失敗", built("C15", [
    ("<h1>第一頁標題</h1>", '<h1>第一頁標題</h1><a href="#deck">回首頁</a><img src="data:image/png;base64,AAAA" alt="">'),
]), 1, ["無外部資源", "投影片數 11 與 slides.md 相同", "與 build_deck.py 輸出不一致", "HTML 投影片標記方式"],
     forbid_msgs=["含外部資源"], html=True)
case("C16", "--html 含外部 https 資源失敗", built("C16", [
    ("<script>", '<script src="https://cdn.example.com/x.js"></script><script>'),
]), 1, ["含外部資源", "https://cdn.example.com/x.js"], html=True)
case("C17", "--html 投影片數不符失敗", built("C17", [
    (LAST_SECTION_OPEN, '<div class="note">\n<h1>第附頁標題</h1>'),
]), 1, ["投影片數不符（HTML 10 張，slides.md 11 頁）"], html=True)
case("C18", "--html CSS @import 失敗", built("C18", [
    ("<style>", "<style>@import url(https://fonts.example.com/a.css);"),
]), 1, ["含外部資源", "@import"], html=True)
case("C19", "沒有 deck/slides.md 為「無法判斷」", lambda: build("C19", no_slides=True), 2,
     ["總結判定: [ 無法判斷 ]", "找不到 deck/slides.md"])

# ---------- 新增：標題數字、HTML 內容比對、build_deck.py ----------
case("C20", "標題含數字失敗", mutate("C20", "# 第三頁標題", "# 準確率 99.9%"), 1,
     ["標題不得含數字，數字請放在內文並附標籤與來源"])
case("C21", "標題含全形數字失敗", mutate("C21", "# 第三頁標題", "# 第３頁標題"), 1,
     ["標題不得含數字"])
case("C22", "HTML 多出 slides.md 沒有的數字失敗", built("C22", [
    ("<h1>第一頁標題</h1>", "<h1>第一頁標題</h1>\n<p>UAR 99.9% 遠勝所有方法</p>"),
]), 1, ["HTML deck/index.html 第 1 張: 數字 99.9 不在 slides.md 第 1 頁原文中"], html=True)
case("C23", "HTML 標題與 slides.md 不同失敗", built("C23", [
    ("<h1>第二頁標題</h1>", "<h1>第二頁大標題</h1>"),
]), 1, ["HTML deck/index.html 第 2 張: 標題與 slides.md 不同"], html=True)
case("C24", "build_deck.py 由合法 slides.md 產生的 HTML 經 --html 通過（正向）", built("C24"), 0,
     ["總結判定: [ PASSED ]", "投影片數 11 與 slides.md 相同", "第 11 張: 標題「第附頁標題」與 slides.md 相同"],
     html=True)


case("C28", "HTML 加入不含數字的文字「本方法是目前最佳」失敗", built("C28", [
    ("<h1>第一頁標題</h1>", "<h1>第一頁標題</h1>\n<p>本方法是目前最佳</p>"),
]), 1, ["與 build_deck.py 輸出不一致", "本方法是目前最佳", "第 1 張: 所有數字皆出現在 slides.md 第 1 頁原文"],
     html=True)
case("C29", "build 後未改動的 HTML 通過，且逐位元組一致檢查列為通過", built("C29"), 0,
     ["與 build_deck.py 由 slides.md 重新產生的輸出逐位元組相同", "總結判定: [ PASSED ]"], html=True)


def _crlf():
    d = build("C30")
    run_build(d)
    p = d / "deck" / "index.html"
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    if b"\r\n" not in p.read_bytes():
        raise AssertionError("變異無效：換行未改成 CRLF")
    return d


case("C30", "HTML 換行改為 CRLF 仍視為一致（比較前統一換行）", _crlf, 0,
     ["逐位元組相同", "總結判定: [ PASSED ]"], html=True)


def extra_case(name, desc, fn):
    try:
        ok, detail = fn()
    except AssertionError as e:
        ok, detail = False, str(e)
    results.append((name, desc, "—", "—", ok, detail))


def _deterministic():
    d = build("C25")
    first = (run_build(d), (d / "deck" / "index.html").read_bytes())
    second = (run_build(d), (d / "deck" / "index.html").read_bytes())
    same = first[1] == second[1]
    return same, f"兩次輸出位元組{'完全相同' if same else '不同'}（{len(first[1])} bytes）"


def _no_http():
    d = build("C26")
    out = run_build(d)
    hits = [w for w in ("http://", "https://", "http", "https") if w in out.lower()]
    return (not hits), ("輸出不含 http/https" if not hits else f"輸出含 {hits}")


def _content_kept():
    """格式轉換不得增刪內容：每頁 slides.md 的數字與標題都在 HTML 中（由 check_deck 的內容比對反向確認）。"""
    d = build("C27")
    out = run_build(d)
    needles = ["67.2 [本文]", "60.7 [引述]", "(p. 3, Table 1)", "〔來源：2021-pepino-wav2vec2-ser〕", "wav2vec 2.0"]
    missing = [n for n in needles if n not in out]
    links = "[[" in out
    return (not missing and not links), ("內容與頁碼原樣保留，[[slug]] 已轉為純文字標記"
                                         if not missing and not links else f"缺少 {missing}；殘留 [[ ]]: {links}")


extra_case("C25", "build_deck.py 決定性：同一輸入 build 兩次輸出完全相同", _deterministic)
extra_case("C26", "build_deck.py 輸出不含 http/https", _no_http)
extra_case("C27", "build_deck.py 只做格式轉換：數字、標籤、頁碼原樣保留，[[slug]] 轉為〔來源：slug〕", _content_kept)

# ------------------------------------------------------------------
print("=" * 100)
print("        check_deck.py 案例測試 (scripts/test_check_deck.py)")
print("=" * 100)
print("| 案例 | 說明 | 預期結束碼 | 預期訊息 | 結果 | 實際 |")
print("| :--- | :--- | :--- | :--- | :--- | :--- |")
for name, desc, code, msgs, ok, detail in results:
    print(f"| {name} | {desc} | {code} | {msgs} | {'PASS' if ok else 'FAIL'} | {detail} |")
fails = sum(1 for r in results if not r[4])
print("=" * 100)
print(f"總結: 共 {len(results)} 案，通過 {len(results) - fails} 案，失敗 {fails} 案")
print("=" * 100)
sys.exit(1 if fails else 0)
