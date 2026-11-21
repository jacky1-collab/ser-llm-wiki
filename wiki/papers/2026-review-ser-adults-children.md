---
title: "Speech emotion recognition in adults and children: a comprehensive review of traditional features and raw waveform models"
authors: ["Sai Rekha Gudivaka", "Pranuthi Polipogu", "Radha Kodali", "Venkata Rao Dhulipalla", "Venkata Siva Kishor Tatavarty", "Jahnavi Penumudi", "Pradeep Reddy Gogulamudi"]
year: 2026
type: survey
pdf: "raw/2026-review-ser-adults-children.pdf"
one_sentence_summary: "回顧成人與兒童語音情緒辨識中傳統手工特徵與原始波形模型的研究，比較兩個族群的資料集、特徵與模型，並指出兒童語音情緒辨識在資料集與原始波形建模上的研究缺口。"
---

# Speech emotion recognition in adults and children: a comprehensive review of traditional features and raw waveform models

## 基本資訊
- **篇名**：Speech emotion recognition in adults and children: a comprehensive review of traditional features and raw waveform models
- **作者**：Sai Rekha Gudivaka、Pranuthi Polipogu、Radha Kodali、Venkata Rao Dhulipalla、Venkata Siva Kishor Tatavarty、Jahnavi Penumudi、Pradeep Reddy Gogulamudi
- **發表年份**：2026（Published online: 13 January 2026）
- **發表會議／期刊**：International Journal of Speech Technology (2026) 29:21
- **論文類型**：綜述
- **原始檔案**：raw/2026-review-ser-adults-children.pdf

## 研究動機與欲解決問題（Problem & Motivation）
- 現有 SER 研究大多集中於成人，兒童受到的關注有限 (p. 1)：
> "most existing studies focus heavily on adults, with limited attention given to children" (p. 1)
- 作者認為兒童情緒偵測有獨特挑戰：標註資料有限、聲音模式持續變化、兒童情緒的動態性 (p. 1)。
- 作者認為兒童的情緒範圍較窄且變異較大，受年齡、語言發展與文化影響；加上隱私與同意等倫理要求，難以建立標準化資料集 (p. 2)。
- 作者歸納兒童 SER 的其他挑戰：音高、音色、音量差異，常見發音錯誤與不完整句子，重疊的聲學模式（如 happiness vs. excitement），快速的情緒轉換，以及強烈的說話者依賴性 (p. 2)。
- 作者指出現有研究較少處理三個面向：自然或吵雜環境下的穩健性、多模態分析、聲學與語言資訊融合；這些在兒童研究中尤其缺乏 (p. 2)。
- 作者認為先前的綜述沒有一篇同時統整成人與兒童的傳統特徵與原始波形方法 (p. 3)。
- **文獻篩選方法**（綜述自述）(p. 4)：
  - 資料庫：IEEE Xplore、PubMed、Scopus、ACM Digital Library、SpringerLink。
  - 涵蓋期間：2014 [本文] (p. 4) 至 2025 [本文] (p. 4) 年。
  - 關鍵字：如 "speech emotion recognition"、"SER"、"children"、"adults"、"traditional features"、"handcrafted features"、"raw-waveform"、"deep learning"，並使用布林組合。
  - 納入條件：聚焦成人及／或兒童的 SER；使用傳統特徵方法或原始波形建模；使用機器學習或深度學習架構；發表於同儕審查期刊、會議論文集或書籍章節。
  - 品質評估：先依標題與摘要篩選，再全文評估；排除缺乏清楚實驗設計或細節不足的研究。
  - 論文未說明最終納入的文獻總篇數。

## 方法與架構（Methodology & Architecture）
不適用（綜述無自研方法）。

## 實驗設定（Experimental Setup）
不適用（綜述無自研實驗）。

## 核心數據與成果（Key Results & Metrics）
**綜述自己的統計**
- 綜述稱成人 SER 共有 15 個 [本文] (p. 21) 資料集在前文章節與表格中提及；專門針對兒童 SER 的資料集只有 7 個 [本文] (p. 21)。

**兒童資料集（Table 3，綜述轉述各資料集原始文獻；僅摘錄，完整表格見 (p. 9, Table 3)）**
| 名稱（綜述引用來源） | 建立年 | 規模 | 語言 | 說話者（男／女） | 年齡 | 情緒數 | 取得方式 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FAU-AIBO（Batliner et al.） | 2006 [引述] (p. 9, Table 3) | 17074 [引述] (p. 9, Table 3) utterances | German | 51 [引述] (p. 9, Table 3)（21 [引述] (p. 9, Table 3)／30 [引述] (p. 9, Table 3)） | 10 [引述] (p. 9, Table 3) 至 13 [引述] (p. 9, Table 3) | 10 [引述] (p. 9, Table 3) | Licensed |
| EmoReact（Rajan et al.） | 2016 [引述] (p. 9, Table 3) | 1102 [引述] (p. 9, Table 3) utterances | German | 63 [引述] (p. 9, Table 3)（31 [引述] (p. 9, Table 3)／32 [引述] (p. 9, Table 3)） | 4 [引述] (p. 9, Table 3) 至 14 [引述] (p. 9, Table 3) | 15 [引述] (p. 9, Table 3) | Licensed |
| MESD（Duville et al.） | 2021 [引述] (p. 9, Table 3) | 288 [引述] (p. 9, Table 3) utterances | Spanish | 6 [引述] (p. 9, Table 3) | 8 [引述] (p. 9, Table 3) 至 11 [引述] (p. 9, Table 3) | 6 [引述] (p. 9, Table 3) | Free |

**成人資料集（Table 2，綜述轉述；僅摘錄與前幾篇重疊者，完整表格見 (p. 7, Table 2)）**
| 名稱 | 建立年 | 規模 | 語言 | 說話者（男／女） | 情緒數 | 取得方式 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| EmoDB | 2005 [引述] (p. 7, Table 2) | 535 [引述] (p. 7, Table 2) utterances | German | 10 [引述] (p. 7, Table 2)（5 [引述] (p. 7, Table 2)／5 [引述] (p. 7, Table 2)） | 7 [引述] (p. 7, Table 2) | Free |
| IEMOCAP | 2008 [引述] (p. 7, Table 2) | 7433 [引述] (p. 7, Table 2) utterances | English | 10 [引述] (p. 7, Table 2) | 10 [引述] (p. 7, Table 2) | Free |
| SAVEE | 2008 [引述] (p. 7, Table 2) | 480 [引述] (p. 7, Table 2) utterances | English | 4 [引述] (p. 7, Table 2) | 6 [引述] (p. 7, Table 2) | Free |
| RAVDESS | 2018 [引述] (p. 7, Table 2) | 7356 [引述] (p. 7, Table 2) files | English | 24 [引述] (p. 7, Table 2)（12 [引述] (p. 7, Table 2)／12 [引述] (p. 7, Table 2)） | 7 [引述] (p. 7, Table 2) | Free |
| MELD | 2018 [引述] (p. 7, Table 2) | 約 13000 [引述] (p. 7, Table 2) utterances | English | 407 [引述] (p. 7, Table 2) | 7 [引述] (p. 7, Table 2) | Free |

綜述 Table 2 另列 BAUM 的資料集，其表中名稱含數字，見下列原文 (p. 7, Table 2)：
> "BAUM-1 (Zhalehpour et al., 2017) 2016 1184 utterances Turkish 31 (18/13) 18–66 13 Free" (p. 7, Table 2)

**兒童 SER 研究結果（綜述轉述他人結果，皆為 FAU-AIBO；僅摘錄，完整表格見 (p. 18, Table 5)）**
- 綜述轉述 Wen 等人：以 RDBN 在 FAU 資料庫的辨識準確率為 42.2% [引述] (p. 17)。
- 綜述轉述 Hsiao 與 Chen：以 mel spectrograms 搭配 DRNN，UAR 為 46.3% [引述] (p. 17)。
- 綜述轉述 Latif 等人：以 eGeMAPS 特徵集搭配 DBN，在 FAU-AIBO 的準確率為 74.11% [引述] (p. 17)。
- 綜述轉述 Cao 等人：以 CNN-BiLSTM 達到 71.6% [引述] (p. 17) 準確率。
- 綜述轉述 Maximos 與 Suendermann-Oeft：以 MFCC 與 ZCR 等手工特徵，UAR 為 69.39% [引述] (p. 17)。
- 綜述轉述 Heracleous 等人：以原始波形的 DNN 與 DCNN，UAR 分別為 61.1% [引述] (p. 17) 與 59.2% [引述] (p. 17)。
- Table 5 中上述 FAU-AIBO 研究的使用量多寫為 18216 [引述] (p. 18, Table 5) utterances。
- 綜述轉述 Rao 等人：在 Child-BESD 上以手工特徵融合後輸入 CNN，準確率為 75.98% [引述] (p. 19)。

**成人 SER 研究結果（僅摘錄與前幾篇重疊者，完整表格見 (pp. 13–15)）**
- 綜述轉述 Sarma 等人：在 IEMOCAP 以 DNN 與 TDNN-LSTM，A 為 70.1 [引述] (p. 14, Table 4)、R 為 60.7 [引述] (p. 14, Table 4)。

## 核心貢獻與作者觀點（Contributions & Insights）
- [作者聲稱] 聚焦回顧 SER 的近期進展，特別是深度學習技術在成人與兒童情緒辨識上的應用 (p. 4)。
- [作者聲稱] 比較手工特徵方法與原始波形建模方法 (p. 4)。
- [作者聲稱] 統整 2014 [本文] (p. 4) 至 2025 [本文] (p. 4) 年的 SER 研究，涵蓋資料集趨勢、建模技術與應用領域 (p. 4)。
- [作者聲稱] 指出兒童 SER 的重大研究缺口，特別是原始波形模型的應用 (p. 4)、(p. 23)。
- [作者聲稱] MFCC 是研究者最常用的特徵 (p. 6)。
- [作者聲稱] CNN 是 SER 中最廣泛使用的深度神經網路模型 (p. 17)。
- [作者聲稱] 成人 SER 以頻譜特徵表現最好，兒童 SER 則更依賴音高、能量變化與強度等特徵，或與頻譜特徵結合 (p. 21)。
- [作者聲稱] 在兒童 SER 任務中，手工特徵方法目前優於原始波形模型 (p. 22)。
- [作者聲稱] 兒童 SER 需要混合架構、動態 RNN，以及遷移學習等策略來處理變異性與資料不足 (p. 22)。

## 論文提及之局限性（Limitations & Future Work）
- 論文未明確說明綜述本身的局限性；也未說明最終納入的文獻篇數 (p. 4)。
- 作者提出的未來方向 (p. 22)：
  - 擴充並多樣化兒童語音資料集，並處理隱私與同意等倫理議題。
  - 進階深度學習架構（DBN、RNN、CNN 與 RNN 混合），但須權衡過擬合與計算成本。
  - 原始波形建模在兒童 SER 的應用仍有限，混合原始波形與結構化特徵的模型是有前景的方向。
  - 非監督與自監督學習，用以從未標註資料學習。
  - 跨領域遷移學習：利用成人資料預訓練的模型，但須處理成人與兒童之間的領域差異。

## 提及實體清單（Referenced Entities）
- [[children-emotion-recognition]]
- [[fau-aibo]]（綜述寫作 FAU-AIBO）
- [[emoreact]]
- [[emo-db]]（綜述寫作 EmoDB／Emo-DB）
- [[iemocap]]
- [[ravdess]]
- [[savee]]
- [[meld]]
- [[mesd]]
- [[baum]]
- [[des]]
- [[pitch]]
- [[mfcc]]
- [[egemaps]]
- [[spectrogram]]
- [[transfer-learning]]
- [[self-supervised-learning]]
- 原始波形建模（raw waveform modeling）（未達建頁門檻）
- 手工特徵：倒頻譜、頻譜、音調描述子（GFCC、LPCC、PLP、TECC 等）（未達建頁門檻）
- CNN、RNN、LSTM、GRU、DBN（未達建頁門檻）
- UAR（未達建頁門檻）
- 其他資料集：TESS、RECOLA、SITB-OSED、CREMA-D、EmoFilm、LSSED、EmoWisconsin、EmoChildRu、IESC-Child、Child-BESD（未達建頁門檻）

## 矛盾／待釐清
1. **FAU Aibo 的描述與 [[2008-fau-aibo]] 不同（並列，不選邊）**：
   - 一致處：兒童人數、男女人數與年齡範圍，與 [[fau-aibo]] 頁記載相同。
   - 規模：綜述寫 17074 [引述] (p. 9, Table 3) utterances；[[2008-fau-aibo]] 以詞與 turn 計數（見 [[fau-aibo]]），未出現此數字。綜述 Table 5 中 FAU-AIBO 研究的使用量則多寫為 18216 [引述] (p. 18, Table 5)，與綜述自己的 Table 3 也不同。
   - 建立年：綜述寫 2006 [引述] (p. 9, Table 3)；[[2008-fau-aibo]] 寫的蒐集與標註年份與此不同（見該頁）。
   - 情緒數：綜述寫 10 [引述] (p. 9, Table 3)；[[2008-fau-aibo]] 為 neutral 加十種其他類別（見該頁）。
   - 語言：綜述稱此資料集包含德語與英語；[[2008-fau-aibo]] 描述的是德語資料庫。綜述引用的是另一篇 Batliner 等人的論文（標題含 cross-linguistic），與 [[2008-fau-aibo]] 不是同一篇：
> "Despite the inclusion of both German and English, it remains limited to these two languages" (p. 9)
> "Children interacting with the AIBO robot: A cross-linguistic emotional speech corpus." (p. 23)
2. **EmoReact 的描述與 [[2016-emoreact]] 不同（並列，不選邊）**：
   - 一致處：建立年、影片數、兒童數、男女人數與年齡範圍，與 [[emoreact]] 頁記載相同。
   - 語言：綜述寫 German (p. 9, Table 3)；[[2016-emoreact]] 未提及語言。
   - 情緒數：綜述寫 15 [引述] (p. 9, Table 3)；[[2016-emoreact]] 的標籤數與此不同（見 [[emoreact]]）。
   - 取得方式：綜述寫 Licensed (p. 9, Table 3)；[[2016-emoreact]] 稱資料集將公開（見該頁）。
   - 引用來源：綜述把 EmoReact 標為 Rajan 等人的文獻，該文獻標題是另一個語料庫：
> "EmoReact (Rajan et al., 2019) 2016 1102 utterances German 63 (31/32) 4–14 15 Licensed" (p. 9, Table 3)
> "Design and development of a multi-lingual speech corpora (TaMaR-EmoDB) for emotion analysis." (p. 25)
3. **同名資料集的數字與 [[2024-ser-evals]] 不同：設定不同，不可直接比較**。[[2024-ser-evals]] 的數字是類別對應後的統計，綜述是轉述原始文獻：
   - EmoDB 情緒數：綜述 7 [引述] (p. 7, Table 2)；[[2024-ser-evals]] 對應後的類別數不同（見 [[emo-db]]）。
   - MESD 規模：綜述 288 [引述] (p. 9, Table 3) utterances；[[2024-ser-evals]] 的樣本數不同（見 [[mesd]]）。兩篇對 MESD 全名的寫法也不同（見 [[mesd]]）。
   - BAUM 規模與情緒數：綜述見上方 Table 2 原文；[[2024-ser-evals]] 的樣本數與類別數不同（見 [[baum]]）。
   - MELD 規模：綜述約 13000 [引述] (p. 7, Table 2) utterances；[[2024-ser-evals]] 的樣本數相近但不同（見 [[meld]]）。
4. **RAVDESS 的描述（綜述內部，並列）**：Table 2 寫建立年 2018 [引述] (p. 7, Table 2)、情緒數 7 [引述] (p. 7, Table 2)；正文則寫 2016 [引述] (p. 8) 年推出、含八種情緒：
> "The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS), introduced in 2016, includes 7356 files from 24 actors (12 male and 12 female) across eight different emotions" (p. 8)
5. **成人資料集數量（綜述內部，AI 整理，待核對）**：綜述稱成人資料集共 15 個 [本文] (p. 21)，但 Table 2 列出的成人資料集列數少於此數 (p. 7, Table 2)。
6. **兒童與成人差異的說法（與 [[2008-fau-aibo]] 並列，不選邊）**：綜述認為兒童的情緒範圍較窄且變異較大，成人與兒童的情緒表達有顯著差異 (p. 2)、(p. 22)；[[2008-fau-aibo]] 則稱沒有跡象顯示兒童的行為與成人有根本差異（見 [[children-emotion-recognition]]）。
7. **指標名稱不同**：綜述把 UAR 寫作 unweighted accuracy (p. 16)；[[2021-pepino-wav2vec2-ser]] 使用「各類平均召回率（average recall）」。名稱不同，論文是否指同一指標需核對：
> "unweighted accuracy (UAR), weighted accuracy (WAR), and F1 scores" (p. 16)
