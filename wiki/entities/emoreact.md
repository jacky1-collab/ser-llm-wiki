---
name: "EmoReact"
type: dataset
sources: ["2016-emoreact", "2026-review-ser-adults-children"]
core_contribution_of: "2016-emoreact"
---

# EmoReact

## 定義
> "we introduce a newly collected multimodal emotion dataset of children between the ages of four and fourteen years old" [[2016-emoreact]] (p. 1)

中文說明（AI 整理，待核對）：EmoReact 是由 [[2016-emoreact]] 新蒐集的兒童多模態（視聽）情緒資料集，素材是 YouTube React 頻道中兒童對各種主題做出反應的影片，並以群眾外包標註多種情感狀態 [[2016-emoreact]] (p. 1)、[[2016-emoreact]] (p. 2)。

## 核心屬性與特點
- 來源：YouTube 的 React 頻道，兒童對食物、科技、YouTube 影片、遊戲裝置等主題做出反應 [[2016-emoreact]] (p. 2)、[[2016-emoreact]] (p. 3)。
- 模態：audio 與 video [[2016-emoreact]] (p. 2, Table 1)。
- 規模：最終 1102 [本文] [[2016-emoreact]] (p. 3) 部影片片段，來自 63 位兒童 [本文] [[2016-emoreact]] (p. 3)（女性 32 [本文] [[2016-emoreact]] (p. 3)、男性 31 [本文] [[2016-emoreact]] (p. 3)）。
- 年齡：4 [本文] [[2016-emoreact]] (p. 2, Table 1) 至 14 歲 [本文] [[2016-emoreact]] (p. 2, Table 1)。
- 片段：手動切分，每段只含一位兒童對單一主題的反應 [[2016-emoreact]] (p. 3)：
> "with an average length of five seconds" [[2016-emoreact]] (p. 3)
- 標籤：共 17 種 [本文] [[2016-emoreact]] (p. 2) 情感狀態，包括基本情緒、neutral、valence 與複雜情緒；每部影片可有多個標籤 [[2016-emoreact]] (p. 2)、[[2016-emoreact]] (p. 4)。
- 標註方式：Amazon Mechanical Turk 群眾外包，每部影片由三位獨立標註者標註 [[2016-emoreact]] (p. 3)：
> "Each video was annotated by three independent workers for seventeen labels." [[2016-emoreact]] (p. 3)
- 量表：除 valence 外為 1 [本文] [[2016-emoreact]] (p. 3) 至 4 [本文] [[2016-emoreact]] (p. 3) 的 Likert 量表；valence 為 1 [本文] [[2016-emoreact]] (p. 3) 至 7 [本文] [[2016-emoreact]] (p. 3)。
- 一致性：以 Krippendorff's alpha 評估，後續只用一致性高於 0.4 [本文] [[2016-emoreact]] (p. 3) 的標籤 [[2016-emoreact]] (p. 3)。
- 切分（person-independent）：訓練 432 [本文] [[2016-emoreact]] (p. 5)、驗證 303 [本文] [[2016-emoreact]] (p. 5)、測試 367 [本文] [[2016-emoreact]] (p. 5) 部影片。

## 在各論文中的應用與實驗表現
- [[2016-emoreact]]：以 Naive Bayes、linear SVM、RBF SVM 建立單模態與多模態基線 [[2016-emoreact]] (p. 5)。視聽特徵下 RBF SVM 的平均 AUC ROC 為 0.64 [本文] [[2016-emoreact]] (p. 6, Table 5)，隨機分類器為 0.50 [本文] [[2016-emoreact]] (p. 6, Table 5)。完整數字見 [[2016-emoreact]] 的 Table 5。
- [[2026-review-ser-adults-children]]：列為兒童資料集；建立年 2016 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3)、1102 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) 句、63 位 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) 兒童（男 31 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3)／女 32 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3)）、年齡 4 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) 至 14 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3)，與 [[2016-emoreact]] 一致。綜述未轉述在 EmoReact 上的實驗結果。

## 相關實體（Related Entities）
- [[children-emotion-recognition]]

## 矛盾／待釐清
- 一致性高於 0.4 [本文] [[2016-emoreact]] (p. 3) 的標籤中，Valence（0.65 [本文] [[2016-emoreact]] (p. 3)）未被選入後續使用的標籤，論文未說明原因 [[2016-emoreact]] (p. 3)。
- **綜述的描述與 [[2016-emoreact]] 不同（並列，不選邊）**：
  - 語言：綜述寫 German [[2026-review-ser-adults-children]] (p. 9, Table 3)；[[2016-emoreact]] 未提及語言。
  - 情緒數：綜述寫 15 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3)；[[2016-emoreact]] 為 17 種 [本文] [[2016-emoreact]] (p. 2) 標籤。
  - 取得方式：綜述寫 Licensed [[2026-review-ser-adults-children]] (p. 9, Table 3)；[[2016-emoreact]] 稱資料集將公開 [[2016-emoreact]] (p. 2)。
  - 引用來源：綜述標為 Rajan 等人的文獻，該文獻標題是另一個語料庫：
> "Design and development of a multi-lingual speech corpora (TaMaR-EmoDB) for emotion analysis." [[2026-review-ser-adults-children]] (p. 25)
