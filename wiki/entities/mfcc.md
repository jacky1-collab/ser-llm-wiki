---
name: "MFCC"
type: feature
sources: ["2016-emoreact", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# MFCC

## 定義
> "MFCC: Mel-Frequency Cepstral Coefficient is widely used in the speech recognition community and has been shown to be successful in emotion recognition" [[2016-emoreact]] (p. 5)

中文說明（AI 整理，待核對）：MFCC（梅爾頻率倒頻譜係數，Mel-Frequency Cepstral Coefficients）是語音辨識常用的倒頻譜特徵，也被用於情緒辨識 [[2016-emoreact]] (p. 5)。

## 核心屬性與特點
- [[2016-emoreact]] 描述 MFCC 以倒頻譜分析模仿人耳的行為 [[2016-emoreact]] (p. 5)。
- [[2026-review-ser-adults-children]] 描述其計算步驟：分幀、加窗、傅立葉轉換、mel 濾波與離散餘弦轉換 [[2026-review-ser-adults-children]] (p. 5)。
- [[2026-review-ser-adults-children]] 稱 MFCC 是研究者最常用的特徵 [[2026-review-ser-adults-children]] (p. 6)。

## 在各論文中的應用與實驗表現
- [[2016-emoreact]]：使用 MFCC 第 1 [本文] [[2016-emoreact]] (p. 5) 至 24 [本文] [[2016-emoreact]] (p. 5) 維；在兒童聲學行為分析中，MFCC 是對各情緒影響最大的聲學行為之一（逐項 Hedges' g 見 [[2016-emoreact]] 的 Table 4）[[2016-emoreact]] (p. 5)。
- [[2026-review-ser-adults-children]]：綜述轉述 Maximos 與 Suendermann-Oeft 以 MFCC 與 ZCR 等手工特徵在 FAU-AIBO 的 UAR 為 69.39% [引述] [[2026-review-ser-adults-children]] (p. 17)；綜述轉述 Cao 等人以 MFCC 搭配 CNN-BiLSTM 在 FAU-AIBO 的準確率為 71.6 [引述] [[2026-review-ser-adults-children]] (p. 18, Table 5)。
- 設定不同，不可直接比較：[[2016-emoreact]] 是效果量分析，綜述引述的是不同研究的分類結果。

## 相關實體（Related Entities）
- [[pitch]]
- [[egemaps]]

## 矛盾／待釐清
無
