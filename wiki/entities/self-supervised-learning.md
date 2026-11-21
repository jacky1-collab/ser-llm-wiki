---
name: "自監督學習（self-supervised learning, SSL）"
type: topic
sources: ["2021-pepino-wav2vec2-ser", "2024-ser-evals"]
core_contribution_of: ""
---

# 自監督學習（self-supervised learning, SSL）

## 定義
論文未定義。

## 核心屬性與特點
- [[2024-ser-evals]] 認為自監督學習讓模型不依賴標註資料就能學到豐富的聲學特徵：
> "Self-supervised learning has revolutionized speech representation learning, enabling models to capture rich acoustic features without relying on labeled data." [[2024-ser-evals]] (p. 1)
- [[2021-pepino-wav2vec2-ser]] 描述 wav2vec 2.0 的自監督預訓練：遮罩部分時間步，最小化對比損失 [[2021-pepino-wav2vec2-ser]] (p. 2)。
- [[2024-ser-evals]] 指出 SSL 模型能否泛化到不同語言與情緒表達仍是挑戰 [[2024-ser-evals]] (p. 1)。

## 在各論文中的應用與實驗表現
- [[2021-pepino-wav2vec2-ser]]：以自監督預訓練的 wav2vec 2.0 作為特徵擷取器；未微調的 Wav2vec2-PT 在所有情況都優於微調做 ASR 的 Wav2vec2-FT [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2024-ser-evals]]：在其基準中比較 SSL 模型與 MERT、CLAP、Whisper；Whisper 在跨語言 SER 上優於專用的 SSL 模型 [[2024-ser-evals]] (p. 2)、[[2024-ser-evals]] (p. 4)。例如域外平均方面，WavLM-Large 為 0.161098 [本文] [[2024-ser-evals]] (p. 4, Table 3)，Whisper-Large 為 0.197882 [本文] [[2024-ser-evals]] (p. 4, Table 3)（macro-averaged F1）。
- 設定不同，不可直接比較：兩篇的模型、資料集、切分與指標皆不同。

## 相關實體（Related Entities）
- [[wav2vec2]]
- [[ser-evals]]

## 矛盾／待釐清
- ASR 與情緒辨識的關係（設定不同，不可直接比較）：[[2021-pepino-wav2vec2-ser]] 認為微調做 ASR 會移除對情緒辨識有用的資訊 [[2021-pepino-wav2vec2-ser]] (p. 4)；[[2024-ser-evals]] 認為其結果挑戰了「ASR 模型不適合 SER」的常見看法 [[2024-ser-evals]] (p. 4)。前者比較的是同一 SSL 模型微調前後，後者比較的是不同模型。
