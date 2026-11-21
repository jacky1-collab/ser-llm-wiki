---
title: "EmoReact: A Multimodal Approach and Dataset for Recognizing Emotional Responses in Children"
authors: ["Behnaz Nojavanasghari", "Tadas Baltrušaitis", "Charles E. Hughes", "Louis-Philippe Morency"]
year: 2016
type: dataset
pdf: "raw/2016-emoreact.pdf"
one_sentence_summary: "介紹 EmoReact：從 YouTube 反應影片蒐集、以群眾外包標註多種情感狀態的兒童視聽情緒資料集，並分析最具指標性的視覺與聲學行為、提供單模態與多模態基線。"
---

# EmoReact: A Multimodal Approach and Dataset for Recognizing Emotional Responses in Children

## 基本資訊
- **篇名**：EmoReact: A Multimodal Approach and Dataset for Recognizing Emotional Responses in Children
- **作者**：Behnaz Nojavanasghari、Tadas Baltrušaitis、Charles E. Hughes、Louis-Philippe Morency（University of Central Florida；Carnegie Mellon University）
- **發表年份**：2016
- **發表會議／期刊**：ICMI’16, November 12–16, 2016, Tokyo, Japan
- **論文類型**：資料集（含基準實驗）
- **原始檔案**：raw/2016-emoreact.pdf

## 研究動機與欲解決問題（Problem & Motivation）
- 自動情緒辨識是社交機器人、情感感知人機互動設計與情感感知家教系統的核心技術 (p. 1)。
- 成人情緒辨識研究已多，兒童情緒辨識則研究不足 (p. 1)：
> "emotion recognition in children has been understudied" (p. 1)
- 作者認為兒童的情緒辨識更具挑戰性 (p. 1)：
> "children tend to fidget and move around more than adults, leading to more self-occlusions and non-frontal head poses" (p. 1)
> "the lack of publicly available datasets for children with annotated emotion labels leads most researchers to focus on adults" (p. 1)
- 作者列出三項挑戰：快速動作、臉部遮擋、缺乏資源 (p. 2)：
> "There are few publicly available datasets of children; only one contains videos and all other ones contain only images." (p. 2)
- 其中關於快速動作的挑戰 (p. 2)：
> "Children move more compared to adults, which makes it challenging to successfully track their face and body gestures." (p. 2)
- 現有唯一含影片的兒童資料集 MMDB 以幼兒為對象，作者認為難以分析語音通道 (p. 2)：
> "as the subjects are toddlers, this makes it hard to analyze the vocal channel due to their very limited vocabularies" (p. 2)
- 部分現有資料集要求兒童擺出指定表情 (p. 2)：
> "children have been asked to pose the desired emotion, and so the expression of emotions might not be natural and lack variability" (p. 2)
- 作者也提到遠距教育與合作學習情境，情緒辨識有助於理解兒童的學習 (pp. 1–2)。

## 方法與架構（Methodology & Architecture）
**資料蒐集**
- 來源：從 YouTube 的 React 頻道下載兒童對不同主題做出反應的影片 (p. 2)。
- 兒童年齡與背景 (p. 3)：
> "children between the ages of four to fourteen years old, from different races and both genders" (p. 3)
- 影片中兒童對 37 個主題 [本文] (p. 3) 做出反應，包括食物、科技、YouTube 影片與遊戲裝置 (p. 3)。
- 影片中兒童執行的任務 (p. 3)：
> "children performed the following five tasks" (p. 3)
- 這些任務為：認識主題、被問問題、回答問題、被告知事實並做出反應、說明自己的看法 (p. 3)。
- 切分：以 ELAN 手動切成短片段，使每段只含一位兒童對單一主題的反應 (p. 3)：
> "with an average length of five seconds" (p. 3)
> "we kept only the videos that are longer than three seconds resulting in a total of 1254 clips" (p. 3)
- 身分標註：標註每段影片中兒童的身分，以支援 person-independent 與 person-specific 分析；論文寫作「Florian et al」的方法（參考文獻列為 FaceNet）(p. 3)、(p. 8)，再經人工檢查與校正 (p. 3)。
- 結果為 63 位兒童 [本文] (p. 3)，其中女性 32 [本文] (p. 3)、男性 31 [本文] (p. 3)。

**情緒標註**
- 標籤選擇著重於對學習與教育重要的情感狀態 (p. 3)。
- 標籤共 17 種 [本文] (p. 2)：
> "including six basic emotions (happiness, sadness, surprise, fear, disgust, and anger), neutral, valence and nine complex emotions" (p. 2)
- 九種複雜情緒為 curiosity、uncertainty、excitement、attentiveness、exploration、confusion、anxiety、embarrassment、frustration (p. 2)。
- 標註者另標註兒童性別，並判斷反應的自然程度 (p. 3)。
- 標註者來自群眾外包平台 Amazon Mechanical Turk（MTurk），先以預研究篩選 (p. 3)：
> "For the pre-study we hired nine different workers" (p. 3)
> "We divided the workers into three groups and assigned 20 videos to each group." (p. 3)
> "we hired two groups out of three initial groups for our main study" (p. 3)
> "The final set of six workers included three female and three male workers to reduce gender bias" (p. 3)
> "Each video was annotated by three independent workers for seventeen labels." (p. 3)
- 標註介面附各標籤定義；並以兒童性別題作為警覺性測試，用來剔除隨機作答 (p. 3)。
- 量表：除 valence 外，各情緒以 1 [本文] (p. 3) 至 4 [本文] (p. 3) 的 Likert 量表標註；1 [本文] (p. 3) 表示沒有該情緒，4 [本文] (p. 3) 表示強烈出現，2 [本文] (p. 3) 與 3 [本文] (p. 3) 分別表示少量與中等 (p. 3)。
- valence 以 1 [本文] (p. 3) 至 7 [本文] (p. 3) 標註，1 [本文] (p. 3) 為最負面、7 [本文] (p. 3) 為最正面 (p. 3)。
- 一致性：以 Krippendorff's alpha 評估標註者間一致性；移除 152 [本文] (p. 3) 部看似標註者不夠警覺的影片，最終為 1102 [本文] (p. 3) 部 (p. 3)。
- 每部影片可有多個情緒標籤，並分析情緒共同出現的比例 (p. 4, Fig. 2)。
- 後續分析與實驗只使用一致性最高的標籤 (p. 3)：
> "We decided to use the eight emotion labels that reached the highest levels in coder agreement (greater than 0.4)" (p. 3)

**多模態行為分析**
- 「出現」某情緒的定義 (p. 4)：
> "presence of an emotion label is defined as at least two workers agreeing that it is present (above or equal to two on a four-point Likert scale)" (p. 4)
- 以 t 檢定比較情緒出現與未出現的片段，依特徵數做多重比較校正，並以 Hedges' g 報告效果量 (p. 4)。
- 視覺特徵：臉部動作單元（Facial Action Units）、頭部位置與方向、非剛性形狀參數（對臉部特徵點做 PCA）(p. 4)。
- 聲學特徵（依先前研究選取）(p. 4)：
  - 嗓音品質特徵（voice quality features）：NAQ、PSP、MDQ、QOQ、H1-H2、peak-slope，用以衡量語音的 pressedness、tenseness、creakiness 或 breathiness (p. 4)。
  - 韻律（prosody）：
> "Pitch/Fundamental Frequency (F0) indicates the pitch information in one" (p. 4)
  - MFCC：使用 MFCC 第 1 [本文] (p. 5) 至 24 [本文] (p. 5) 維 (p. 5)。
  - 有聲段統計（VUV），用以表示每段影片的說話長度 (p. 5)。

## 實驗設定（Experimental Setup）
- 特徵擷取：
  - 以 OpenFace 擷取視覺特徵，只使用成功偵測到臉且接近正面的影格；共 72.88% [本文] (p. 5) 的影格成功處理 (p. 5)。
  - 以 COVAREP 擷取聲學特徵，在有聲段每 10 毫秒 [本文] (p. 5) 計算；共 76.52% [本文] (p. 5) 的影片有有效語音訊號 (p. 5)。
  - 以平均值與標準差把短時窗特徵彙總為整部影片的特徵 (p. 5)。
- 基線模型：Naive Bayes、linear SVM、RBF kernel SVM，分別使用視覺、聲學與視聽特徵 (p. 5)。
- 資料切分（person-independent）：訓練集 432 [本文] (p. 5) 部、驗證集 303 [本文] (p. 5) 部、測試集 367 [本文] (p. 5) 部；每個集合中的情緒由 21 位 [本文] (p. 5) 不同兒童表現，三個集合的情緒分布相近 (p. 5)。
- 超參數：以驗證集選擇 SVM 的 γ 與 C (p. 6)。PDF 抽字時指數上標被攤平，搜尋範圍無法可靠辨識，本 Wiki 不轉錄其數值。
- 類別不平衡的處理 (p. 6)：
> "To address the challenge of imbalanced emotion labels we followed two approaches: (1) under-sampling negative examples, and (2) using an ensemble classifier." (p. 6)
- 隨機選取與正例等量的負例，重複 100 次 [本文] (p. 6) 建立平衡訓練集，各訓練一個模型，再以簡單多數決整合 (p. 6)。
- 多模態融合：early fusion（串接視覺與聲學特徵）、late fusion（視覺與聲學分類器 ensemble 之間多數決）、hybrid fusion（視覺、聲學、視聽分類器 ensemble 之間多數決）(p. 6)。
- 指標：ROC 曲線下面積（AUC ROC）與 skew normalized F1 (p. 6)。
- 比較對象：majority voting 與隨機猜測分類器 (p. 6)。

## 核心數據與成果（Key Results & Metrics）
**Table 1：EmoReact 與其他公開兒童資料集比較**（EmoReact 欄為本文資料；其他資料集為本篇整理的他人資料，標 [引述]）
| 項目 | EmoReact | MMDB | CAFE | Radboud | NIMH | Dartmouth |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 模態 | A/V | A/V/P | I | I | I | I |
| 樣本數 | 1102 [本文] (p. 2, Table 1) 影片 | 160 [引述] (p. 2, Table 1) 影片 | 1192 [引述] (p. 2, Table 1) 圖片 | 80 [引述] (p. 2, Table 1) 圖片 | 482 [引述] (p. 2, Table 1) 圖片 | 640 [引述] (p. 2, Table 1) 圖片 |
| 兒童數 | 63 [本文] (p. 2, Table 1) | 121 [引述] (p. 2, Table 1) | 154 [引述] (p. 2, Table 1) | 10 [引述] (p. 2, Table 1) | 59 [引述] (p. 2, Table 1) | 80 [引述] (p. 2, Table 1) |
| 標籤數 | 17 [本文] (p. 2, Table 1) | 2 [引述] (p. 2, Table 1) | 7 [引述] (p. 2, Table 1) | 8 [引述] (p. 2, Table 1) | 5 [引述] (p. 2, Table 1) | 8 [引述] (p. 2, Table 1) |
| 女性比例 | 51% [本文] (p. 2, Table 1) | 表中為「-」 | 58% [引述] (p. 2, Table 1) | 60% [引述] (p. 2, Table 1) | 63% [引述] (p. 2, Table 1) | 50% [引述] (p. 2, Table 1) |
| 年齡範圍 | 4 [本文] (p. 2, Table 1) 至 14 [本文] (p. 2, Table 1) | 1 [引述] (p. 2, Table 1) 至 2 [引述] (p. 2, Table 1) | 2 [引述] (p. 2, Table 1) 至 8 [引述] (p. 2, Table 1) | 8 [引述] (p. 2, Table 1) 至 12 [引述] (p. 2, Table 1) | 10 [引述] (p. 2, Table 1) 至 17 [引述] (p. 2, Table 1) | 6 [引述] (p. 2, Table 1) 至 16 [引述] (p. 2, Table 1) |

表中縮寫：A 為 audio、V 為 video、P 為 physiological、I 為 images (p. 2, Table 1)。

**各標籤的 Krippendorff's alpha (p. 3)**
- Happiness 0.57 [本文] (p. 3)；Surprise 0.63 [本文] (p. 3)；Disgust 0.61 [本文] (p. 3)；Fear 0.43 [本文] (p. 3)
- Curiosity 0.41 [本文] (p. 3)；Uncertainty 0.47 [本文] (p. 3)；Excitement 0.43 [本文] (p. 3)；Frustration 0.54 [本文] (p. 3)
- Exploration 0.24 [本文] (p. 3)；Confusion 0.29 [本文] (p. 3)；Anxiety 0.31 [本文] (p. 3)；Attentiveness -0.16 [本文] (p. 3)
- Anger 0.28 [本文] (p. 3)；Sadness 0.23 [本文] (p. 3)；Embarrassment 0.09 [本文] (p. 3)；Valence 0.65 [本文] (p. 3)；Neutral 0.37 [本文] (p. 3)
- 論文引用的判讀標準：0.4 [本文] (p. 3) 至 0.6 [本文] (p. 3) 為中等一致，0.6 [本文] (p. 3) 至 0.8 [本文] (p. 3) 為高度一致 (p. 3)。

**Table 2：各情緒的影片數與表現該情緒的兒童數**
| 情緒 | 影片數 | 兒童數 |
| :--- | :--- | :--- |
| Curiosity | 385 [本文] (p. 3, Table 2) | 51 [本文] (p. 3, Table 2) |
| Uncertainty | 344 [本文] (p. 3, Table 2) | 53 [本文] (p. 3, Table 2) |
| Excitement | 355 [本文] (p. 3, Table 2) | 49 [本文] (p. 3, Table 2) |
| Happiness | 604 [本文] (p. 3, Table 2) | 60 [本文] (p. 3, Table 2) |
| Surprise | 298 [本文] (p. 3, Table 2) | 49 [本文] (p. 3, Table 2) |
| Disgust | 137 [本文] (p. 3, Table 2) | 35 [本文] (p. 3, Table 2) |
| Fear | 50 [本文] (p. 3, Table 2) | 20 [本文] (p. 3, Table 2) |
| Frustration | 131 [本文] (p. 3, Table 2) | 31 [本文] (p. 3, Table 2) |

**Table 3：各情緒最具預測力的視覺行為（Hedges' g）**
表中所有行為的校正後 p 值皆小於 0.001 [本文] (p. 4)。Stat 欄的 µ、δ 照錄論文表中符號，論文未在表中定義 (p. 5, Table 3)。
| 情緒 | 特徵 | Stat | Hedges' g |
| :--- | :--- | :--- | :--- |
| Curiosity | HeadRot(rx) | µ | -0.54 [本文] (p. 5, Table 3) |
| Curiosity | H Gaze shift | µ | 0.48 [本文] (p. 5, Table 3) |
| Uncertainty | Scale | δ | -0.26 [本文] (p. 5, Table 3) |
| Uncertainty | HeadTrans(tx) | δ | 0.22 [本文] (p. 5, Table 3) |
| Excitement | Lip corner puller | δ | 0.42 [本文] (p. 5, Table 3) |
| Excitement | Lip Stretcher | δ | 0.34 [本文] (p. 5, Table 3) |
| Excitement | Cheek raiser | δ | 0.28 [本文] (p. 5, Table 3) |
| Happiness | HeadRot(rz) | µ | -0.29 [本文] (p. 5, Table 3) |
| Happiness | Upper lip raiser | δ | -0.22 [本文] (p. 5, Table 3) |
| Surprise | Lip corner puller | δ | -0.38 [本文] (p. 5, Table 3) |
| Surprise | Upper lip raiser | µ | -0.25 [本文] (p. 5, Table 3) |
| Disgust | V Gaze shift | δ | 0.48 [本文] (p. 5, Table 3) |
| Disgust | HeadRot(rz) | δ | -0.43 [本文] (p. 5, Table 3) |
| Disgust | Lip stretcher | δ | 0.35 [本文] (p. 5, Table 3) |
| Disgust | Nose wrinkler | µ | 0.33 [本文] (p. 5, Table 3) |
| Disgust | Upper lid raiser | µ | 0.33 [本文] (p. 5, Table 3) |
| Fear | Non-rigid P 22 | µ | 0.55 [本文] (p. 5, Table 3) |
| Fear | Non-rigid P 8 | δ | -0.54 [本文] (p. 5, Table 3) |
| Frustration | HeadRot(rx) | µ | -0.72 [本文] (p. 5, Table 3) |
| Frustration | Lip corner puller | µ | -0.42 [本文] (p. 5, Table 3) |

- Fear 的兩個非剛性參數分別對應睜大眼睛與張開嘴巴 (p. 5, Table 3)。
- 作者認為頭部方向與動作單元是區分這些情緒最有效的行為 (p. 4)。

**Table 4：各情緒最具預測力的聲學行為（Hedges' g）**
表中所有行為的校正後 p 值皆小於 0.001 [本文] (p. 5)。
| 情緒 | 特徵 | Stat | Hedges' g |
| :--- | :--- | :--- | :--- |
| Curiosity | MFCC 14 | δ | -0.44 [本文] (p. 5, Table 4) |
| Curiosity | H1H2 | δ | -0.35 [本文] (p. 5, Table 4) |
| Curiosity | QOQ | µ | 0.31 [本文] (p. 5, Table 4) |
| Uncertainty | MFCC 14 | δ | -0.35 [本文] (p. 5, Table 4) |
| Uncertainty | H1H2 | δ | -0.28 [本文] (p. 5, Table 4) |
| Excitement | QOQ | δ | 0.70 [本文] (p. 5, Table 4) |
| Excitement | F0 | µ | 0.50 [本文] (p. 5, Table 4) |
| Happiness | MFCC 3 | µ | 0.24 [本文] (p. 5, Table 4) |
| Happiness | PSP | δ | 0.22 [本文] (p. 5, Table 4) |
| Surprise | MFCC 10 | µ | 0.48 [本文] (p. 5, Table 4) |
| Surprise | VUV | δ | 0.40 [本文] (p. 5, Table 4) |
| Surprise | PSP | δ | -0.39 [本文] (p. 5, Table 4) |
| Disgust | MDQ | µ | -0.70 [本文] (p. 5, Table 4) |
| Disgust | MFCC 21 | δ | -0.63 [本文] (p. 5, Table 4) |
| Disgust | F0 | µ | 0.60 [本文] (p. 5, Table 4) |
| Fear | F0 | µ | 0.81 [本文] (p. 5, Table 4) |
| Fear | MDQ | µ | -0.69 [本文] (p. 5, Table 4) |
| Frustration | MFCC 15 | δ | 0.68 [本文] (p. 5, Table 4) |
| Frustration | F0 | µ | 0.40 [本文] (p. 5, Table 4) |

- 作者指出對這組情緒影響最大的聲學行為是 MFCC、嗓音品質特徵（H1H2、MDQ）與韻律特徵 (p. 5)。
- 在 fear 與 disgust 出現時，MDQ 平均較低、音高平均較高，作者解讀為緊繃、嘎裂的嗓音與較高的嗓音能量 (p. 5)。

**Table 5：基線模型在各情緒上的平均表現**
| 方法 | Audio AUC ROC | Audio F1 | Visual AUC ROC | Visual F1 | Audio-Visual AUC ROC | Audio-Visual F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Majority voting | 0.50 [本文] (p. 6, Table 5) | 未定義 | 0.50 [本文] (p. 6, Table 5) | 未定義 | 0.50 [本文] (p. 6, Table 5) | 未定義 |
| Random | 0.50 [本文] (p. 6, Table 5) | 0.50 [本文] (p. 6, Table 5) | 0.50 [本文] (p. 6, Table 5) | 0.50 [本文] (p. 6, Table 5) | 0.50 [本文] (p. 6, Table 5) | 0.50 [本文] (p. 6, Table 5) |
| Naive Bayes | 0.57 [本文] (p. 6, Table 5) | 0.55 [本文] (p. 6, Table 5) | 0.59 [本文] (p. 6, Table 5) | 0.57 [本文] (p. 6, Table 5) | 0.61 [本文] (p. 6, Table 5) | 0.61 [本文] (p. 6, Table 5) |
| Linear SVM | 0.61 [本文] (p. 6, Table 5) | 0.66 [本文] (p. 6, Table 5) | 0.62 [本文] (p. 6, Table 5) | 0.66 [本文] (p. 6, Table 5) | 0.63 [本文] (p. 6, Table 5) | 0.65 [本文] (p. 6, Table 5) |
| RBF SVM | 0.61 [本文] (p. 6, Table 5) | 0.69 [本文] (p. 6, Table 5) | 0.62 [本文] (p. 6, Table 5) | 0.68 [本文] (p. 6, Table 5) | 0.64 [本文] (p. 6, Table 5) | 0.69 [本文] (p. 6, Table 5) |

- 表注說明 skew normalized F1 對 majority voting 沒有定義 (p. 6, Table 5)。
- 基線模型在兩種指標上皆優於 majority voting 與隨機分類器；兩種 SVM 皆優於 Naive Bayes，RBF SVM 略優於 linear SVM (p. 6)。
- 視覺與聲學模態比較：fear 與 surprise 以聲學行為預測較佳；frustration 與 excitement 以視覺行為預測較佳 (p. 6, Fig. 3)。
- 單模態與多模態比較：多數多模態方法優於單模態 (p. 7, Fig. 4)；early、late、hybrid fusion 表現相近 (p. 7)。

## 核心貢獻與作者觀點（Contributions & Insights）
- [作者聲稱] 提出新蒐集的兒童多模態情緒資料集 EmoReact，作者稱是同類中最大的資料集 (p. 2)：
> "EmoReact is the largest dataset of its kind both in size of data and number of annotated emotion labels." (p. 2, Table 1)
- [作者聲稱] 據作者所知，EmoReact 是第一個涵蓋廣泛兒童年齡範圍、並以多種情感狀態標註的多模態資料集 (p. 2)。
- [作者聲稱] 標註一致性與先前情感運算研究相比表現良好 (p. 3)。
- [作者聲稱] 提供兒童表達情緒時最具指標性的視覺與聲學行為的詳細分析 (p. 7)。
- [作者聲稱] 提供單模態與多模態基線，作為 EmoReact 後續研究的基線 (p. 7)。
- [作者聲稱] 各模態在預測特定情緒上各有優勢且可互補；不同多模態方法表現相近，但都比單模態更成功 (p. 7)。
- [作者聲稱] 每個情緒都由大量不同兒童表現，有助於建立能泛化到未見個體的模型 (p. 3)。
- [作者聲稱] 資料集將公開 (p. 2)。

## 論文提及之局限性（Limitations & Future Work）
- 視覺分類器可能受張嘴、臉部遮擋、快速動作等影響；例如 fear 時兒童會遮住嘴、surprise 時常張嘴 (p. 6)。
- 音訊可能受不想要的聲音影響，例如說話時掉落物品或背景音樂；這些都可能造成臉部追蹤、動作單元辨識與聲學特徵的雜訊 (pp. 6–7)。
- 未來研究：作者計畫為 EmoReact 加上字幕，讓語言模態的研究成為可能；也想探討性別對兒童情緒表達的影響 (p. 7)。

## 提及實體清單（Referenced Entities）
- [[emoreact]]（本篇核心貢獻）
- [[children-emotion-recognition]]
- [[pitch]]（本篇寫作 Pitch/Fundamental Frequency）
- MMDB、CAFE、Radboud、NIMH、Dartmouth（兒童臉部或影片資料集，未達建頁門檻）
- Amazon Mechanical Turk 群眾外包標註（未達建頁門檻）
- Krippendorff's alpha（未達建頁門檻）
- Likert 量表（未達建頁門檻）
- Hedges' g（未達建頁門檻）
- 臉部動作單元（Facial Action Units）（未達建頁門檻）
- OpenFace（未達建頁門檻）
- COVAREP（未達建頁門檻）
- 嗓音品質特徵（voice quality features：NAQ、PSP、MDQ、QOQ、H1-H2、peak-slope）（未達建頁門檻）
- [[mfcc]]
- Naive Bayes、linear SVM、RBF SVM（未達建頁門檻）
- 多數決（majority voting，本篇為基線分類器與 ensemble 整合方式）（未達建頁門檻）
- early／late／hybrid fusion（未達建頁門檻）
- AUC ROC（未達建頁門檻）
- skew normalized F1（未達建頁門檻）
- valence（未達建頁門檻）
- 基本情緒與複雜情緒標籤（未達建頁門檻）

## 矛盾／待釐清
1. **Valence 未被選入（論文未說明）**：論文稱選用一致性高於 0.4 [本文] (p. 3) 的標籤，但 Valence 的一致性為 0.65 [本文] (p. 3)，高於所選的部分標籤，卻不在後續使用的標籤之列（Table 2 只列出所選的情緒，不含 Valence）(p. 3, Table 2)。論文未說明原因。並列原文：
> "We decided to use the eight emotion labels that reached the highest levels in coder agreement (greater than 0.4)" (p. 3)
> "Valence: 0.65" (p. 3)
2. **與 [[2008-fau-aibo]] 的兒童語料：設定不同，不可直接比較**。
   - [[2008-fau-aibo]]：德國兒童在綠野仙蹤情境中對機器人說話，只有語音，以詞為單位標註（年齡與人數見 [[fau-aibo]]）。
   - 本篇：從 YouTube 影片蒐集，視聽雙模態，年齡 4 [本文] (p. 2, Table 1) 至 14 歲 [本文] (p. 2, Table 1)，以片段為單位、可多標籤，由群眾外包標註 (pp. 2–3)。
   - 兩篇的標註一致性指標也不同：[[2008-fau-aibo]] 為 AMEN 子集的加權 kappa，本篇為各標籤的 Krippendorff's alpha。
3. **兒童公開資料集的現況（並列，不選邊）**：本篇稱公開的兒童資料集很少、只有一個含影片 (p. 2)，其 Table 1 比較的資料集未包含 [[fau-aibo]] (p. 2, Table 1)；[[2008-fau-aibo]] 則表示 FAU Aibo 將釋出供科學使用（見該頁）。本篇未提及 FAU Aibo，兩篇也都未說明 FAU Aibo 在本篇發表時的實際公開狀態。
