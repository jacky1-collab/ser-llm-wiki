---
name: "頻譜圖（spectrogram）"
type: feature
sources: ["2021-pepino-wav2vec2-ser", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# 頻譜圖（spectrogram）

## 定義
論文未定義。

## 核心屬性與特點
- [[2021-pepino-wav2vec2-ser]] 使用的是 magnitude spectrograms，hanning 窗 25 ms [本文] [[2021-pepino-wav2vec2-ser]] (p. 2)、hop 10 ms [本文] [[2021-pepino-wav2vec2-ser]] (p. 2)。
- [[2026-review-ser-adults-children]] 稱 CNN 與頻譜圖輸入結合時在 SER 中表現穩定良好 [[2026-review-ser-adults-children]] (p. 10)。
- [[2026-review-ser-adults-children]] 認為與 MFCC 或頻譜圖這類結構化表示相比，原始波形缺乏內在組織 [[2026-review-ser-adults-children]] (p. 22)。

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：作為基線特徵，IEMOCAP 為 49.8 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)、RAVDESS 為 44.5 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率），低於 wav2vec 2.0 的 local encoder 特徵 [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2026-review-ser-adults-children]]：綜述轉述 Hsiao 與 Chen 以 mel spectrograms 搭配 DRNN 在兒童 SER 的 UAR 為 46.3% [引述] [[2026-review-ser-adults-children]] (p. 17)。
- 設定不同，不可直接比較：兩篇的頻譜圖種類、資料集與指標皆不同。

## 相關實體（Related Entities）
- [[mfcc]]

## 矛盾／待釐清
無
