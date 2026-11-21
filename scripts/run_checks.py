#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/run_checks.py - 整合執行腳本
依據 AGENTS.md 第 11 節規格：
依序執行 scripts/check.py 與 scripts/check_numbers.py，
並將兩者檢查結果合併寫入 <root>/temp/check-report.txt。
任何腳本回報失敗則最終結束碼為 1。
"""

import sys
import subprocess
import argparse
from pathlib import Path

# 確保輸出支援 UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    parser = argparse.ArgumentParser(description="SER LLM Wiki 總體品質檢查執行器")
    parser.add_argument("--root", type=str, default=".", help="專案根目錄路徑")
    parser.add_argument("--final", action="store_true", help="完工檢查模式 (PDF 必須全部完成 Ingest)")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    scripts_dir = Path(__file__).resolve().parent

    check_py = scripts_dir / "check.py"
    check_num_py = scripts_dir / "check_numbers.py"

    temp_dir = root_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    combined_report_file = temp_dir / "check-report.txt"

    # 清空或重設合併報告
    if combined_report_file.exists():
        combined_report_file.unlink()

    print("=================================================================")
    print("          執行 SER LLM WIKI 總體驗證套件 (scripts/run_checks.py)")
    print("=================================================================")

    # 1. 執行 check.py
    cmd1 = [sys.executable, str(check_py), "--root", str(root_dir)]
    if args.final:
        cmd1.append("--final")
    res1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    out1 = res1.stdout + res1.stderr

    # 2. 執行 check_numbers.py
    cmd2 = [sys.executable, str(check_num_py), "--root", str(root_dir)]
    res2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    out2 = res2.stdout + res2.stderr

    # 合併輸出
    combined_output = out1.strip() + "\n\n" + out2.strip()
    print(combined_output)

    # 寫入 <root>/temp/check-report.txt
    combined_report_file.write_text(combined_output, encoding="utf-8")

    exit_code = 0 if (res1.returncode == 0 and res2.returncode == 0) else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
