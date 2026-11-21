#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/test_normalization.py - check_numbers.py 比對函式單元測試
以人工構造的 PDF 頁面文字（dict: 頁碼 -> 文字）直接呼叫 check_numbers 的函式，
不讀取任何真實 PDF、不寫入正式 wiki。名稱清單測試檔寫在 <專案>/temp/ 下（已 gitignore）。
任一測試失敗結束碼為 1。
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import check_numbers as cn  # noqa: E402
from check import WikiChecker  # noqa: E402

results = []


def check(name, actual, expected):
    ok = actual == expected
    results.append((name, expected, actual, ok))


# ------------------------------------------------------------------
# 1. 跨行斷詞 se\ngmented（真實 FAU Aibo p. 2 抽字格式）
# ------------------------------------------------------------------
page_seg = {2: "The speech data were\nse\ngmented automatically into speech ﬁles (‘turns’)"}
q = "The speech data were segmented automatically into speech files"
check("se\\ngmented：第一階段正規化單獨不吻合",
      cn.normalize_text(q) in cn.normalize_text(page_seg[2]), False)
check("se\\ngmented：完整比對經第二階段寬鬆比對吻合",
      cn.match_quote_in_pages(q, page_seg, 2, 2), (True, "寬鬆比對: 移除所有空白與連字號"))
check("se\\ngmented：改字 (fragmented) 必須不吻合",
      cn.match_quote_in_pages(q.replace("segmented", "fragmented"), page_seg, 2, 2)[0], False)

# ------------------------------------------------------------------
# 2. ﬁ 連字（wiki 寫普通 fi）
# ------------------------------------------------------------------
page_lig = {1: "made available for scientiﬁc use; in the licensing"}
check("ﬁ 連字：wiki 'scientific' 與 PDF 'scientiﬁc' 第一階段即吻合",
      cn.match_quote_in_pages("for scientific use", page_lig, 1, 1), (True, ""))
check("ﬁ 連字：未正規化時原字串確實不相等（證明靠正規化）",
      "scientific" in page_lig[1], False)

# ------------------------------------------------------------------
# 3. 51 % 與 51%
# ------------------------------------------------------------------
check("51 %（PDF 有空格）可吻合 wiki 51",
      cn.find_number_in_pages("51", {1: "a rate of 51 % was"}, 1, 1), 1)
check("51%（PDF 無空格）可吻合 wiki 51",
      cn.find_number_in_pages("51", {1: "a rate of 51% was"}, 1, 1), 1)
check("wiki 51% 寫法（含 %）可吻合 PDF 51 %",
      cn.find_number_in_pages("51%", {1: "a rate of 51 % was"}, 1, 1), 1)

# ------------------------------------------------------------------
# 4. 千分位 1,102 與 1102
# ------------------------------------------------------------------
check("PDF 1,102 可吻合 wiki 1102",
      cn.find_number_in_pages("1102", {1: "a total of 1,102 videos"}, 1, 1), 1)
check("PDF 1102 可吻合 wiki 1102",
      cn.find_number_in_pages("1102", {1: "a total of 1102 videos"}, 1, 1), 1)
check("PDF 1,102 不可讓 wiki 102 吻合（不得當子字串）",
      cn.find_number_in_pages("102", {1: "a total of 1,102 videos"}, 1, 1), None)

# ------------------------------------------------------------------
# 5. 句尾 62.3.
# ------------------------------------------------------------------
check("PDF 句尾 'was 62.3.' 可吻合 wiki 62.3",
      cn.find_number_in_pages("62.3", {1: "The UAR was 62.3. Next"}, 1, 1), 1)
check("PDF 62.31 不可吻合 wiki 62.3（後接數字）",
      cn.find_number_in_pages("62.3", {1: "The UAR was 62.31 here"}, 1, 1), None)
check("PDF 62.3.1 不可吻合 wiki 62.3（後接小數點加數字）",
      cn.find_number_in_pages("62.3", {1: "see 62.3.1 here"}, 1, 1), None)
check("PDF 62.3 不可吻合 wiki 62（後接小數點加數字）",
      cn.find_number_in_pages("62", {1: "The UAR was 62.3 here"}, 1, 1), None)
check("PDF 0.5 不可吻合 wiki 5（前接數字加小數點）",
      cn.find_number_in_pages("5", {1: "kappa 0.5 here"}, 1, 1), None)

# ------------------------------------------------------------------
# 6. (pp. 1–2) 數字在第 2 頁
# ------------------------------------------------------------------
pages_12 = {1: "page one has no such number", 2: "page two reports 868 turns"}
check("parse_page_cite('(pp. 1–2)') -> (1, 2)", cn.parse_page_cite("(pp. 1–2)"), (1, 2))
check("(pp. 1–2)：數字 868 在第 2 頁 -> 找到於 p. 2",
      cn.find_number_in_pages("868", pages_12, 1, 2), 2)
check("(p. 1)：數字 868 只查第 1 頁 -> 找不到",
      cn.find_number_in_pages("868", pages_12, 1, 1), None)

# ------------------------------------------------------------------
# 7. wav2vec 2.0 名稱例外：在清單內／不在清單內
# ------------------------------------------------------------------
tmp_dir = PROJECT_ROOT / "temp" / "unit_tests"
tmp_dir.mkdir(parents=True, exist_ok=True)
names_file = tmp_dir / "name_exceptions.txt"
names_file.write_text("# 測試用名稱清單（臨時檔）\nwav2vec 2.0\n", encoding="utf-8")
names_in = cn.load_name_exceptions(names_file)
check("load_name_exceptions 讀到 ['wav2vec 2.0']（略過 # 註解）", names_in, ["wav2vec 2.0"])

line = "本研究使用 wav2vec 2.0 模型，UAR 63.4% [本文] (p. 3, Table 2)。"
tagged_in, untagged_in = cn.scan_plain_line(line, True, names_in)
check("名稱在清單內：標註數字只有 63.4", [t["num"] for t in tagged_in], ["63.4"])
check("名稱在清單內：無孤立數字", untagged_in, [])

tagged_out, untagged_out = cn.scan_plain_line(line, True, [])
check("名稱不在清單內：標註數字仍只有 63.4", [t["num"] for t in tagged_out], ["63.4"])
check("名稱不在清單內：wav2vec 的 2（緊鄰英文字，需提示）與 2.0 皆為孤立數字",
      untagged_out, [("2", True), ("2.0", False)])
check("名稱精確比對：'Wav2Vec 2.0'（大小寫不同）不遮蔽",
      cn.scan_plain_line("使用 Wav2Vec 2.0 模型", True, names_in)[1], [("2", True), ("2.0", False)])
check("名稱邊界：'wav2vec 2.01' 不被 'wav2vec 2.0' 遮蔽",
      [n for n, _ in cn.scan_plain_line("使用 wav2vec 2.01 模型", True, names_in)[1]], ["2", "2.01"])
check("連字號提示：'10-fold' 的 10 需提示",
      cn.scan_plain_line("採用 10-fold 交叉驗證", True, [])[1], [("10", True)])

# ------------------------------------------------------------------
# 8. 原始行號（HTML 註解跨行 + frontmatter）
# ------------------------------------------------------------------
content = "---\na: 1\nb: 2\nc: 3\nd: 4\ne: 5\nf: 6\n---\n<!-- x\n123\n-->\n文字\n捏造 777\n"
lines = cn.prepare_lines(content)
check("prepare_lines：第 13 行仍為原始第 13 行", lines[12], "捏造 777")
check("prepare_lines：frontmatter 與跨行註解內數字被清空",
      any(ch.isdigit() for ln in lines[:11] for ch in ln), False)

# ------------------------------------------------------------------
# 9. check.py frontmatter 行尾註解剝除
# ------------------------------------------------------------------
check("strip_inline_comment：'\"\" # 必填' -> '\"\"'", WikiChecker.strip_inline_comment('"" # 必填'), '""')
check("strip_inline_comment：引號內 # 保留", WikiChecker.strip_inline_comment('"a # b" # c'), '"a # b"')
check("strip_inline_comment：method # 註解 -> method", WikiChecker.strip_inline_comment("method # 可選"), "method")

# ------------------------------------------------------------------
# 10. 引文只有 "¨"（去除變音符號後為空字串）不得吻合
# ------------------------------------------------------------------
page_noth = {1: "A. Batliner, S. Steidl, E. N¨oth"}
check("引文只有 '¨'：不得吻合", cn.match_quote_in_pages("¨", page_noth, 1, 1), (False, ""))
check("引文只有 '̈'（結合用分音符）：不得吻合", cn.match_quote_in_pages("̈", page_noth, 1, 1), (False, ""))
check("對照：引文 'E. Nöth' 仍經變音符號寬鬆比對吻合",
      cn.match_quote_in_pages("E. Nöth", page_noth, 1, 1), (True, "寬鬆比對: 變音符號分離"))

# ------------------------------------------------------------------
# 11. 專案路徑本身含 papers 資料夾時，實體頁不得被當成論文頁
# ------------------------------------------------------------------
fake_root = PROJECT_ROOT / "temp" / "unit_tests" / "papers" / "proj"
ent_path = fake_root / "wiki" / "entities" / "test-dataset.md"
paper_path = fake_root / "wiki" / "papers" / "2008-fau-aibo.md"
nc = cn.NumberChecker(fake_root)
check("對照：舊判斷法 'papers' in 完整路徑 會誤判實體頁", "papers" in ent_path.parts, True)
check("is_paper_page(實體頁) -> False", nc.is_paper_page(ent_path), False)
check("is_paper_page(論文頁) -> True", nc.is_paper_page(paper_path), True)
check("find_target_pdf(實體頁, 無 slug) -> None", nc.find_target_pdf(ent_path), None)
check("find_target_pdf(實體頁, slug) -> raw/<slug>.pdf",
      nc.find_target_pdf(ent_path, "2008-fau-aibo"), fake_root.resolve() / "raw" / "2008-fau-aibo.pdf")
check("find_target_pdf(論文頁) -> raw/<檔名>.pdf",
      nc.find_target_pdf(paper_path), fake_root.resolve() / "raw" / "2008-fau-aibo.pdf")

# ------------------------------------------------------------------
# 輸出
# ------------------------------------------------------------------
print("=" * 100)
print("        check_numbers / check 比對函式單元測試 (scripts/test_normalization.py)")
print("=" * 100)
for i, (name, exp, act, ok) in enumerate(results, 1):
    print(f"[{'PASS' if ok else 'FAIL'}] {i:02d}. {name}")
    if not ok:
        print(f"         預期: {exp!r}")
        print(f"         實際: {act!r}")
fails = sum(1 for r in results if not r[3])
print("=" * 100)
print(f"總結: 共 {len(results)} 項，通過 {len(results) - fails} 項，失敗 {fails} 項")
print("=" * 100)
sys.exit(1 if fails else 0)
