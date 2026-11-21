#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_deck.py - 把 deck/slides.md 決定性地轉成單一檔案 deck/index.html（不經 AI）

- 投影片以單獨一行的 `---` 分隔（與 check_deck.py 相同），移除 HTML 註解後轉換。
- 每頁輸出 <section class="slide">；支援：# 標題、段落、- 條列、> 引文、Markdown 表格、**粗體**。
- [[slug]] 轉成純文字標記「〔來源：slug〕」，不產生連結；(p. N) 原樣保留。
- 內嵌 CSS 與少量 JS（鍵盤左右鍵與按鈕換頁、以 JS 產生「第 k／N 頁」），不引用任何外部資源。
- 只做格式轉換，不新增、刪除或改寫內容文字；輸出不含時間戳記，同一輸入必得同一輸出。

用法：python scripts/build_deck.py [--root <專案根目錄>]
結束碼：0 成功；2 找不到 deck/slides.md。
"""

import sys
import re
import html
import argparse
from pathlib import Path

if sys.platform == "win32" and __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_deck import split_slides  # noqa: E402
import check_numbers as cn  # noqa: E402

CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,"Noto Sans TC","Microsoft JhengHei",sans-serif;background:#f4f4f2;color:#1d1d1f}
main{max-width:1000px;margin:0 auto;padding:24px 16px 96px}
.slide{display:none;background:#fff;border-radius:12px;padding:32px 40px;min-height:70vh;box-shadow:0 1px 4px rgba(0,0,0,.12)}
.slide.active{display:block}
h1{font-size:1.9rem;margin:0 0 1rem}
h2{font-size:1.4rem}
p,li{font-size:1.15rem;line-height:1.7}
blockquote{margin:1rem 0;padding:.5rem 1rem;border-left:4px solid #888;background:#f7f7f7;font-style:italic}
table{border-collapse:collapse;margin:1rem 0;font-size:1rem}
th,td{border:1px solid #bbb;padding:.4rem .7rem;text-align:left}
th{background:#eee}
.src{color:#666;font-size:.9em}
nav{position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:center;align-items:center;gap:16px;padding:12px;background:#fff;border-top:1px solid #ddd}
button{font-size:1rem;padding:.4rem 1rem;cursor:pointer}
@media print{nav{display:none}.slide{display:block;page-break-after:always;box-shadow:none}}
""".strip()

JS = """
(function(){
  var slides = document.querySelectorAll('section.slide');
  var pager = document.getElementById('pager');
  var i = 0;
  function show(k){
    if (k < 0 || k >= slides.length) return;
    slides[i].classList.remove('active');
    i = k;
    slides[i].classList.add('active');
    pager.textContent = '\\u7b2c ' + (i + 1) + '\\uff0f' + slides.length + ' \\u9801';
  }
  document.getElementById('prev').addEventListener('click', function(){ show(i - 1); });
  document.getElementById('next').addEventListener('click', function(){ show(i + 1); });
  document.addEventListener('keydown', function(e){
    if (e.key === 'ArrowRight') show(i + 1);
    if (e.key === 'ArrowLeft') show(i - 1);
  });
  if (slides.length) { slides[0].classList.add('active'); show(0); }
})();
""".strip()

LINK = re.compile(r'\[\[([a-zA-Z0-9_\-]+)\]\]')
BOLD = re.compile(r'\*\*(.+?)\*\*')
TABLE_SEP = re.compile(r'^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$')


def inline(text: str) -> str:
    """跳脫 HTML 後轉換 **粗體** 與 [[slug]]；其餘文字原樣保留。"""
    t = html.escape(text, quote=False)
    t = BOLD.sub(r'<strong>\1</strong>', t)
    t = LINK.sub(lambda m: f'<span class="src">〔來源：{m.group(1)}〕</span>', t)
    return t


def table_cells(line: str) -> list:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def render_slide(lines: list) -> str:
    out, para, i = [], [], 0
    rows = [l.rstrip() for l in lines]

    def flush_para():
        if para:
            out.append("<p>" + "\n".join(inline(p) for p in para) + "</p>")
            para.clear()

    while i < len(rows):
        s = rows[i].strip()
        if not s:
            flush_para()
            i += 1
        elif re.match(r'^#{1,6} ', s):
            flush_para()
            level = len(s) - len(s.lstrip('#'))
            out.append(f"<h{level}>{inline(s[level:].strip())}</h{level}>")
            i += 1
        elif s.startswith("- "):
            flush_para()
            items = []
            while i < len(rows) and rows[i].strip().startswith("- "):
                items.append(f"<li>{inline(rows[i].strip()[2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif s.startswith(">"):
            flush_para()
            quotes = []
            while i < len(rows) and rows[i].strip().startswith(">"):
                quotes.append(inline(rows[i].strip()[1:].strip()))
                i += 1
            out.append("<blockquote>" + "<br>\n".join(quotes) + "</blockquote>")
        elif s.startswith("|"):
            flush_para()
            block = []
            while i < len(rows) and rows[i].strip().startswith("|"):
                block.append(rows[i].strip())
                i += 1
            html_rows = []
            for j, row in enumerate(block):
                if TABLE_SEP.match(row):
                    continue
                cells = table_cells(row)
                tag = "th" if (j == 0 and len(block) > 1 and TABLE_SEP.match(block[1])) else "td"
                html_rows.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            out.append("<table>" + "".join(html_rows) + "</table>")
        else:
            para.append(s)
            i += 1
    flush_para()
    return '<section class="slide">\n' + "\n".join(out) + "\n</section>"


def build(markdown: str) -> str:
    lines = cn.strip_html_comments(markdown.replace('\r\n', '\n').replace('\r', '\n')).split('\n')
    sections = [render_slide([l for _, l in slide]) for slide in split_slides(lines)]
    return ("<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>SER 簡報</title>\n<style>\n" + CSS + "\n</style>\n</head>\n<body>\n<main id=\"deck\">\n"
            + "\n".join(sections)
            + "\n</main>\n<nav><button id=\"prev\" type=\"button\">上一頁</button>"
              "<span id=\"pager\"></span><button id=\"next\" type=\"button\">下一頁</button></nav>\n"
              "<script>\n" + JS + "\n</script>\n</body>\n</html>\n")


def main():
    ap = argparse.ArgumentParser(description="把 deck/slides.md 轉成 deck/index.html")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="專案根目錄")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    src = root / "deck" / "slides.md"
    if not src.is_file():
        print(f"找不到 {src}，未產生 HTML")
        sys.exit(2)
    out = root / "deck" / "index.html"
    out.write_text(build(src.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    print(f"已產生 {out}")


if __name__ == "__main__":
    main()
