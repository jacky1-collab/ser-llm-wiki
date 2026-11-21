---
name: "wav2vec 2.0"
type: model
sources: ["2021-pepino-wav2vec2-ser", "2024-ser-evals"]
core_contribution_of: ""
---

# wav2vec 2.0

## 定義
> "Wav2vec 2.0 [28] is a framework for self-supervised learning of representations from raw audio." [[2021-pepino-wav2vec2-ser]] (p. 1)

中文說明（AI 整理，待核對）：wav2vec 2.0 是從原始音訊以自監督方式學習語音表徵的框架。兩篇論文都不是提出此模型的原始論文 [[2021-pepino-wav2vec2-ser]] (p. 1)、[[2024-ser-evals]] (p. 1)。

## 核心屬性與特點
- local encoder 由卷積區塊組成，步距 20 ms [本文] [[2021-pepino-wav2vec2-ser]] (p. 1)、感受野 25 ms [本文] [[2021-pepino-wav2vec2-ser]] (p. 1)。
- base 模型嵌入維度 768 [本文] [[2021-pepino-wav2vec2-ser]] (p. 1)、使用 12 個 [本文] [[2021-pepino-wav2vec2-ser]] (p. 1) transformer blocks；large 模型嵌入維度 1024 [本文] [[2021-pepino-wav2vec2-ser]] (p. 1)、使用 24 個 [本文] [[2021-pepino-wav2vec2-ser]] (p. 1) transformer blocks。
- 預訓練方式：遮罩部分時間步並最小化對比損失 [[2021-pepino-wav2vec2-ser]] (p. 2)。
- [[2024-ser-evals]] 把它列為在語音處理任務（含情緒辨識）上達到頂尖表現的 SSL 模型之一：
> "Models like wav2vec 2.0 [1], HuBERT [2], and WavLM [3] have achieved state-of-the-art performance on various speech processing tasks" [[2024-ser-evals]] (p. 1)

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：以 Wav2vec2-PT（未微調）與 Wav2vec2-FT（微調做 ASR）擷取特徵，接淺層下游模型；多層加權平均（All layers）搭配 Wav2vec2-PT 在 IEMOCAP 為 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)、RAVDESS 為 84.3 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率，依說話者正規化）。
- [[2024-ser-evals]]：只在引言與相關研究中提及，未列入 Table 2 的骨幹模型 [[2024-ser-evals]] (p. 1)、[[2024-ser-evals]] (p. 2, Table 2)。Table 2 中的 w2v-bert-2.0 引用的是其他文獻，論文未說明它與 wav2vec 2.0 的關係，本 Wiki 不合併 [[2024-ser-evals]] (p. 2, Table 2)。

## 相關實體（Related Entities）
- [[self-supervised-learning]]
- [[iemocap]]

## 矛盾／待釐清
- 名稱寫法：[[2024-ser-evals]] 引言中的另一種寫法見下列引文：
> "Recent advancements in self-supervised learning have led to powerful speech representation models like wav2vec2 [1], HuBERT [2], and WavLM [3]" [[2024-ser-evals]] (p. 1)
- ASR 微調／ASR 模型與情緒辨識（設定不同，不可直接比較）：[[2021-pepino-wav2vec2-ser]] 發現微調做 ASR 的 wav2vec 2.0 表現較差 [[2021-pepino-wav2vec2-ser]] (p. 4)；[[2024-ser-evals]] 則發現以 ASR 為主要目的的 Whisper 優於 SSL 模型 [[2024-ser-evals]] (p. 4)。兩篇比較的模型、資料集、切分與指標皆不同。
