#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/run_mutation_tests.py - 變異測試（Mutation Testing）與正規化驗證套件
依據 AGENTS.md 第 11 節與使用者修訂規範實作：
1. 嚴格在 temp/mutation_runs/ 臨時副本執行，絕不污染正式 Wiki；每個副本先刪除複製來的舊 temp/ 報告。
2. 先確認未突變之基準版本 (Valid fixture) 通過；失敗則整體中止。
3. 每個變異都必須真的改到檔案（replace 找不到原字串即視為案例無效並失敗），不得有空變異。
4. 每個案例比對預期訊息（可多條，全部須出現）與不應出現的訊息。
5. 完整表格（預期訊息與實際訊息不截斷）同時輸出至終端機與 <專案>/temp/mutation-report.txt（UTF-8）。
"""

import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VALID_FIXTURE = PROJECT_ROOT / "scripts" / "fixtures" / "valid"
TEMPLATE_PAPER = PROJECT_ROOT / "templates" / "paper-template.md"
TEMP_BASE = PROJECT_ROOT / "temp" / "mutation_runs"
REPORT_FILE = PROJECT_ROOT / "temp" / "mutation-report.txt"

QUOTE_P1 = '> "We report on a thoroughly processed and annotated German emotional speech database" (p. 1)'
MOTIVATION = "## 研究動機與欲解決問題\n測試研究動機與背景說明。"


class MutationNotApplied(Exception):
    pass


# ==============================================================================
# 共用工具
# ==============================================================================

def paper(d: Path) -> Path:
    return d / "wiki" / "papers" / "2008-fau-aibo.md"


def entity(d: Path) -> Path:
    return d / "wiki" / "entities" / "test-dataset.md"


def replace_in(path: Path, old: str, new: str):
    """替換 old -> new；old 不存在即拋出例外（防止空變異）。"""
    content = path.read_text(encoding="utf-8")
    if old not in content:
        raise MutationNotApplied(f"{path.name} 中找不到要替換的字串: {old[:60]!r}")
    mutated = content.replace(old, new)
    if mutated == content:
        raise MutationNotApplied(f"{path.name} 替換前後內容相同（無效變異）: {old[:60]!r}")
    path.write_text(mutated, encoding="utf-8")


def append_to(path: Path, text: str):
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def add_extra_pdf(d: Path):
    src = d / "raw" / "2008-fau-aibo.pdf"
    shutil.copyfile(src, d / "raw" / "2099-extra-test.pdf")


def write_paper_8line_frontmatter(d: Path):
    """frontmatter 剛好 8 行（第 1–8 行），第 13 行為捏造數字。"""
    lines = [
        "---",                                        # 1
        'title: "Test FAU Aibo"',                     # 2
        'authors: ["Test Author"]',                   # 3
        "year: 2008",                                 # 4
        "type: dataset",                              # 5
        'pdf: "raw/2008-fau-aibo.pdf"',               # 6
        'one_sentence_summary: "測試用摘要。"',        # 7
        "---",                                        # 8
        "",                                           # 9
        "# Test FAU Aibo",                            # 10
        "",                                           # 11
        "## 核心數據與成果",                           # 12
        "捏造 77777 位兒童 [本文] (p. 1)。",           # 13
        "",
        "## 提及實體清單",
        "- [[test-dataset]]",
        "",
        "## 矛盾／待釐清",
        "無",
        "",
    ]
    paper(d).write_text("\n".join(lines), encoding="utf-8")


def write_temp_scripts_file(d: Path, name: str, body: str):
    """只寫入臨時副本的 scripts/，絕不碰正式 scripts/ 內的使用者專用清單。"""
    sd = d / "scripts"
    sd.mkdir(parents=True, exist_ok=True)
    (sd / name).write_text(body, encoding="utf-8")


# ==============================================================================
# 變異函式
# ==============================================================================

def m_change_number(d):
    replace_in(paper(d), "51 位兒童 [本文] (p. 1)", "99999 位兒童 [本文] (p. 1)")

def m_broken_link(d):
    replace_in(paper(d), "[[test-dataset]]", "[[non-existent-entity-link]]")

def m_remove_page(d):
    replace_in(paper(d), "共計 51 位兒童 [本文] (p. 1) 與 9.2 小時 [本文] (p. 1) 語音。", "共計 51 位兒童與 9.2 小時語音。")

def m_page_overflow(d):
    replace_in(paper(d), "(p. 1)", "(p. 99)")

def m_future_log_date(d):
    replace_in(d / "wiki" / "log.md", "[2026-11-20]", "[2099-12-31]")

def m_missing_contradictions(d):
    replace_in(paper(d), "## 矛盾／待釐清\n無", "")

def m_missing_tag_51(d):
    replace_in(paper(d), "51 位兒童 [本文] (p. 1)", "51 位兒童 (p. 1)")

def m_shared_tag(d):
    replace_in(paper(d), "共計 51 位兒童 [本文] (p. 1) 與 9.2 小時 [本文] (p. 1) 語音。", "共計 51 位兒童、9.2 小時 [本文] (p. 1) 語音。")

def m_extra_pdf(d):
    add_extra_pdf(d)

def m_inconsistent_sources(d):
    replace_in(paper(d), "- [[test-dataset]]", "- test-dataset (純文字未連結)")

def m_fake_decimal(d):
    replace_in(paper(d), "9.2 小時 [本文] (p. 1)", "99.9 小時 [本文] (p. 1)")

def m_num_after_word(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "實驗模型 model 999 評測表現。")

def m_fake_quote(d):
    replace_in(paper(d), QUOTE_P1, '> "This is a completely fabricated quote that never exists in the paper" (p. 1)')

def m_non_paper_missing_slug(d):
    replace_in(entity(d), "[[2008-fau-aibo]] (p. 1)", "(p. 1)")

def m_missing_tag_10fold(d):
    replace_in(paper(d), "## 研究動機與欲解決問題\n", "## 研究動機與欲解決問題\n採用 10-fold cross-validation 評測方式。\n")

def m_unit_word_positive(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n受試者共 51 位兒童 [本文] (p. 1)。")

def m_valid_fig_citation(d):
    replace_in(paper(d), "(p. 1)", "(p. 1, Fig. 1)")

def m_norm_nfkc(d):
    # wiki 端寫普通 "scientific"；PDF p. 1 為連字 "scientiﬁc"，須靠 NFKC 才能吻合
    replace_in(paper(d), QUOTE_P1, '> "made available for scientific use" (p. 1)')

def m_norm_soft_hyphen(d):
    replace_in(paper(d), "emotional", "emo­tional")

def m_norm_dehyphen(d):
    # PDF p. 1: "‘natural-\nistic’"（行尾連字號斷詞）
    replace_in(paper(d), QUOTE_P1, '> "naturalistic" (p. 1)')

def m_norm_spaces_case(d):
    replace_in(paper(d), QUOTE_P1, '> "WE   REPORT   ON   A    THOROUGHLY   PROCESSED" (p. 1)')

def m_norm_diacritics(d):
    replace_in(paper(d), QUOTE_P1, '> "E. Nöth" (p. 1)')

SEGMENTED_QUOTE = "The speech data were segmented automatically into speech files"

def m_norm_segmented(d):
    # PDF p. 2: "The speech data were\nse\ngmented automatically into speech ﬁles"（無連字號的跨行斷詞）
    replace_in(paper(d), QUOTE_P1, f'> "{SEGMENTED_QUOTE}" (p. 2)')

def m_norm_segmented_altered(d):
    # 同一句改一個字，必須失敗（確認第二階段寬鬆比對不會放過改字）
    replace_in(paper(d), QUOTE_P1, f'> "{SEGMENTED_QUOTE.replace("segmented", "fragmented")}" (p. 2)')

def m_line_number_13(d):
    write_paper_8line_frontmatter(d)

def m_waiver_original_line(d):
    write_paper_8line_frontmatter(d)
    write_temp_scripts_file(d, "number_waivers.txt", "2008-fau-aibo.md | 13 | 77777 | 變異測試 | 2026-11-20\n")

def m_waiver_body_line(d):
    # 若誤用「去掉 frontmatter 後」的行號（13 - 8 = 5），豁免不得生效
    write_paper_8line_frontmatter(d)
    write_temp_scripts_file(d, "number_waivers.txt", "2008-fau-aibo.md | 5 | 77777 | 變異測試 | 2026-11-20\n")

def m_html_comment_numbers(d):
    # 第 21 行為「## 研究動機與欲解決問題」；插入第 22–24 行跨行註解（含 12345），第 25 行為捏造數字
    replace_in(paper(d), "## 研究動機與欲解決問題\n",
               "## 研究動機與欲解決問題\n<!-- 註解開始\n內含數字 12345 不應被檢查\n註解結束 -->\n捏造 88888 位兒童。\n")

def m_heading_inside_comment(d):
    replace_in(paper(d), "## 矛盾／待釐清\n無", "<!--\n## 矛盾／待釐清\n無\n-->")

def m_template_empty_summary(d):
    shutil.copyfile(TEMPLATE_PAPER, paper(d))

def m_index_broken_link(d):
    append_to(d / "wiki" / "index.md", "\n- [[ghost-page]]｜ghost\n")

def m_log_broken_link(d):
    append_to(d / "wiki" / "log.md", "- [[ghost-log-page]]\n")

def m_orphan_only_index_log(d):
    (d / "wiki" / "entities" / "orphan-entity.md").write_text(
        '---\nname: "orphan-entity"\ntype: dataset\nsources: ["2008-fau-aibo"]\ncore_contribution_of: "2008-fau-aibo"\n---\n\n'
        "# orphan-entity\n\n## 定義\n論文未定義\n\n## 核心屬性與特點\n無\n\n## 在各論文中的應用與實驗表現\n無\n\n## 矛盾／待釐清\n無\n",
        encoding="utf-8")
    replace_in(d / "wiki" / "index.md", "- [[test-dataset]]｜test-dataset", "- [[test-dataset]]｜test-dataset\n- [[orphan-entity]]｜orphan-entity")
    append_to(d / "wiki" / "log.md", "- [[orphan-entity]]\n")

def m_name_hint(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n測試模型 wav2vec2 表現。")

def m_name_in_exceptions(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n測試模型 wav2vec2 表現。")
    write_temp_scripts_file(d, "name_exceptions.txt", "# 臨時副本測試用\nwav2vec2\n")

def m_only_indeterminate(d):
    paper(d).unlink()
    entity(d).unlink()

def m_pp_range_positive(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n另有 868 個 [本文] (pp. 2–3)。")

def m_pp_range_overflow(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n另有 868 個 [本文] (pp. 3–9)。")

def m_real_percent_space(d):
    # PDF p. 3 真實文字為 "868 A (21.7 %)"
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\nA 類占 21.7% [本文] (p. 3)。")

def m_real_sentence_end(d):
    # PDF p. 2 真實文字為 "weighted kappa is 0.59."
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\nweighted kappa 為 0.59 [本文] (p. 2)。")

# ---- 第二輪新增 ----
CONTRIB_BLOCK = "## 核心貢獻與作者觀點\n- [作者聲稱] 提供兒童語音情緒資料庫 (p. 1)\n"

def m_contradictions_blank_then_heading(d):
    # 「## 矛盾／待釐清」後空一行就接下一個 ##，本節實際為空
    replace_in(paper(d), "## 矛盾／待釐清\n無", "## 矛盾／待釐清\n\n## 附錄\n附錄內容。")

def m_contrib_empty_next_has_bullets(d):
    # 核心貢獻為空、下一節（局限性）有未加標籤的條列，不得算到核心貢獻頭上
    replace_in(paper(d), CONTRIB_BLOCK, "## 核心貢獻與作者觀點\n")
    replace_in(paper(d), "## 論文提及之局限性\n論文未提及", "## 論文提及之局限性\n- 樣本僅限德語兒童")

def m_survey_methods_blank_then_heading(d):
    # 綜述的「方法與架構」為空，下一節才寫不適用，不得算作本節已標註
    replace_in(paper(d), "type: dataset", "type: survey")
    replace_in(paper(d), "## 方法與架構\n資料蒐集與標註流程說明。", "## 方法與架構\n\n## 實驗設定\n不適用（綜述無自研實驗）")

def m_bullet_dash_number(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n- 88888 位兒童參與 (p. 1)")

def m_bullet_star_number(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n* 99.9 小時的語音")

def m_ordered_list_number(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n1. 77777 位受試者")

def m_summary_has_digit(d):
    replace_in(paper(d), 'one_sentence_summary: "這是測試用假資料的一句話摘要。"',
               'one_sentence_summary: "收錄 51 位兒童語音的測試資料庫。"')

def m_quote_then_untagged_number(d):
    replace_in(paper(d), QUOTE_P1, QUOTE_P1 + " 作者共收錄 66666 位兒童。")

def m_quote_then_tagged_fake_number(d):
    replace_in(paper(d), QUOTE_P1, QUOTE_P1 + " 另有 66666 位兒童 [本文] (p. 1)。")

def m_nopypdf_valid_line(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n受試者共 51 位兒童 [本文] (p. 1)。")

def m_nopypdf_untagged(d):
    replace_in(paper(d), MOTIVATION, MOTIVATION + "\n另有 66666 位兒童參與。")

QUOTE_ALT = "made available for scientific use"  # PDF p. 1 真實文字（連字 ﬁ）

def make_quote_cite(cite):
    def fn(d):
        replace_in(paper(d), QUOTE_P1, f'> "{QUOTE_ALT}" {cite}')
    return fn

def make_plain_cite(cite):
    def fn(d):
        replace_in(paper(d), MOTIVATION, MOTIVATION + f"\n另有 51 位兒童 [本文] {cite}。")
    return fn


# ==============================================================================
# 測試案例清單
# expected: 字串或字串清單（全部須出現）；unexpected: 不得出現的字串清單
# ==============================================================================
NUM = "check_numbers.py"
CHK = "check.py"
FAIL_TAG = "缺少 [本文]/[引述] 標籤或未在同一句/格附帶頁碼"
PASS_SUMMARY = "總結判定: [ PASSED ]"

MUTATION_CASES = [
    {"id": "1", "name": "改數字（捏造不在該頁的數字 99999）", "script": NUM, "neg": True,
     "expected": "數字 99999 在 2008-fau-aibo.pdf p. 1 查無完全吻合", "fn": m_change_number},
    {"id": "2", "name": "刪掉連結（指向不存在的實體頁）", "script": CHK, "neg": True,
     "expected": "失效連結 [[non-existent-entity-link]] (目標檔案不存在)", "fn": m_broken_link},
    {"id": "3", "name": "拿掉頁碼（正文數字未附頁碼）", "script": NUM, "neg": True,
     "expected": f"數字 '51' {FAIL_TAG}", "fn": m_remove_page},
    {"id": "4", "name": "頁碼超過總頁數（FAU Aibo 僅 4 頁寫 p. 99）", "script": NUM, "neg": True,
     "expected": "超過 2008-fau-aibo.pdf 總頁數 (4)", "fn": m_page_overflow},
    {"id": "5", "name": "log 日期在未來（寫 2099-12-31）", "script": CHK, "neg": True,
     "expected": "log.md 日期在未來: 2099-12-31 (不可晚於今天", "fn": m_future_log_date},
    {"id": "6", "name": "缺「矛盾／待釐清」標題", "script": CHK, "neg": True,
     "expected": "缺少必填逐字標題 '## 矛盾／待釐清'", "fn": m_missing_contradictions},
    {"id": "7", "name": "缺標籤（51 位兒童 (p. 1)）", "script": NUM, "neg": True,
     "expected": f"數字 '51' {FAIL_TAG}", "fn": m_missing_tag_51},
    {"id": "8", "name": "共用標籤（51 位兒童、9.2 小時 [本文] (p. 1)）", "script": NUM, "neg": True,
     "expected": f"數字 '51' {FAIL_TAG}", "fn": m_shared_tag},
    {"id": "9", "name": "--final 模式：raw/ 多一份 PDF 沒有論文頁", "script": CHK, "args": ["--final"], "neg": True,
     "expected": "raw/2099-extra-test.pdf 尚未完成 Ingest (缺少 wiki/papers/2099-extra-test.md)", "fn": m_extra_pdf},
    {"id": "10", "name": "實體 sources 與論文頁連結不一致", "script": CHK, "neg": True,
     "expected": "實體 wiki/entities/test-dataset.md 的 sources 包含 '2008-fau-aibo'，但論文 wiki/papers/2008-fau-aibo.md 的「提及實體清單」未包含 [[test-dataset]]",
     "fn": m_inconsistent_sources},
    {"id": "11", "name": "捏造小數 99.9（小數未被當成章節遮蔽）", "script": NUM, "neg": True,
     "expected": "數字 99.9 在 2008-fau-aibo.pdf p. 1 查無完全吻合", "fn": m_fake_decimal},
    {"id": "12", "name": "英文字後的捏造數字（model 999）", "script": NUM, "neg": True,
     "expected": f"數字 '999' {FAIL_TAG}", "fn": m_num_after_word},
    {"id": "13", "name": "捏造引文（不在該頁的英文句子）", "script": NUM, "neg": True,
     "expected": "引述在 2008-fau-aibo.pdf p. 1 查無吻合文字", "fn": m_fake_quote},
    {"id": "14", "name": "非論文頁缺 slug（實體頁引註缺少 [[slug]]）", "script": NUM, "neg": True,
     "expected": "非論文頁之引用必須加上來源 [[slug]] (p. N)", "fn": m_non_paper_missing_slug},
    {"id": "15", "name": "10-fold 缺標籤（且應附名稱提示）", "script": NUM, "neg": True,
     "expected": [f"數字 '10' {FAIL_TAG}", "請使用者將名稱加入 scripts/name_exceptions.txt"], "fn": m_missing_tag_10fold},
    {"id": "16", "name": "正向：新增一行「51 位兒童 [本文] (p. 1)」必須通過", "script": NUM, "neg": False,
     "expected": PASS_SUMMARY, "fn": m_unit_word_positive},
    {"id": "17", "name": "正向：合法 (p. 1, Fig. 1) 引註通過", "script": NUM, "neg": False,
     "expected": PASS_SUMMARY, "fn": m_valid_fig_citation},
    {"id": "18", "name": "正規化：wiki 普通 scientific 對 PDF 連字 scientiﬁc（NFKC）", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "2008-fau-aibo.md:23: 引述在 2008-fau-aibo.pdf p. 1 吻合"],
     "unexpected": ["寬鬆比對"], "fn": m_norm_nfkc},
    {"id": "19", "name": "正規化：軟連字號移除 (emo\\u00adtional)", "script": NUM, "neg": False,
     "expected": PASS_SUMMARY, "fn": m_norm_soft_hyphen},
    {"id": "20", "name": "正規化：行尾連字號斷詞合併 (natural-\\nistic)", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "2008-fau-aibo.md:23: 引述在 2008-fau-aibo.pdf p. 1 吻合"],
     "unexpected": ["寬鬆比對"], "fn": m_norm_dehyphen},
    {"id": "21", "name": "正規化：多重空白壓縮與不分大小寫比對", "script": NUM, "neg": False,
     "expected": PASS_SUMMARY, "fn": m_norm_spaces_case},
    {"id": "22", "name": "正規化：變音符號分離寬鬆比對 (Nöth / N¨oth)", "script": NUM, "neg": False,
     "expected": PASS_SUMMARY, "fn": m_norm_diacritics},
    {"id": "23", "name": "正規化：無連字號跨行斷詞 se\\ngmented（PDF p. 2）改變前：原句通過", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "引述在 2008-fau-aibo.pdf p. 2 吻合 (寬鬆比對: 移除所有空白與連字號)"],
     "fn": m_norm_segmented},
    {"id": "23b", "name": "正規化：同句改變後（segmented→fragmented）必須失敗", "script": NUM, "neg": True,
     "expected": "引述在 2008-fau-aibo.pdf p. 2 查無吻合文字", "fn": m_norm_segmented_altered},
    # 原案例 24（空的 pass 變異，未真正產生 51 %）已刪除，改由 scripts/test_normalization.py 負責
    {"id": "25", "name": "非 --final：raw/ 多一份 PDF 沒有論文頁，check.py 結束碼為 0", "script": CHK, "neg": False,
     "expected": ["[待 Ingest]: raw/2099-extra-test.pdf 尚未完成 Ingest", "總結: 通過 10 項，失敗 0 項"], "fn": m_extra_pdf},
    {"id": "26", "name": "行號：frontmatter 8 行，第 13 行捏造數字，報告須寫 :13", "script": NUM, "neg": True,
     "expected": "2008-fau-aibo.md:13: 數字 77777 在 2008-fau-aibo.pdf p. 1 查無完全吻合", "fn": m_line_number_13},
    {"id": "27", "name": "行號：豁免清單用原始行號 13，豁免生效", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "2008-fau-aibo.md:13: 數字 77777 符合人工例外豁免清單"], "fn": m_waiver_original_line},
    {"id": "27b", "name": "行號：豁免清單誤用去 frontmatter 行號 5，豁免不生效", "script": NUM, "neg": True,
     "expected": "2008-fau-aibo.md:13: 數字 77777 在 2008-fau-aibo.pdf p. 1 查無完全吻合", "fn": m_waiver_body_line},
    {"id": "28", "name": "HTML 註解：跨行註解內數字不檢查，其後捏造數字報原始行號 :25", "script": NUM, "neg": True,
     "expected": f"2008-fau-aibo.md:25: 數字 '88888' {FAIL_TAG}", "unexpected": ["12345"], "fn": m_html_comment_numbers},
    {"id": "29", "name": "HTML 註解：標題只出現在註解內，check.py 視為缺標題", "script": CHK, "neg": True,
     "expected": "wiki/papers/2008-fau-aibo.md: 缺少必填逐字標題 '## 矛盾／待釐清'", "fn": m_heading_inside_comment},
    {"id": "30", "name": "frontmatter：真實 paper-template.md（type 已填、summary 留空）項目 3 失敗", "script": CHK, "neg": True,
     "expected": ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: frontmatter 必填欄位 'one_sentence_summary' 為空"],
     "unexpected": ["frontmatter type"], "fn": m_template_empty_summary},
    {"id": "31", "name": "連結：index.md 內失效連結判失敗", "script": CHK, "neg": True,
     "expected": "wiki/index.md: 失效連結 [[ghost-page]] (目標檔案不存在)", "fn": m_index_broken_link},
    {"id": "31b", "name": "連結：log.md 內失效連結判失敗", "script": CHK, "neg": True,
     "expected": "wiki/log.md: 失效連結 [[ghost-log-page]] (目標檔案不存在)", "fn": m_log_broken_link},
    {"id": "32", "name": "連結：只被 index.md／log.md 連入的實體仍為孤兒", "script": CHK, "neg": True,
     "expected": "wiki/entities/orphan-entity.md: 孤兒實體頁", "unexpected": ["失效連結"], "fn": m_orphan_only_index_log},
    {"id": "33", "name": "名稱例外：wav2vec2 未列入清單 -> 失敗並附提示", "script": NUM, "neg": True,
     "expected": [f"數字 '2' {FAIL_TAG}", "（若為模型／資料集／指標名稱，請使用者將名稱加入 scripts/name_exceptions.txt）"],
     "fn": m_name_hint},
    {"id": "33b", "name": "名稱例外：臨時副本 name_exceptions.txt 列入 wav2vec2 -> 通過", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "名稱例外清單 (name_exceptions.txt): 1 筆"], "fn": m_name_in_exceptions},
    {"id": "34", "name": "總結列：只有無法判斷時顯示「無法判斷」且結束碼非 0", "script": NUM, "neg": True,
     "expected": ["總結判定: [ 無法判斷 ] (失敗數: 0, 無法判斷: 1)"], "unexpected": ["FAILED"], "fn": m_only_indeterminate},
    {"id": "35", "name": "(pp. 2–3)：數字 868 在第 3 頁，通過", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "數字 868 成功於 2008-fau-aibo.pdf p. 3 溯源比對"], "fn": m_pp_range_positive},
    {"id": "36", "name": "(pp. 3–9)：結束頁 9 超過總頁數，失敗", "script": NUM, "neg": True,
     "expected": "數字 868 標註頁碼 pp. 3–9 超過 2008-fau-aibo.pdf 總頁數 (4)", "fn": m_pp_range_overflow},
    {"id": "37", "name": "真實 PDF：wiki 21.7% 對 PDF p. 3 的「21.7 %」", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "數字 21.7 成功於 2008-fau-aibo.pdf p. 3 溯源比對"], "fn": m_real_percent_space},
    {"id": "38", "name": "真實 PDF：wiki 0.59 對 PDF p. 2 句尾「0.59.」", "script": NUM, "neg": False,
     "expected": [PASS_SUMMARY, "數字 0.59 成功於 2008-fau-aibo.pdf p. 2 溯源比對"], "fn": m_real_sentence_end},
    # ---------------- 第二輪新增 ----------------
    {"id": "39", "name": "項目 4：矛盾／待釐清後空一行即接下一個 ##，須判為空白", "script": CHK, "neg": True,
     "expected": ["項目 04: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: '## 矛盾／待釐清' 內容不可為空白"],
     "fn": m_contradictions_blank_then_heading},
    {"id": "40", "name": "項目 9：核心貢獻為空、下一節有未標籤條列，不得誤報", "script": CHK, "neg": False, "ignore_exit": True,
     "expected": "項目 09: [ PASS ]", "unexpected": ["核心貢獻條列未以"], "fn": m_contrib_empty_next_has_bullets},
    {"id": "41", "name": "項目 3：綜述方法與架構為空、下一節寫不適用，仍須失敗", "script": CHK, "neg": True,
     "expected": "wiki/papers/2008-fau-aibo.md (survey): '## 方法與架構' 應標註 '不適用（附理由）'",
     "fn": m_survey_methods_blank_then_heading},
    {"id": "42", "name": "條列行首：- 88888 位兒童參與 (p. 1) 須報缺標籤", "script": NUM, "neg": True,
     "expected": f"2008-fau-aibo.md:23: 數字 '88888' {FAIL_TAG}", "fn": m_bullet_dash_number},
    {"id": "43", "name": "條列行首：* 99.9 小時的語音 須報缺標籤", "script": NUM, "neg": True,
     "expected": f"2008-fau-aibo.md:23: 數字 '99.9' {FAIL_TAG}", "fn": m_bullet_star_number},
    {"id": "44", "name": "有序清單：1. 77777 位受試者 須報缺標籤（編號 1 本身不報）", "script": NUM, "neg": True,
     "expected": f"2008-fau-aibo.md:23: 數字 '77777' {FAIL_TAG}", "unexpected": [f"數字 '1' {FAIL_TAG}"],
     "fn": m_ordered_list_number},
    {"id": "45", "name": "項目 3：one_sentence_summary 含阿拉伯數字須失敗", "script": CHK, "neg": True,
     "expected": ["項目 03: [ FAIL ]", "frontmatter 'one_sentence_summary' 不得含阿拉伯數字 (發現 51"],
     "fn": m_summary_has_digit},
    {"id": "46", "name": "引述行後接自己的話含未標籤捏造數字須失敗（引文本身仍吻合）", "script": NUM, "neg": True,
     "expected": [f"2008-fau-aibo.md:23: 數字 '66666' {FAIL_TAG}", "2008-fau-aibo.md:23: 引述在 2008-fau-aibo.pdf p. 1 吻合"],
     "fn": m_quote_then_untagged_number},
    {"id": "47", "name": "引述行後接自己的話含已標籤捏造數字須失敗", "script": NUM, "neg": True,
     "expected": "2008-fau-aibo.md:23: 數字 66666 在 2008-fau-aibo.pdf p. 1 查無完全吻合", "fn": m_quote_then_tagged_fake_number},
    {"id": "48", "name": "缺 pypdf：合法標註數字 -> 總結「無法判斷」、結束碼非 0", "script": NUM, "runner": "nopypdf", "neg": True,
     "expected": ["總結判定: [ 無法判斷 ]", "缺少 pypdf 套件"], "unexpected": ["FAILED"], "fn": m_nopypdf_valid_line},
    {"id": "49", "name": "缺 pypdf：其他檢查照跑（未標籤數字仍報失敗，並列無法判斷）", "script": NUM, "runner": "nopypdf", "neg": True,
     "expected": [f"數字 '66666' {FAIL_TAG}", "[ 無法判斷項目清單 ]", "缺少 pypdf 套件"], "fn": m_nopypdf_untagged},
]

# 第 9 點：頁碼格式（非法 5 種 × 引述行／一般行；合法 4 種 × 引述行／一般行）
ILLEGAL_CITES = [
    ("(p.1)", "缺空格"),
    ("(pp. 1-2)", "範圍用連字號"),
    ("(p. 1–2)", "單頁寫成範圍"),
    ("(pp. 3, Table 1)", "範圍加 Table"),
    ("(pp. 1–1)", "範圍 N 不小於 M"),
]
LEGAL_CITES = ["(p. 1)", "(p. 1, Table 1)", "(p. 1, Fig. 1)", "(pp. 1–2)"]
_next_id = 50
for _kind, _maker in (("引述行", make_quote_cite), ("一般行", make_plain_cite)):
    for _cite, _why in ILLEGAL_CITES:
        MUTATION_CASES.append({
            "id": str(_next_id), "name": f"頁碼格式非法（{_why}）{_cite} 於{_kind}須失敗", "script": NUM, "neg": True,
            "expected": f"頁碼格式非法: '{_cite}'", "fn": _maker(_cite)})
        _next_id += 1
for _kind, _maker in (("引述行", make_quote_cite), ("一般行", make_plain_cite)):
    for _cite in LEGAL_CITES:
        MUTATION_CASES.append({
            "id": str(_next_id), "name": f"頁碼格式合法 {_cite} 於{_kind}須通過", "script": NUM, "neg": False,
            "expected": PASS_SUMMARY, "unexpected": ["頁碼格式非法"], "fn": _maker(_cite)})
        _next_id += 1

# ==============================================================================
# 第三輪新增：引述行結構（A）與 check.py 必填內容／frontmatter／殘留（B）
# ==============================================================================
QUOTE_TEXT = "We report on a thoroughly processed and annotated German emotional speech database"
ENTITY_QUOTE_LINE = f'> "{QUOTE_TEXT}" [[2008-fau-aibo]] (p. 1)'
EMPTY_HINT = "內容不可為空白（無內容請寫「論文未提及」或「不適用（附理由）」）"

def m_quote_prefix_text(d):
    replace_in(paper(d), QUOTE_P1, f'> 共 88888 位兒童："{QUOTE_TEXT}" (p. 1)')

def m_quote_two_quotes(d):
    replace_in(paper(d), QUOTE_P1, f'> "{QUOTE_TEXT}" (p. 1) 另見 "fabricated english sentence" (p. 1)')

def m_entity_quote_valid_alt(d):
    replace_in(entity(d), ENTITY_QUOTE_LINE, '> "made available for scientific use" [[2008-fau-aibo]] (p. 1)')

def m_empty_motivation(d):
    replace_in(paper(d), MOTIVATION + "\n" + QUOTE_P1 + "\n", "## 研究動機與欲解決問題\n")

def m_empty_methods_dataset(d):
    replace_in(paper(d), "## 方法與架構\n資料蒐集與標註流程說明。", "## 方法與架構\n")

def m_empty_limitations(d):
    replace_in(paper(d), "## 論文提及之局限性\n論文未提及", "## 論文提及之局限性\n")

def m_empty_entity_list(d):
    replace_in(paper(d), "## 提及實體清單\n- [[test-dataset]]", "## 提及實體清單\n")

def m_empty_entity_definition(d):
    replace_in(entity(d), ENTITY_QUOTE_LINE + "\n", "")
    replace_in(entity(d), "中文說明（AI 整理，待核對）：測試用資料集定義說明。", "")

def m_motivation_not_mentioned(d):
    replace_in(paper(d), MOTIVATION + "\n" + QUOTE_P1 + "\n", "## 研究動機與欲解決問題\n論文未提及\n")

def m_methods_not_applicable(d):
    replace_in(paper(d), "## 方法與架構\n資料蒐集與標註流程說明。", "## 方法與架構\n不適用（本測試資料集論文無自研方法）")

def m_paper_template_residue(d):
    replace_in(paper(d), "# Test FAU Aibo", "# {{title}}")

def m_entity_template_residue(d):
    replace_in(entity(d), "# test-dataset", "# {{name}}")

def m_empty_title(d):
    replace_in(paper(d), 'title: "Test FAU Aibo"', 'title: ""')

def m_empty_authors(d):
    replace_in(paper(d), 'authors: ["Test Author"]', 'authors: []')

def m_bad_year(d):
    replace_in(paper(d), "year: 2008", "year: abc")

def m_bad_pdf(d):
    replace_in(paper(d), 'pdf: "raw/2008-fau-aibo.pdf"', 'pdf: "raw/..."')

def m_basic_info_blank(d):
    replace_in(paper(d), "- **發表會議／期刊**：LREC", "- **發表會議／期刊**：")

def m_empty_entity_name(d):
    replace_in(entity(d), 'name: "test-dataset"', 'name: ""')

_ROUND3 = [
    ("引述行：引號前有文字（共 88888 位兒童：\"...\"）須失敗，且引號前數字仍被檢查", NUM, True,
     ["引述行必須以雙引號開頭，引號前不得有其他文字", f"數字 '88888' {FAIL_TAG}"], [], m_quote_prefix_text),
    ("引述行：一行兩段引述須失敗", NUM, True,
     ["一行只能有一段引述，請另起一行"], [], m_quote_two_quotes),
    ("引述行：非論文頁 > \"引文\" [[slug]] (p. 1) 換成另一句真實引文仍須通過", NUM, False,
     [PASS_SUMMARY, "test-dataset.md:12: 引述在 2008-fau-aibo.pdf p. 1 吻合"], ["引述行必須以雙引號開頭", "一行只能有一段引述"],
     m_entity_quote_valid_alt),
    ("必填非空：研究動機為空須失敗", CHK, True,
     ["項目 04: [ FAIL ]", f"wiki/papers/2008-fau-aibo.md: '## 研究動機與欲解決問題' {EMPTY_HINT}"], [], m_empty_motivation),
    ("必填非空：dataset 的方法與架構為空須失敗", CHK, True,
     ["項目 04: [ FAIL ]", f"wiki/papers/2008-fau-aibo.md: '## 方法與架構' {EMPTY_HINT}"], [], m_empty_methods_dataset),
    ("必填非空：局限性為空須失敗", CHK, True,
     ["項目 04: [ FAIL ]", f"wiki/papers/2008-fau-aibo.md: '## 論文提及之局限性' {EMPTY_HINT}"], [], m_empty_limitations),
    ("必填非空：提及實體清單為空須失敗", CHK, True,
     ["項目 04: [ FAIL ]", f"wiki/papers/2008-fau-aibo.md: '## 提及實體清單' {EMPTY_HINT}"], [], m_empty_entity_list),
    ("必填非空：實體頁定義為空須失敗", CHK, True,
     ["項目 04: [ FAIL ]", "wiki/entities/test-dataset.md: '## 定義' 內容不可為空白"], [], m_empty_entity_definition),
    ("必填非空：研究動機寫「論文未提及」須通過", CHK, False,
     ["項目 04: [ PASS ]", "總結: 通過 10 項，失敗 0 項"], [], m_motivation_not_mentioned),
    ("必填非空：dataset 方法與架構寫「不適用（附理由）」須通過", CHK, False,
     ["項目 04: [ PASS ]", "總結: 通過 10 項，失敗 0 項"], [], m_methods_not_applicable),
    ("模板殘留：論文頁含 {{title}} 須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md:11: 含模板殘留"], [], m_paper_template_residue),
    ("模板殘留：實體頁含 {{name}} 須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/entities/test-dataset.md:9: 含模板殘留"], [], m_entity_template_residue),
    ("frontmatter：title 為空須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: frontmatter 'title' 不得為空"], [], m_empty_title),
    ("frontmatter：authors 為空清單須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: frontmatter 'authors' 不得為空清單"], [], m_empty_authors),
    ("frontmatter：year 為 abc 須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: frontmatter 'year' 必須是 4 位數字 (目前為 'abc')"], [], m_bad_year),
    ("frontmatter：pdf 寫成 raw/... 須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: frontmatter 'pdf' 必須等於 'raw/2008-fau-aibo.pdf' (目前為 'raw/...')"],
     [], m_bad_pdf),
    ("基本資訊：發表會議／期刊冒號後留空須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/papers/2008-fau-aibo.md: 基本資訊 '發表會議／期刊' 冒號後不可留空（不知道請寫「論文未提及」）"],
     [], m_basic_info_blank),
    ("frontmatter：實體頁 name 為空須失敗", CHK, True,
     ["項目 03: [ FAIL ]", "wiki/entities/test-dataset.md: frontmatter 'name' 不得為空"], [], m_empty_entity_name),
]
for _name, _script, _neg, _exp, _unexp, _fn in _ROUND3:
    MUTATION_CASES.append({"id": str(_next_id), "name": _name, "script": _script, "neg": _neg,
                           "expected": _exp, "unexpected": _unexp, "fn": _fn})
    _next_id += 1

NOPYPDF_CODE = (
    "import sys, runpy; sys.modules['pypdf'] = None; "
    "script, root = sys.argv[1], sys.argv[2]; sys.argv = [script, '--root', root]; "
    "runpy.run_path(script, run_name='__main__')"
)


def pick_actual(output: str, expected_list: list) -> str:
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    picked = []
    for exp in expected_list:
        hit = next((l for l in lines if exp in l), None)
        if hit and hit not in picked:
            picked.append(hit)
    if picked:
        return " ／ ".join(picked)
    hit = next((l for l in lines if "[FAIL]" in l or "失敗原因:" in l or "總結判定" in l or l.startswith("總結:")), None)
    return hit or (lines[-1] if lines else "無輸出")


def run_tests():
    if TEMP_BASE.exists():
        shutil.rmtree(TEMP_BASE)
    TEMP_BASE.mkdir(parents=True, exist_ok=True)

    out = []
    def emit(s=""):
        print(s)
        out.append(s)

    emit("=" * 100)
    emit("                 SER LLM WIKI 變異測試與正規化套件 (Mutation Testing)")
    emit("=" * 100)
    emit(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    emit(f"基準樣本: {VALID_FIXTURE}")
    emit(f"測試臨時目錄: {TEMP_BASE}")
    emit("-" * 100)

    emit("[ 階段 1 ] 驗證基準樣本 (Valid Fixture) 通過性...")
    base_dir = TEMP_BASE / "baseline"
    shutil.copytree(VALID_FIXTURE, base_dir)
    shutil.rmtree(base_dir / "temp", ignore_errors=True)
    proc = subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "run_checks.py"), "--root", str(base_dir)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        emit(f"[ 嚴重失敗 ] 基準樣本未能全數通過檢查！結束碼: {proc.returncode}")
        emit(proc.stdout + proc.stderr)
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        REPORT_FILE.write_text("\n".join(out), encoding="utf-8")
        return 1
    emit("└── 基準樣本 100% 通過 check.py 與 check_numbers.py 檢查（結束碼 0）\n")

    emit("[ 階段 2 ] 執行變異測試，比對預期訊息與實際訊息...")
    results = []
    for case in MUTATION_CASES:
        run_dir = TEMP_BASE / f"case_{case['id']}"
        shutil.copytree(VALID_FIXTURE, run_dir)
        shutil.rmtree(run_dir / "temp", ignore_errors=True)  # 移除複製來的舊報告，避免誤判
        expected = case["expected"] if isinstance(case["expected"], list) else [case["expected"]]
        unexpected = case.get("unexpected", [])

        try:
            case["fn"](run_dir)
        except MutationNotApplied as e:
            results.append({**case, "exit": "-", "expected_list": expected, "actual": f"變異未套用（案例無效）: {e}", "matched": False})
            continue

        script_path = str(PROJECT_ROOT / "scripts" / case["script"])
        if case.get("runner") == "nopypdf":
            # 模擬缺 pypdf：在子行程內先把 sys.modules['pypdf'] 設為 None，再以 __main__ 執行腳本
            cmd = [sys.executable, "-c", NOPYPDF_CODE, script_path, str(run_dir)]
        else:
            cmd = [sys.executable, script_path, "--root", str(run_dir)] + case.get("args", [])
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        output = proc.stdout + proc.stderr

        if case.get("ignore_exit"):
            exit_ok = True  # 只驗證特定項目的訊息，不以整體結束碼判定
        else:
            exit_ok = (proc.returncode != 0) if case["neg"] else (proc.returncode == 0)
        all_expected = all(e in output for e in expected)
        none_unexpected = not any(u in output for u in unexpected)
        results.append({**case, "exit": proc.returncode, "expected_list": expected,
                        "actual": pick_actual(output, expected), "matched": exit_ok and all_expected and none_unexpected})

    emit("")
    emit("| 編號 | 測試情境 | 腳本 | 類型 | 結束碼 | 預期訊息 | 不應出現 | 實際訊息 | 是否吻合 |")
    emit("|---|---|---|---|---|---|---|---|---|")
    for r in results:
        script_desc = r['script'] + (' ' + ' '.join(r['args']) if r.get('args') else '') + (' [無 pypdf]' if r.get('runner') == 'nopypdf' else '')
        kind = '負向(應失敗)' if r['neg'] else '正向(應通過)'
        if r.get('ignore_exit'):
            kind += '，不判結束碼'
        emit(f"| {r['id']} | {r['name']} | {script_desc} | {kind} | {r['exit']} | "
             f"{' ／ '.join(r['expected_list'])} | {' ／ '.join(r.get('unexpected', [])) or '—'} | "
             f"{r['actual']} | {'YES (吻合)' if r['matched'] else 'NO (不吻合)'} |")

    n_ok = sum(1 for r in results if r["matched"])
    emit("")
    emit("=" * 100)
    emit(f"總結: 共執行 {len(results)} 項案例，吻合通過 {n_ok} 項，不吻合 {len(results) - n_ok} 項")
    emit("=" * 100)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    emit(f"完整報告已寫入: {REPORT_FILE}")
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(run_tests())
