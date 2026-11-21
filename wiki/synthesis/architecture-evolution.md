# 特徵與模型做法對照（依 5 篇論文）

本頁不是領域史，只是五篇論文做法的並列；綜述的領域發展論述以綜述轉述呈現。

## 本頁回答的問題
- 五篇論文各自用了哪些特徵與模型？
- 各篇如何評價手工特徵、自監督表徵、ASR 模型與原始波形？
- 哪些比較是同篇同設定、可以比較的？

## 手工特徵
- [[2008-fau-aibo]]：未建模型；提供人工校正的音高值，並提到 CEICES 倡議發展的特徵編碼規格 [[2008-fau-aibo]] (p. 3)。
- [[2016-emoreact]]：以 OpenFace 擷取視覺特徵、COVAREP 擷取聲學特徵（嗓音品質、韻律、MFCC），再以 Naive Bayes、linear SVM、RBF SVM 建立基線 [[2016-emoreact]] (p. 5)。
- [[2021-pepino-wav2vec2-ser]]：以 eGeMAPS 與頻譜圖作為基線特徵 [[2021-pepino-wav2vec2-ser]] (p. 2)。
- [[2026-review-ser-adults-children]]：比較手工特徵與原始波形建模方法，並稱 MFCC 是最常用的特徵 [[2026-review-ser-adults-children]] (p. 4)、[[2026-review-ser-adults-children]] (p. 6)。
- 相關實體：[[pitch]]、[[mfcc]]、[[egemaps]]、[[spectrogram]]。

## 自監督表徵
- [[2021-pepino-wav2vec2-ser]]：以預訓練的 wav2vec 2.0 作為特徵擷取器，搭配淺層下游模型，並提出多層可訓練加權平均 [[2021-pepino-wav2vec2-ser]] (p. 2)。
  - 【可比較：同篇、同協定（Table 1）】IEMOCAP 上 Wav2vec2-PT 所有層為 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)，Wav2vec2-FT 所有層為 63.8 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)；作者稱 PT 在所有情況都優於 FT [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2024-ser-evals]]：以多個語音表徵模型為骨幹、接約 500K [本文] [[2024-ser-evals]] (p. 2) 參數的 MLP 做評估 [[2024-ser-evals]] (p. 2)。
- 相關實體：[[wav2vec2]]、[[self-supervised-learning]]、[[transfer-learning]]。

## ASR 模型
- [[2024-ser-evals]]：主要以 ASR 為目的的 Whisper 在跨語言 SER 上優於專用的 SSL 模型 [[2024-ser-evals]] (p. 4)。
  - 【可比較：同篇、同協定（Table 3）】域外平均 Whisper-Large 為 0.197882 [本文] [[2024-ser-evals]] (p. 4, Table 3)，WavLM-Large 為 0.161098 [本文] [[2024-ser-evals]] (p. 4, Table 3)（macro-averaged F1）。
- [[2021-pepino-wav2vec2-ser]]：微調做 ASR 的 wav2vec 2.0 表現較差，作者認為微調會移除對情緒辨識有用的資訊 [[2021-pepino-wav2vec2-ser]] (p. 4)。
- 兩篇之間：【設定不同，不可直接比較：差在比較對象（同一模型微調前後 vs. 不同模型）、資料集、切分與指標】。

## 原始波形與深度學習架構（綜述轉述）
- 綜述稱 CNN 是 SER 中最廣泛使用的深度神經網路模型 [[2026-review-ser-adults-children]] (p. 17)。
- 綜述稱在兒童 SER 中，手工特徵方法目前優於原始波形模型 [[2026-review-ser-adults-children]] (p. 22)。
- 綜述轉述 Heracleous 等人以原始波形的 DNN 在 FAU-AIBO 的 UAR 為 61.1% [引述] [[2026-review-ser-adults-children]] (p. 17)。

## 論文未涵蓋
- 五篇論文以外的模型或特徵做法的發展脈絡：論文未涵蓋。
- 在同一資料集與同一協定下，比較手工特徵、自監督表徵、ASR 模型與原始波形模型：論文未涵蓋。
- 原始波形模型在兒童 SER 的本篇自研實驗：論文未涵蓋（五篇中只有綜述轉述）。

## 矛盾／待釐清
以下只匯總各頁既有條目，詳見原頁：
- ASR 與 SER 的關係：[[2021-pepino-wav2vec2-ser]] 與 [[2024-ser-evals]] 的發現方向不同，設定不同，不可直接比較（見 [[2024-ser-evals]]、[[wav2vec2]]、[[self-supervised-learning]]）。
- wav2vec 2.0 在 [[2024-ser-evals]] 中有另一種寫法；該篇的 w2v-bert-2.0 與 wav2vec 2.0 的關係論文未說明，本 wiki 不合併（見 [[wav2vec2]]）。
- 各篇指標名稱不同（average recall、AUC ROC／skew normalized F1、macro-averaged F1、綜述的 unweighted accuracy (UAR)），本 wiki 不判定是否為同一指標，數值不跨篇比較。
