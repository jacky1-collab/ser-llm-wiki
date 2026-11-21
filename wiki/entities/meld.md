---
name: "MELD"
type: dataset
sources: ["2024-ser-evals", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# MELD

## 定義
> "MELD: A multimodal multi-party dataset for emotion recognition in conversations" [[2024-ser-evals]] (p. 5)

中文說明（AI 整理，待核對）：MELD 是多模態、多人對話情境的情緒辨識資料集（依 [[2024-ser-evals]] 參考文獻標題） [[2024-ser-evals]] (p. 5)。

## 核心屬性與特點
- [[2024-ser-evals]]（類別對應後）：7 類 [本文] [[2024-ser-evals]] (p. 1, Table 1)、407 位說話者 [本文] [[2024-ser-evals]] (p. 1, Table 1)、英語、12924 個樣本 [本文] [[2024-ser-evals]] (p. 1, Table 1)，平均長度 3.2 秒 [本文] [[2024-ser-evals]] (p. 1, Table 1)，具域外資格 [[2024-ser-evals]] (p. 1, Table 1)。
- 綜述轉述：約 13000 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 句、英語、407 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者、7 種 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 情緒、可免費取得。

## 在各論文中的應用與實驗表現
- [[2024-ser-evals]]：MELD 是未在其上訓練的模型最難泛化的資料集之一；以 MELD 訓練的域外泛化也比以 BAUM 訓練差 [[2024-ser-evals]] (p. 3)。
- [[2026-review-ser-adults-children]]：只列於成人資料集表 [[2026-review-ser-adults-children]] (p. 7, Table 2)。

## 相關實體（Related Entities）
- [[baum]]

## 矛盾／待釐清
- 規模：[[2024-ser-evals]] 為 12924 [本文] [[2024-ser-evals]] (p. 1, Table 1) 個樣本（類別對應後），綜述為約 13000 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 句。說話者數與情緒數兩篇一致。設定不同（對應後 vs. 原始文獻），不可直接比較。
