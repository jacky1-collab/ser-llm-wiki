---
name: "RAVDESS"
type: dataset
sources: ["2021-pepino-wav2vec2-ser", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# RAVDESS

## 定義
> "The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS) [3] is a multi-modal database of emotional speech and song." [[2021-pepino-wav2vec2-ser]] (p. 3)

中文說明（AI 整理，待核對）：RAVDESS（Ryerson Audio-Visual Database of Emotional Speech and Song）是由演員演出的情緒語音與歌唱多模態資料庫 [[2021-pepino-wav2vec2-ser]] (p. 3)。

## 核心屬性與特點
- 24 位演員 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)（男性 12 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)、女性 12 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)），演出 2 句 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3) 語句、8 種情緒 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)；每位演員 104 個 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3) 獨特發聲。
- 綜述轉述：7356 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 個檔案、英語、24 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者（男 12 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)／女 12 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)），可免費取得 [[2026-review-ser-adults-children]] (p. 7, Table 2)。
- 綜述認為 RAVDESS 可能有語言、性別與文化偏誤，且錄音情境受控 [[2026-review-ser-adults-children]] (p. 8)。

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：合併 neutral 與 calm 為 7 種情緒 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)，依演員切分；Wav2vec2-PT 多層加權平均（依說話者正規化）為 84.3 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率）。
- [[2026-review-ser-adults-children]]：列於成人資料集表，並在 Table 4 轉述多篇研究在 RAVDESS 上的結果 [[2026-review-ser-adults-children]] (p. 7, Table 2)、[[2026-review-ser-adults-children]] (pp. 14–15)。

## 相關實體（Related Entities）
- [[iemocap]]

## 矛盾／待釐清
- **情緒數**：[[2021-pepino-wav2vec2-ser]] 寫 8 種情緒 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)；綜述 Table 2 寫 7 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)，綜述正文則寫八種：
> "includes 7356 files from 24 actors (12 male and 12 female) across eight different emotions" [[2026-review-ser-adults-children]] (p. 8)
- **年份（綜述內部）**：綜述 Table 2 寫建立年 2018 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)，正文寫 2016 [引述] [[2026-review-ser-adults-children]] (p. 8) 年推出。
