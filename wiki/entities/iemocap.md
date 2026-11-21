---
name: "IEMOCAP"
type: dataset
sources: ["2021-pepino-wav2vec2-ser", "2024-ser-evals"]
core_contribution_of: ""
---

# IEMOCAP

## 定義
> "The Interactive Emotional Dyadic Motion Capture (IEMOCAP) dataset [5] has a length of approximately 12 hours and consists of scripted and improvised dialogues by 10 speakers." [[2021-pepino-wav2vec2-ser]] (p. 3)

中文說明（AI 整理，待核對）：IEMOCAP（Interactive Emotional Dyadic Motion Capture）是由說話者進行劇本與即興對話的情緒資料集 [[2021-pepino-wav2vec2-ser]] (p. 3)。

## 核心屬性與特點
- 長度約 12 小時 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)，10 位說話者 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)，含劇本與即興對話 [[2021-pepino-wav2vec2-ser]] (p. 3)。
- session 數為 5 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)，每個 session 有一位男演員與一位女演員：
> "each including speech from an actor and an actress" [[2021-pepino-wav2vec2-ser]] (p. 3)
- 標註者可為每個樣本選擇一個或多個情緒標籤 [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2024-ser-evals]] 稱 IEMOCAP 為知名的 SER 基準，但認為這類基準偏重域內評估 [[2024-ser-evals]] (p. 2)：
> "these benchmarks often emphasize in-domain evaluation and may not adequately capture the challenges of real-world deployment" [[2024-ser-evals]] (p. 2)

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：使用 4 類 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)（anger、happiness、sadness、neutral，excitement 併入 happiness），以 5 折 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3) 交叉驗證、每折留出一個 session；最佳結果為 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率，依說話者正規化）。仿照另一篇論文設定（只用 improvised sessions 與 full agreement 樣本、全域正規化）時為 72.1% [本文] [[2021-pepino-wav2vec2-ser]] (p. 4)。
- [[2024-ser-evals]]：只在相關研究中提及，未列入其基準的資料集 [[2024-ser-evals]] (p. 2)、[[2024-ser-evals]] (p. 1, Table 1)。
- 兩篇對 IEMOCAP 沒有可對照的數字。

## 相關實體（Related Entities）
- [[msp-podcast]]
- [[wav2vec2]]

## 矛盾／待釐清
無
