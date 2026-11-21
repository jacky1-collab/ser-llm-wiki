---
name: "eGeMAPS"
type: feature
sources: ["2021-pepino-wav2vec2-ser", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# eGeMAPS

## 定義
論文未定義。

## 核心屬性與特點
- [[2021-pepino-wav2vec2-ser]] 稱 eGeMAPS 低階描述子（LLD）在情緒辨識文獻中常用，並以 opensmile-python 擷取 [[2021-pepino-wav2vec2-ser]] (p. 2)。
- eGeMAPS 的步距為 10 ms [本文] [[2021-pepino-wav2vec2-ser]] (p. 2)；其局部視窗為 60 ms [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)。

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：作為基線特徵，IEMOCAP 為 52.4 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)、RAVDESS 為 57.0 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率）；在 Fusion 模型中與 wav2vec 2.0 特徵結合，帶來小幅改進 [[2021-pepino-wav2vec2-ser]] (p. 4)。
- [[2026-review-ser-adults-children]]：綜述轉述 Latif 等人以 eGeMAPS 特徵集搭配 DBN，在 FAU-AIBO 的準確率為 74.11% [引述] [[2026-review-ser-adults-children]] (p. 17)。
- 設定不同，不可直接比較：兩篇的資料集（成人 IEMOCAP／RAVDESS vs. 兒童 FAU-AIBO）、模型與指標（各類平均召回率 vs. 準確率）皆不同。

## 相關實體（Related Entities）
- [[mfcc]]
- [[fau-aibo]]

## 矛盾／待釐清
無
