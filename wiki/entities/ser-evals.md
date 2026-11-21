---
name: "SER Evals"
type: metric
sources: ["2024-ser-evals"]
core_contribution_of: "2024-ser-evals"
---

# SER Evals

## 定義
> "We propose a large-scale benchmark to evaluate the robustness and adaptability of state-of-the-art SER models in both in-domain and out-of-domain settings." [[2024-ser-evals]] (p. 1)

中文說明（AI 整理，待核對）：SER Evals 是 [[2024-ser-evals]] 提出的語音情緒辨識基準，以多語言、較少被使用的情緒語料，同時評估模型在域內（訓練與測試同分布）與域外（不同分布、zero-shot）設定下的表現 [[2024-ser-evals]] (p. 1)。

## 核心屬性與特點
- 資料集：多語言資料集，刻意選用較少被使用的語料；標籤重新對應到統一的類別空間 [[2024-ser-evals]] (p. 2)。
- 域外資格：類別對應後擁有完全相同類別的資料集才可用於域外測試 [[2024-ser-evals]] (p. 2)。
- 切分：每個資料集 80% [本文] [[2024-ser-evals]] (p. 2, Fig. 1) 訓練、20% [本文] [[2024-ser-evals]] (p. 2, Fig. 1) 做域內測試。
- 效能矩陣：列為訓練資料集、欄為評估資料集；對角線為域內，非對角線為域外 zero-shot [[2024-ser-evals]] (p. 3)。
- 三個指標：域內可分性（對角線平均）、給定訓練資料集的域外表現（列平均）、未見資料集上的平均表現（欄平均）；皆以 macro-averaged F1 表示 [[2024-ser-evals]] (p. 3)。
- Weighted Average：結合域內與域外的平均與標準差，discounting factor λ 設為 1.0 [本文] [[2024-ser-evals]] (p. 4)。
- 分類器：約 500K [本文] [[2024-ser-evals]] (p. 2) 參數的 MLP；評估時使用 logit adjustment [[2024-ser-evals]] (p. 2)、[[2024-ser-evals]] (p. 3)。

## 在各論文中的應用與實驗表現
- [[2024-ser-evals]]：Table 3 中 Weighted Average 最高的是 Whisper-Large-v2，為 0.345741 [本文] [[2024-ser-evals]] (p. 4, Table 3)；最低的是 w2v-bert-2.0，為 0.268165 [本文] [[2024-ser-evals]] (p. 4, Table 3)。完整數字見 [[2024-ser-evals]] 的 Table 3。

## 相關實體（Related Entities）
- [[self-supervised-learning]]
- [[emo-db]]（基準中的資料集之一）

## 矛盾／待釐清
- 論文稱模型對 URDU 與 AESDD 泛化最好，但兩者在 Table 1 標示為不具域外資格 [[2024-ser-evals]] (p. 3)、[[2024-ser-evals]] (p. 1, Table 1)；詳見 [[2024-ser-evals]] 的「矛盾／待釐清」。
