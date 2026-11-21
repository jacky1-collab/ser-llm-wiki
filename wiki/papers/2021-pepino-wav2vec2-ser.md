---
title: "Emotion Recognition from Speech Using Wav2vec 2.0 Embeddings"
authors: ["Leonardo Pepino", "Pablo Riera", "Luciana Ferrer"]
year: 2021
type: method
pdf: "raw/2021-pepino-wav2vec2-ser.pdf"
one_sentence_summary: "以預訓練自監督語音模型各層輸出的可訓練加權平均作為淺層神經網路的輸入進行語音情緒辨識，在 IEMOCAP 與 RAVDESS 上優於文獻中僅用聲學資訊的方法。"
---

# Emotion Recognition from Speech Using Wav2vec 2.0 Embeddings

## 基本資訊
- **篇名**：Emotion Recognition from Speech Using Wav2vec 2.0 Embeddings
- **作者**：Leonardo Pepino、Pablo Riera、Luciana Ferrer（ICC, CONICET-UBA；Universidad de Buenos Aires）
- **發表年份**：2021
- **發表會議／期刊**：INTERSPEECH 2021, Brno, Czechia
- **論文類型**：方法
- **原始檔案**：raw/2021-pepino-wav2vec2-ser.pdf

## 研究動機與欲解決問題（Problem & Motivation）
- 情緒辨識資料集相對小，使深度學習技術難以應用 (p. 1)：
> "Emotion recognition datasets are relatively small, making the use of deep learning techniques challenging." (p. 1)
- 作者列舉的資料集包括 SAVEE、RAVDESS、EMODB、IEMOCAP 與 MSP-Podcast；除 MSP-Podcast 外皆相對小 (p. 1)：
> "With the exception of MSP-Podcast, these datasets are relatively small in size, usually including only a few dozen speakers." (p. 1)
- 深度神經網路（DNN）在自動語音辨識（ASR）與說話者辨識上大幅優於傳統方法，但在情緒辨識上的增益有限 (p. 1)：
> "the gains observed on emotion recognition are limited, likely due to the small size of the datasets" (p. 1)
- 小資料集的常見策略是遷移學習（transfer learning）：把在有大量資料的輔助任務上學到的模型，當作特徵擷取器或微調到目標任務 (p. 1)。
- 已有以自監督預訓練 ASR 模型的表徵作為情緒特徵的研究 (p. 1)：
> "Recently, several models for automatic speech recognition (ASR) which use self-supervised pretraining have been released, including wav2vec [23] and VQ-wav2vec [24]." (p. 1)
> "A few recent studies [25, 26, 27] have successfully applied representations from these models as features for emotion recognition." (p. 1)
- 本篇探索以 wav2vec 2.0 作為語音情緒辨識（SER）的特徵擷取器 (p. 1)。

## 方法與架構（Methodology & Architecture）
**wav2vec 2.0 模型（由 Baevski 等人提出 (p. 5)）**
- wav2vec 2.0 是從原始音訊自監督學習表徵的框架 (p. 1)。
- local encoder 由數個卷積區塊組成，把原始音訊編碼成嵌入序列，步距 20 ms [本文] (p. 1)、感受野 25 ms [本文] (p. 1)。
- 公開的模型有 large 與 base 兩種，嵌入維度分別為 1024 [本文] (p. 1) 與 768 [本文] (p. 1)。
- 量化模組（Gumbel-Softmax 層）量化 local encoder 表徵以產生訓練目標；contextualized encoder 由多個 transformer encoder blocks 組成 (p. 1)。
- base 模型使用 12 個 [本文] (p. 1) transformer blocks、各 8 個 [本文] (p. 1) attention heads；large 模型使用 24 個 [本文] (p. 1) transformer blocks、各 16 個 [本文] (p. 1) attention heads。
- 預訓練方式類似 BERT 的遮罩語言模型：隨機遮罩部分時間步，最小化 contextualized encoder 輸出與量化表徵之間的對比損失（contrastive loss）(p. 2)。
- 微調做 ASR 時，在輸出端加上隨機初始化的線性投影並最小化 CTC 損失 (p. 2)。

**本篇比較的兩個預訓練模型**
- Wav2vec2-PT：在 LibriSpeech 上預訓練、未經微調的 base 模型 (p. 2)。
- Wav2vec2-FT：以 LibriSpeech 中 960 小時 [本文] (p. 2) 子集微調做 ASR 的 base 模型 (p. 2)。
- 作者表示使用 large 模型未見顯著改進，且 base 模型可降低計算需求，因此兩者皆用 base 模型 (p. 2)。
- 作者的假設 (p. 2)：
> "these features, particularly the ones from the pre-trained model not fine-tuned for ASR, might also contain prosodic information useful for emotion recognition" (p. 2)

**特徵**
- 比較以 local encoder 輸出、contextualized encoder 輸出作為 SER 模型輸入 (p. 2)。
- 本篇提出：把 12 個 [本文] (p. 2) transformer blocks 的輸出連同 local encoder 輸出做加權平均，權重與 SER 模型其餘部分一起訓練 (p. 2)。
- 多層可訓練加權平均：作為下游模型的第一層，為每一層的輸出學習一個權重；層索引從 0 [本文] (p. 2) 到 12 [本文] (p. 2)，索引起點為 local encoder 輸出，最後一層為 contextualized encoder 輸出；權重初始值為 1.0 [本文] (p. 2)。
- 各層輸出大小相同，因此可以這樣結合；作者認為若串接所有層，特徵維度過高，對下游模型是挑戰；此做法受 Peters 等人 (p. 5) 在 NLP 中的做法啟發 (p. 3)。
- 基線特徵：頻譜圖（spectrogram），hanning 窗 25 ms [本文] (p. 2)、hop 10 ms [本文] (p. 2)；以及 eGeMAPS 低階描述子（LLD），以 opensmile-python 擷取 (p. 2)。
- eGeMAPS 步距 10 ms [本文] (p. 2)，wav2vec 2.0 特徵步距 20 ms [本文] (p. 2)，因此把 eGeMAPS 每 2 個 [本文] (p. 2) 連續框取平均以對齊長度。
- 說話者正規化（speaker normalization）：每個特徵減去該說話者全部資料的平均、除以標準差；關閉時改為全域正規化（global normalization），統計量只用訓練資料計算 (p. 2)。

**下游模型（Fig. 1）**
- Dense：2 層 [本文] (p. 2) dense layer，各 128 個 [本文] (p. 2) 神經元，逐框獨立套用，ReLU 激活，dropout 機率 0.2 [本文] (p. 2)；輸出隨時間平均成大小 128 [本文] (p. 2) 的向量，最後以 softmax dense layer 輸出各情緒類別機率 (p. 2)。
- 訓練下游模型時 wav2vec 2.0 權重不變，只當特徵擷取器 (p. 2)。
- 最大序列長度：IEMOCAP 為 400 [本文] (p. 2)、RAVDESS 為 250 [本文] (p. 2)，分別相當於 8 秒 [本文] (p. 2) 與 5 秒 [本文] (p. 2)。
- 作者指出 contextualized encoder 為 transformer，其輸出可能包含比下游模型所見序列更長的完整波形資訊；local encoder 的感受野有限，只能擷取局部資訊 (p. 2)。
- LSTM 模型 (p. 3)：
> "the second dense layer is replaced by an LSTM layer to account for long-range temporal dependencies" (p. 3)
- Fusion 模型：增加以 eGeMAPS 為輸入的分支 (p. 3)：
> "the outputs of the first dense layer are concatenated before applying the second dense layer" (p. 3)
> "some prosodic information could be absent from the wav2vec 2.0 representations" (p. 3)

## 實驗設定（Experimental Setup）
**訓練**
- batch 為 32 [本文] (p. 3) 個 utterance，Adam 最佳化器，學習率 0.001 [本文] (p. 3)，early stopping patience 4 [本文] (p. 3) epochs。
- 每組結果以 5 個隨機種子 [本文] (p. 3) 執行。
- 指標：各類平均召回率（average recall），報告各種子的平均值與標準差 (p. 3)：
> "the mean and standard deviation over those seeds of the average recall over all emotion classes" (p. 3)

**RAVDESS**
- 24 位演員 [本文] (p. 3)（男性 12 [本文] (p. 3)、女性 12 [本文] (p. 3)），演出 2 句 [本文] (p. 3) 語句，含 8 種情緒 [本文] (p. 3)：happy、sad、angry、fearful、surprise、disgust、calm、neutral。
> "These emotions are expressed in two different intensities: normal and strong, except for neutral (normal only)." (p. 3)
- 每種組合皆有說與唱，重複 2 次 [本文] (p. 3)，每位演員有 104 個 [本文] (p. 3) 獨特發聲。
- 依循先前研究把 neutral 與 calm 合併，得到 7 種情緒 [本文] (p. 3)。
- 演員切分原文如下（切分範圍的疑點見「矛盾／待釐清」）：
> "used the first 20 actors for training, actors 20-22 for validation to do early stopping, and actors 22-24 for test" (p. 3)

**IEMOCAP**
- 長度約 12 小時 [本文] (p. 3)，為 10 位說話者 [本文] (p. 3) 的 scripted 與 improvised 對話；session 數為 5 [本文] (p. 3)：
> "each including speech from an actor and an actress" (p. 3)
- 使用 4 類 [本文] (p. 3)：anger、happiness、sadness、neutral；excitement 樣本改標為 happiness；其他類別與在各標註間沒有多數標籤的樣本被捨棄 (p. 3)。
- 作者在註腳承認此做法並不理想，但因為是文獻常規、便於比較而採用 (p. 3)：
> "discarding no-agreement samples and samples from non-target emotions is not an ideal practice" (p. 3)
- 波形截至 15 秒 [本文] (p. 3) 以降低計算需求；只有 2% [本文] (p. 3) 的波形長於 15 秒 [本文] (p. 3)。
- 評估採 5 折 [本文] (p. 3) 交叉驗證：
> "leaving one session out for each of the folds" (p. 3)
> "We used one of the 4 training sessions to perform early stopping for each cross-validation model." (p. 3)

## 核心數據與成果（Key Results & Metrics）
**Table 1：不同特徵的各類平均召回率（%），平均值 ± 標準差**
> "All results are obtained with the Dense model." (p. 3, Table 1)

所有情況的特徵皆依說話者正規化 (p. 3)。

| 預訓練模型 | 特徵 | IEMOCAP | RAVDESS |
| :--- | :--- | :--- | :--- |
| None | eGeMAPS | 52.4 [本文] (p. 3, Table 1) ± 0.1 [本文] (p. 3, Table 1) | 57.0 [本文] (p. 3, Table 1) ± 2.4 [本文] (p. 3, Table 1) |
| None | Spectrogram | 49.8 [本文] (p. 3, Table 1) ± 1.0 [本文] (p. 3, Table 1) | 44.5 [本文] (p. 3, Table 1) ± 0.8 [本文] (p. 3, Table 1) |
| Wav2vec2-PT | Local enc. | 60.3 [本文] (p. 3, Table 1) ± 0.7 [本文] (p. 3, Table 1) | 65.4 [本文] (p. 3, Table 1) ± 1.7 [本文] (p. 3, Table 1) |
| Wav2vec2-PT | Cont. enc. | 58.5 [本文] (p. 3, Table 1) ± 0.6 [本文] (p. 3, Table 1) | 69.0 [本文] (p. 3, Table 1) ± 0.2 [本文] (p. 3, Table 1) |
| Wav2vec2-PT | All layers | 67.2 [本文] (p. 3, Table 1) ± 0.7 [本文] (p. 3, Table 1) | 84.3 [本文] (p. 3, Table 1) ± 1.7 [本文] (p. 3, Table 1) |
| Wav2vec2-FT | Local enc. | 57.3 [本文] (p. 3, Table 1) ± 1.0 [本文] (p. 3, Table 1) | 58.8 [本文] (p. 3, Table 1) ± 2.7 [本文] (p. 3, Table 1) |
| Wav2vec2-FT | Cont. enc. | 44.6 [本文] (p. 3, Table 1) ± 1.0 [本文] (p. 3, Table 1) | 37.5 [本文] (p. 3, Table 1) ± 3.0 [本文] (p. 3, Table 1) |
| Wav2vec2-FT | All layers | 63.8 [本文] (p. 3, Table 1) ± 0.3 [本文] (p. 3, Table 1) | 68.7 [本文] (p. 3, Table 1) ± 0.9 [本文] (p. 3, Table 1) |

- 兩個預訓練模型的 local encoder 表徵皆優於兩種基線特徵 (p. 3)。
- eGeMAPS 的局部視窗為 60 ms [本文] (p. 3)，頻譜圖與 local encoder 表徵為 25 ms [本文] (p. 3)。
- Wav2vec2-PT 特徵在所有情況皆優於 Wav2vec2-FT；Wav2vec2-FT 只用 contextualized encoder 輸出的結果為表中最差 (p. 3)。
- 使用所有層加權平均（All layers）優於只用 local 或 contextualized encoder 輸出 (p. 3)。
- 加權平均層的權重：中間層權重較大；Wav2vec2-PT 特徵在靠近輸出的層權重比 Wav2vec2-FT 大；不同訓練種子得到的權重非常相近 (pp. 3–4)；見 Fig. 2 (p. 4, Fig. 2)。

**Table 2：模型變體與正規化方式（使用所有層的特徵）**
> "using the wav2vec2-PT features from all layers" (p. 4, Table 2)
> "corresponding to the fifth line in Table 1" (p. 4)

| 模型－正規化 | IEMOCAP | RAVDESS |
| :--- | :--- | :--- |
| Dense - Speaker | 67.2 [本文] (p. 4, Table 2) ± 0.7 [本文] (p. 4, Table 2) | 84.3 [本文] (p. 4, Table 2) ± 1.7 [本文] (p. 4, Table 2) |
| Dense - Global | 65.8 [本文] (p. 4, Table 2) ± 0.3 [本文] (p. 4, Table 2) | 75.7 [本文] (p. 4, Table 2) ± 2.3 [本文] (p. 4, Table 2) |
| LSTM - Global | 64.8 [本文] (p. 4, Table 2) ± 1.9 [本文] (p. 4, Table 2) | 74.6 [本文] (p. 4, Table 2) ± 3.7 [本文] (p. 4, Table 2) |
| Fusion - Global | 66.3 [本文] (p. 4, Table 2) ± 0.7 [本文] (p. 4, Table 2) | 77.5 [本文] (p. 4, Table 2) ± 1.0 [本文] (p. 4, Table 2) |

- 改用全域正規化後結果明顯下降，RAVDESS 下降較多；作者推測是 RAVDESS 不同情緒的音檔詞彙內容變化不大 (p. 4)。
- LSTM 未比簡單的 dense layer 帶來改進；加入 eGeMAPS（Fusion）有小幅改進 (p. 4)。

**Table 2 下半：其他論文的結果（皆為全域正規化）**
以下數字來自各自的原論文，由本篇轉引，全部標 [引述]。本篇稱使用相同實驗設定，且只比較不使用自動或人工轉寫的模型 (p. 4)；但各原論文的完整設定本 Wiki 未核對，不一定相同。表中 RAVDESS 欄為「-」（未提供）(p. 4, Table 2)。
- Mirsamadi 等人 (p. 5) 的 BiLSTM w. attention：IEMOCAP 58.8 [引述] (p. 4, Table 2)
- Satt 等人 (p. 5) 的 CNN-BiLSTM：IEMOCAP 59.4 [引述] (p. 4, Table 2)
- Sarma 等人 (p. 5) 的 TDNN-LSTM w. attention：IEMOCAP 60.7 [引述] (p. 4, Table 2)
- Boigne 等人 (p. 5) 的方法（表中名稱與數字如下列原文）：
> "Wav2Vec [27] 64.3 -" (p. 4, Table 2)

**仿照 Issa 等人 (p. 5) 設定的比較（設定不同，不可與 Table 1 直接比較）**
- 差異：使用 Dense 下游模型並採全域正規化 (p. 4)。
- IEMOCAP：只用 improvised sessions 與 full agreement 樣本 (p. 4)。
- RAVDESS：採 5 折 [本文] (p. 4) 隨機切分的交叉驗證，不合併 calm 與 neutral，共 8 種情緒 [本文] (p. 4)。
- RAVDESS：本篇 84.1% [本文] (p. 4) ± 1.2% [本文] (p. 4)；Issa 等人 71.6% [引述] (p. 4)。
- IEMOCAP：本篇 72.1% [本文] (p. 4) ± 0.9% [本文] (p. 4)；Issa 等人 64.3% [引述] (p. 4)。

## 核心貢獻與作者觀點（Contributions & Insights）
- [作者聲稱] 據作者所知，首次把 wav2vec 2.0 表徵用於語音情緒辨識 (p. 1)。
- [作者聲稱] 提出利用 wav2vec 2.0 多層資訊的新方法（多層可訓練加權平均），比先前方法有顯著改進 (p. 1)。
- [作者聲稱] 分析 wav2vec 2.0 各層對情緒辨識的重要性：中間層權重較大，可能因為已整合足夠的局部資訊，又還不像最後幾層那樣偏向預訓練或微調任務 (p. 1)、(p. 4)。
- [作者聲稱] 在只用聲學資訊的模型中，本篇在 IEMOCAP 與 RAVDESS 的結果優於文獻 (p. 1)；作者稱其所有模型皆優於 Table 2 所列的先前最佳結果 (p. 4)。
- [作者聲稱] wav2vec 2.0 特徵與韻律特徵（eGeMAPS）結合帶來額外增益，顯示 wav2vec 2.0 可能未包含情緒辨識所需的全部韻律資訊 (p. 4)。
- [作者聲稱] 微調做 ASR 的模型表現較差，顯示微調會移除對情緒辨識有用的資訊；作者以音高為例，認為音高對 ASR 可能不重要，但對 SER 很關鍵 (p. 3)、(p. 4)。
- [作者聲稱] 依說話者正規化可去除部分說話者資訊，幫助模型聚焦情緒特徵 (p. 4)。
- [作者聲稱] 已公開重現結果的程式碼 (p. 1)。

## 論文提及之局限性（Limitations & Future Work）
- 捨棄無一致標籤與非目標情緒的樣本並不理想，本篇為了與文獻比較才採用 (p. 3)。
- 下游模型只用全域平均結合連續框的資訊 (p. 3)：
> "is a very simple approach that might be suboptimal because it cannot take into account temporal patterns in the features" (p. 3)
- 作者推測 LSTM 可能比簡單的 dense layer 更容易過擬合或遇到最佳化問題 (p. 4)。
- 作者指出 wav2vec 2.0 特徵可能缺少 eGeMAPS 中的部分資訊 (p. 4)。
- 因計算考量限制了最大序列長度，並截短 IEMOCAP 波形 (p. 2)、(p. 3)。
- 未來研究方向：論文未提及。

## 提及實體清單（Referenced Entities）
- [[emo-db]]（本篇寫作 EMODB）
- [[pitch]]
- [[wav2vec2]]
- Wav2vec2-PT／Wav2vec2-FT（未達建頁門檻）
- [[iemocap]]
- [[ravdess]]
- [[egemaps]]
- [[spectrogram]]
- 各類平均召回率（average recall）（未達建頁門檻）
- 說話者正規化／全域正規化（未達建頁門檻）
- [[transfer-learning]]
- [[self-supervised-learning]]
- LibriSpeech（未達建頁門檻）
- Dense／LSTM／Fusion 下游模型（未達建頁門檻）
- CTC（未達建頁門檻）
- [[savee]]
- [[msp-podcast]]
- 多數決（majority voting）（未達建頁門檻）
- 交叉驗證（cross-validation）（未達建頁門檻）

## 矛盾／待釐清
1. **RAVDESS 演員切分範圍重疊（論文未說明）**：訓練集為前 20 位演員 [本文] (p. 3)，驗證集為演員 20 [本文] (p. 3) 至 22 [本文] (p. 3)，測試集為演員 22 [本文] (p. 3) 至 24 [本文] (p. 3)。照字面，第 20 [本文] (p. 3) 位與第 22 [本文] (p. 3) 位演員各出現在兩個集合中，論文未說明實際切分方式。並列原文、不推測：
> "used the first 20 actors for training, actors 20-22 for validation to do early stopping, and actors 22-24 for test" (p. 3)
2. **與 [[2008-fau-aibo]] 的比較：設定不同，不可直接比較**。[[2008-fau-aibo]] 是德國兒童與機器人自發互動的語料，且未做分類實驗；本篇使用演員演出的 RAVDESS (p. 3) 與含 scripted／improvised 對話的 IEMOCAP (p. 3)。兩篇沒有可對照的數字。
