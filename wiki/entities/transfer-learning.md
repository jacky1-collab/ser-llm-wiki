---
name: "遷移學習（transfer learning）"
type: topic
sources: ["2021-pepino-wav2vec2-ser", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# 遷移學習（transfer learning）

## 定義
論文未定義。

## 核心屬性與特點
- [[2021-pepino-wav2vec2-ser]] 把遷移學習視為處理小訓練資料的常見策略：
> "A common strategy when dealing with small training datasets is to apply transfer learning techniques." [[2021-pepino-wav2vec2-ser]] (p. 1)
- [[2021-pepino-wav2vec2-ser]] 描述的做法：把在輔助任務上學到的模型當作特徵擷取器，或替換最後幾層後微調到目標任務 [[2021-pepino-wav2vec2-ser]] (p. 1)。
- [[2026-review-ser-adults-children]] 認為遷移學習可利用成人資料預訓練的模型處理兒童資料不足的問題：
> "Transfer learning has the potential to address the issue of small datasets by using pretrained models from adult speech datasets." [[2026-review-ser-adults-children]] (p. 22)

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：以預訓練的 wav2vec 2.0 作為特徵擷取器，接淺層下游模型做 SER [[2021-pepino-wav2vec2-ser]] (p. 1)、[[2021-pepino-wav2vec2-ser]] (p. 2)。
- [[2026-review-ser-adults-children]]：綜述把遷移學習列為兒童 SER 的未來方向，但指出成人與兒童情緒表達差異大，直接把成人模型用於兒童資料仍有問題 [[2026-review-ser-adults-children]] (p. 19)、[[2026-review-ser-adults-children]] (p. 22)。
- 設定不同，不可直接比較：前者是從語音辨識預訓練模型遷移到成人 SER，後者討論的是從成人資料遷移到兒童資料。

## 相關實體（Related Entities）
- [[self-supervised-learning]]
- [[children-emotion-recognition]]

## 矛盾／待釐清
無
