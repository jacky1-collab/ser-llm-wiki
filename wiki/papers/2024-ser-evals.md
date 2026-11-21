---
title: "SER Evals: In-domain and Out-of-domain Benchmarking for Speech Emotion Recognition"
authors: ["Mohamed Osman", "Daniel Z. Kaplan", "Tamer Nadeem"]
year: 2024
type: benchmark
pdf: "raw/2024-ser-evals.pdf"
one_sentence_summary: "提出以多語言、較少被使用的情緒語料評估語音情緒辨識模型域內與域外泛化能力的大規模基準，發現以語音辨識為主要目的的 Whisper 在跨語言情緒辨識上優於專用的自監督模型。"
---

# SER Evals: In-domain and Out-of-domain Benchmarking for Speech Emotion Recognition

## 基本資訊
- **篇名**：SER Evals: In-domain and Out-of-domain Benchmarking for Speech Emotion Recognition
- **作者**：Mohamed Osman、Daniel Z. Kaplan、Tamer Nadeem（Virginia Commonwealth University；realiz.ai）
- **發表年份**：2024
- **發表會議／期刊**：arXiv:2408.07851v1 [cs.CL]（PDF 上標示的出處）
- **論文類型**：基準評測
- **原始檔案**：raw/2024-ser-evals.pdf

## 研究動機與欲解決問題（Problem & Motivation）
- 自監督學習（self-supervised learning, SSL）模型推動了語音情緒辨識（SER），但這些模型能否泛化到不同語言與情緒表達仍是挑戰 (p. 1)。
- 作者認為現有 SER 基準多集中於少數被充分研究的資料集，可能無法反映真實情境；而且偏重域內（in-domain）評估，忽略了實際部署所需的域外（out-of-domain）泛化 (p. 1)。
- 本篇對域內與域外的定義 (p. 1)：
> "we define in-domain as evaluating on the same data distribution seen in training, and out-of-domain as evaluating on a different data distribution" (p. 1)
- 作者也提到 IEMOCAP 與 MSP-Podcast 等知名基準偏重域內評估；EMO-SUPERB 與 SERAB 在語言、資料集多樣性與域外泛化上有所限制 (p. 2)。

## 方法與架構（Methodology & Architecture）
**評測設計**
- 資料集：蒐集多語言資料集，刻意選用較少被使用的語料，以降低過擬合並鼓勵更穩健的模型 (p. 2)。資料集清單見下方 Table 1 (p. 1, Table 1)。
- 前處理：最大音訊長度設為 30 秒 [本文] (p. 2)；以 Huggingface 函式庫做前處理與推論 (p. 2)。
- 標籤重新對應 (p. 2)：
> "we remap the label space by mapping the original emotion labels to a unified eight-class space" (p. 2)
- 各資料集的確切對應方式未寫在論文中，只放在開源程式碼裡 (p. 2)。
- 域外資格（OOD Eligible）：類別對應後擁有完全相同類別（不含「other」）的資料集才可用於域外測試；計算域外指標時捨棄「other」樣本，並禁止模型預測「other」(p. 2)。
- 所有資料集都計入域內測試，只有具域外資格的資料集計入域外指標 (p. 3)。

**骨幹模型（backbone）與分類器**
- 骨幹模型為 Table 2 所列的語音表徵模型，另評估音樂辨識模型 MERT、對比式學習模型 CLAP，以及以 encoder-decoder 架構訓練做 ASR 的 Whisper encoder (p. 2)。
- 分類器：約 500K [本文] (p. 2) 參數的多層感知器（MLP），訓練 100 [本文] (p. 2) 個 epoch，label smoothing 係數 0.1 [本文] (p. 2)：
> "The MLP consists of two hidden layers" (p. 2)
- 不先對特徵取平均，而是對每個特徵框執行 MLP 後再對預測取平均；作者表示這樣保留更多資訊、結果更強也更一致 (p. 2)。
- 評估時使用 logit adjustment，依訓練與測試資料分布的差異調整輸出 logits，以減輕類別不平衡的影響 (p. 3)。

**評測協定**
- 依 Fig. 1，每個資料集以 80% [本文] (p. 2, Fig. 1) 訓練、20% [本文] (p. 2, Fig. 1) 做域內測試（切分比例僅見於 Fig. 1 圖內文字）(p. 2, Fig. 1)。
- 每個模型建立一個效能矩陣：列為訓練資料集、欄為評估資料集；對角線為域內表現，非對角線為域外 zero-shot 表現 (p. 3)。
- 三個指標 (p. 3)：
  - 域內可分性：對角線元素的平均。
  - 給定訓練資料集的域外表現：每列（不含對角線）的平均。
  - 未見資料集上的平均表現：每欄（不含對角線）的平均。
- 所有指標以 macro-averaged F1 score 表示 (p. 3)。
- Weighted Average =（域外平均 + 域內平均）/ 2 [本文] (p. 4) − λ ×（域外標準差 + 域內標準差）/ 2 [本文] (p. 4)；λ（discounting factor）設為 1.0 [本文] (p. 4)。

## 實驗設定（Experimental Setup）
- 資料集：Table 1 的多語言資料集，數值為類別對應後的統計 (p. 1, Table 1)。
- 切分：每個資料集以 80% [本文] (p. 2, Fig. 1) 訓練、20% [本文] (p. 2, Fig. 1) 做域內測試（切分比例僅見於 Fig. 1 圖內文字）；域外為在其他具域外資格的資料集上做 zero-shot 評估 (p. 2, Fig. 1)、(p. 3)。
- 骨幹模型：Table 2 的 Huggingface checkpoints (p. 2, Table 2)。
- 分類器：上述 MLP，骨幹模型特徵逐框輸入 (p. 2)。
- 指標：macro-averaged F1 score (p. 3)。
- 評估時使用 logit adjustment (p. 3)。

## 核心數據與成果（Key Results & Metrics）
**Table 1：基準使用的多語言資料集（類別對應後的數值，本篇整理）**
| 資料集 | 類別數 | 說話者數 | 語言 | 樣本數 | 平均長度（秒） | 域外資格 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| URDU | 4 [本文] (p. 1, Table 1) | 6 [本文] (p. 1, Table 1) | Urdu | 400 [本文] (p. 1, Table 1) | 2.5 [本文] (p. 1, Table 1) | No |
| EmoDB | 6 [本文] (p. 1, Table 1) | 10 [本文] (p. 1, Table 1) | German | 535 [本文] (p. 1, Table 1) | 2.8 [本文] (p. 1, Table 1) | No |
| EMOVO | 7 [本文] (p. 1, Table 1) | 10 [本文] (p. 1, Table 1) | Italian | 588 [本文] (p. 1, Table 1) | 3.1 [本文] (p. 1, Table 1) | Yes |
| eNTERFACE | 6 [本文] (p. 1, Table 1) | 42 [本文] (p. 1, Table 1) | English | 1293 [本文] (p. 1, Table 1) | 2.9 [本文] (p. 1, Table 1) | No |
| MESD | 6 [本文] (p. 1, Table 1) | 6 [本文] (p. 1, Table 1) | Spanish | 1150 [本文] (p. 1, Table 1) | 0.7 [本文] (p. 1, Table 1) | Yes |
| MASC | 5 [本文] (p. 1, Table 1) | 68 [本文] (p. 1, Table 1) | Mandarin | 25636 [本文] (p. 1, Table 1) | 1.9 [本文] (p. 1, Table 1) | No |
| DEMoS | 7 [本文] (p. 1, Table 1) | 68 [本文] (p. 1, Table 1) | Italian | 9697 [本文] (p. 1, Table 1) | 2.9 [本文] (p. 1, Table 1) | Yes |
| CASIA | 6 [本文] (p. 1, Table 1) | 4 [本文] (p. 1, Table 1) | Mandarin | 1200 [本文] (p. 1, Table 1) | 1.9 [本文] (p. 1, Table 1) | No |
| AESDD | 5 [本文] (p. 1, Table 1) | 6 [本文] (p. 1, Table 1) | Greek | 604 [本文] (p. 1, Table 1) | 4.1 [本文] (p. 1, Table 1) | No |
| BAUM | 8 [本文] (p. 1, Table 1) | 31 [本文] (p. 1, Table 1) | Turkish | 1398 [本文] (p. 1, Table 1) | 4.6 [本文] (p. 1, Table 1) | Yes |
| EEKK | 4 [本文] (p. 1, Table 1) | 10 [本文] (p. 1, Table 1) | Estonian | 1164 [本文] (p. 1, Table 1) | 3.4 [本文] (p. 1, Table 1) | No |
| Thorsten | 6 [本文] (p. 1, Table 1) | 1 [本文] (p. 1, Table 1) | German | 2399 [本文] (p. 1, Table 1) | 4.4 [本文] (p. 1, Table 1) | No |
| RESD | 7 [本文] (p. 1, Table 1) | 200 [本文] (p. 1, Table 1) | Russian | 1396 [本文] (p. 1, Table 1) | 6.0 [本文] (p. 1, Table 1) | No |
| MELD | 7 [本文] (p. 1, Table 1) | 407 [本文] (p. 1, Table 1) | English | 12924 [本文] (p. 1, Table 1) | 3.2 [本文] (p. 1, Table 1) | Yes |
| MEAD | 7 [本文] (p. 1, Table 1) | 60 [本文] (p. 1, Table 1) | English | 31724 [本文] (p. 1, Table 1) | 4.2 [本文] (p. 1, Table 1) | Yes |
| CaFE | 7 [本文] (p. 1, Table 1) | 12 [本文] (p. 1, Table 1) | French | 936 [本文] (p. 1, Table 1) | 4.4 [本文] (p. 1, Table 1) | Yes |
| Expresso | 8 [本文] (p. 1, Table 1) | 4 [本文] (p. 1, Table 1) | English | 11954 [本文] (p. 1, Table 1) | 4.2 [本文] (p. 1, Table 1) | Yes |
| ShEMO | 6 [本文] (p. 1, Table 1) | 87 [本文] (p. 1, Table 1) | Persian | 3000 [本文] (p. 1, Table 1) | 4.1 [本文] (p. 1, Table 1) | No |
| SUBESCO | 7 [本文] (p. 1, Table 1) | 20 [本文] (p. 1, Table 1) | Bangla | 7000 [本文] (p. 1, Table 1) | 4.0 [本文] (p. 1, Table 1) | Yes |

表中資料集名稱在 PDF 中寫作「URDUDataset」「EmoDBDataset」等（帶 Dataset 字尾），此處省略字尾 (p. 1, Table 1)。

**Table 2：骨幹模型（訓練資料時數與參數量為各模型本身的屬性，標 [引述]）**
| Checkpoint | 訓練資料時數 | 參數量 |
| :--- | :--- | :--- |
| facebook/w2v-bert-2.0 | 4500k [引述] (p. 2, Table 2) | 580M [引述] (p. 2, Table 2) |
| facebook/hubert-large-ll60k | 60k [引述] (p. 2, Table 2) | 315M [引述] (p. 2, Table 2) |
| microsoft/wavlm-large | 94k [引述] (p. 2, Table 2) | 315M [引述] (p. 2, Table 2) |
| laion/larger clap music and speech | 超過 10k [引述] (p. 2, Table 2) | 193M [引述] (p. 2, Table 2) |
| m-a-p/MERT-v1-330M | 160k [引述] (p. 2, Table 2) | 315M [引述] (p. 2, Table 2) |
| openai/whisper-medium | 680k [引述] (p. 2, Table 2) | 307M [引述] (p. 2, Table 2) |
| openai/whisper-large-v2 | 680k [引述] (p. 2, Table 2) | 636M [引述] (p. 2, Table 2) |
| openai/whisper-large-v3 | 5000k [引述] (p. 2, Table 2) | 636M [引述] (p. 2, Table 2) |
| openai/whisper-large | 680k [引述] (p. 2, Table 2) | 636M [引述] (p. 2, Table 2) |

**Table 3：各模型的關鍵指標（macro-averaged F1，本篇結果）**
設定：Table 1 的資料集，各資料集依 Fig. 1 切分做域內、具域外資格的資料集間做 zero-shot 域外評估；分類器為上述 MLP；評估時使用 logit adjustment (p. 2)、(p. 3)。
| 模型 | 域內平均 | 域內標準差 | 域外平均 | 域外標準差 | Weighted Average |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Whisper-Large-v2 | 0.781942 [本文] (p. 4, Table 3) | 0.194716 [本文] (p. 4, Table 3) | 0.194250 [本文] (p. 4, Table 3) | 0.089993 [本文] (p. 4, Table 3) | 0.345741 [本文] (p. 4, Table 3) |
| Whisper-Large | 0.781314 [本文] (p. 4, Table 3) | 0.203542 [本文] (p. 4, Table 3) | 0.197882 [本文] (p. 4, Table 3) | 0.085657 [本文] (p. 4, Table 3) | 0.344999 [本文] (p. 4, Table 3) |
| Whisper-Large-v3 | 0.776689 [本文] (p. 4, Table 3) | 0.201399 [本文] (p. 4, Table 3) | 0.192961 [本文] (p. 4, Table 3) | 0.083822 [本文] (p. 4, Table 3) | 0.342214 [本文] (p. 4, Table 3) |
| Whisper-medium | 0.756563 [本文] (p. 4, Table 3) | 0.200798 [本文] (p. 4, Table 3) | 0.196831 [本文] (p. 4, Table 3) | 0.087710 [本文] (p. 4, Table 3) | 0.332443 [本文] (p. 4, Table 3) |
| WavLM-Large | 0.765474 [本文] (p. 4, Table 3) | 0.206174 [本文] (p. 4, Table 3) | 0.161098 [本文] (p. 4, Table 3) | 0.068182 [本文] (p. 4, Table 3) | 0.326108 [本文] (p. 4, Table 3) |
| CLAP Music & Speech | 0.743248 [本文] (p. 4, Table 3) | 0.215404 [本文] (p. 4, Table 3) | 0.148090 [本文] (p. 4, Table 3) | 0.055976 [本文] (p. 4, Table 3) | 0.309980 [本文] (p. 4, Table 3) |
| Hubert Large | 0.733036 [本文] (p. 4, Table 3) | 0.207492 [本文] (p. 4, Table 3) | 0.156504 [本文] (p. 4, Table 3) | 0.066509 [本文] (p. 4, Table 3) | 0.307769 [本文] (p. 4, Table 3) |
| MERT v1 330M | 0.707891 [本文] (p. 4, Table 3) | 0.211471 [本文] (p. 4, Table 3) | 0.127485 [本文] (p. 4, Table 3) | 0.049841 [本文] (p. 4, Table 3) | 0.287032 [本文] (p. 4, Table 3) |
| w2v-bert-2.0 | 0.668253 [本文] (p. 4, Table 3) | 0.211685 [本文] (p. 4, Table 3) | 0.141581 [本文] (p. 4, Table 3) | 0.061820 [本文] (p. 4, Table 3) | 0.268165 [本文] (p. 4, Table 3) |

**作者對結果的解讀**
- 域內：Whisper-Large-v2 平均最高、跨資料集變異低，原始 Whisper-Large 緊隨其後；Hubert Large、MERT v1 330M 與 w2v-bert-2.0 最低且波動較大 (p. 3)。
- 給定訓練資料集的域外表現：Whisper 系列最高；但不同訓練集間變異大，例如以 BAUM 訓練的域外泛化遠優於以 MELD 訓練 (p. 3, Fig. 2)。
- 未見資料集上的表現：EMOVO、MELD、MEAD 對未在其上訓練的模型最困難；作者稱模型對 URDU 與 AESDD 泛化最好 (p. 3, Fig. 3)。
- 整體：作者稱 Whisper 模型在所有指標上都最高，但標準差高，顯示表現依訓練／測試組合而變動很大，模型穩健性仍是挑戰 (p. 4)。
- 作者稱 logit adjustment 能處理資料集間類別分布不同的問題，確保公平比較 (p. 4)。

## 核心貢獻與作者觀點（Contributions & Insights）
- [作者聲稱] 提出大規模基準，評估 SER 模型在不同語言與情緒表達上的穩健性與泛化能力 (p. 1)。
- [作者聲稱] 蒐集多語言資料集，並建立供系統化域內與域外評估的子集 (p. 1)。
- [作者聲稱] 使用 logit adjustment（引用既有方法，非本篇提出）處理不同的類別分布，確保跨資料集公平比較 (p. 1)。
- [作者聲稱] 以最新語音表徵模型進行大量實驗，並分析其跨語言 SER 表現 (p. 1)。
- [作者聲稱] 開源完整程式碼、未縮減的完整結果與訓練紀錄 (p. 1)。
- [作者聲稱] 主要以 ASR 為目的的 Whisper 在跨語言 SER 上優於專用的 SSL 模型，挑戰「ASR 模型因專注音素辨識而不適合 SER」的常見看法 (p. 1)、(p. 3)、(p. 4)。
- [作者聲稱] 對每個特徵框執行 MLP 再平均預測，比先平均特徵保留更多資訊、結果更強更一致 (p. 2)。

## 論文提及之局限性（Limitations & Future Work）
- 高標準差顯示表現依訓練／測試組合而變動很大，模型穩健性仍待改進 (p. 4)。
- 不同訓練集的域外泛化差異大，哪些資料集特性帶來更好的泛化仍需研究 (p. 3)。
- 各資料集確切的標籤對應方式未寫在論文中，只放在開源程式碼裡 (p. 2)。
- 未來研究：探索領域適應、few-shot learning 與 meta-learning；研究哪些資料集特性有助泛化，以供資料集設計與選擇參考 (p. 4)。

## 提及實體清單（Referenced Entities）
- [[ser-evals]]（本篇核心貢獻）
- [[wav2vec2]]
- [[iemocap]]
- [[msp-podcast]]
- [[emo-db]]（本篇寫作 EmoDB／EmoDBDataset）
- [[self-supervised-learning]]
- Whisper（未達建頁門檻）
- HuBERT（未達建頁門檻）
- WavLM（未達建頁門檻）
- w2v-bert-2.0（未達建頁門檻）
- MERT（未達建頁門檻）
- CLAP（未達建頁門檻）
- logit adjustment（未達建頁門檻）
- macro-averaged F1（未達建頁門檻）
- 域內／域外評估（in-domain／out-of-domain）（未達建頁門檻）
- 跨語言 SER（cross-lingual SER）（未達建頁門檻）
- 多層感知器（MLP）（未達建頁門檻）
- label smoothing（未達建頁門檻）
- EMO-SUPERB、SERAB（其他 SER 基準，未達建頁門檻）
- [[mesd]]
- [[baum]]
- [[meld]]
- Table 1 中其餘資料集：URDU、EMOVO、eNTERFACE、MASC、DEMoS、CASIA、AESDD、EEKK、Thorsten、RESD、MEAD、CaFE、Expresso、ShEMO、SUBESCO（未達建頁門檻）

## 矛盾／待釐清
1. **URDU 與 AESDD 的域外泛化說法（論文內部，待核對）**：作者稱模型對 URDU 與 AESDD 泛化最好 (p. 3)，但 Table 1 標示這兩個資料集不具域外資格 (p. 1, Table 1)，Fig. 3 列出的資料集也不含這兩者 (p. 4, Fig. 3)。論文未說明這兩個資料集的域外表現從何而來。並列原文：
> "models generalize best to URDU and AESDD, indicating these datasets share more common features with others" (p. 3)
> "URDUDataset[10] 4 6 Urdu 400 2.5 No" (p. 1, Table 1)
> "AESDDDataset[18] 5 6 Greek 604 4.1 No" (p. 1, Table 1)
2. **對 [[2021-pepino-wav2vec2-ser]] 的引用脈絡（並列，不選邊）**：本篇把 Pepino 等人列為探討以 SSL 模型做跨語言 SER 的研究之一 (p. 1)、(p. 5)；[[2021-pepino-wav2vec2-ser]] 的實驗使用 IEMOCAP 與 RAVDESS，論文中未描述跨語言實驗。並列原文：
> "Several studies have explored the use of SSL models for cross-lingual SER [30, 4]." (p. 1)
3. **ASR 模型是否適合 SER：設定不同，不可直接比較**。本篇發現以 ASR 為主要目的的 Whisper 優於 SSL 模型 (p. 4)；[[2021-pepino-wav2vec2-ser]] 則發現微調做 ASR 的 Wav2vec2-FT 表現比未微調的 Wav2vec2-PT 差。兩篇的模型（Whisper vs. 微調後的 wav2vec 2.0）、資料集、切分與指標（macro-averaged F1 vs. 各類平均召回率）皆不同。
4. 三篇使用不同指標（本篇 macro-averaged F1；[[2021-pepino-wav2vec2-ser]] 各類平均召回率；[[2016-emoreact]] AUC ROC 與 skew normalized F1），數值不可互相比較。
