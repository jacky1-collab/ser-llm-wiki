# 開場：這份簡報要帶你看什麼

本簡報的內容全部整理自本 wiki 的五篇論文頁、實體頁與綜合頁，不加入 wiki 以外的資訊。

- 主題：語音情緒辨識（SER），特別是兒童的語音情緒辨識。
- 路線：概念 → 資料集 → 評測 → 特徵與模型 → 成人與兒童 → 開放問題。
- 五個綜合頁：[[datasets-comparison]]、[[benchmark-matrix]]、[[adult-vs-child-ser]]、[[architecture-evolution]]、[[open-challenges]]。

**怎麼讀這份簡報**

- [本文]＝該論文自己的結果；[引述]＝該論文轉述別人的結果。
- 〔來源：…〕＝本 wiki 的頁面；(p. N)＝原始 PDF 的頁碼。

---

# 什麼是語音情緒辨識

- 自動情緒辨識是社交機器人、情感感知人機互動設計與情感感知家教系統的核心技術 [[2016-emoreact]] (p. 1)。
- 綜述指出 SER 的應用領域包括人機互動、情感運算與心理健康：

> "Speech emotion recognition (SER) has become an important area of research due to its wide applications in human-computer interaction, affective computing, and mental health." [[2026-review-ser-adults-children]] (p. 1)

- 現有 SER 研究大多集中於成人，兒童受到的關注有限 [[2026-review-ser-adults-children]] (p. 1)。
- 情緒資料集通常不大，使深度學習難以應用：

> "Emotion recognition datasets are relatively small, making the use of deep learning techniques challenging." [[2021-pepino-wav2vec2-ser]] (p. 1)

---

# 兒童語音情緒辨識為什麼難

- 兒童較成人更常扭動、移動，造成遮擋與非正面頭部姿勢：

> "children tend to fidget and move around more than adults, leading to more self-occlusions and non-frontal head poses" [[2016-emoreact]] (p. 1)

- 綜述歸納的挑戰：音高、音色、音量差異，常見發音錯誤與不完整句子，以及強烈的說話者依賴性 [[2026-review-ser-adults-children]] (p. 2)。
- 資料集數量：綜述稱成人有 15 個 [本文] [[2026-review-ser-adults-children]] (p. 21) 資料集，兒童只有 7 個 [本文] [[2026-review-ser-adults-children]] (p. 21)。註：綜述 Table 2 實際列出的成人資料集數量少於此數（見 [[2026-review-ser-adults-children]] 的「矛盾／待釐清」）。

---

# 兩個兒童資料集：FAU Aibo 與 EmoReact

- **FAU Aibo**：德國兒童與 Aibo 機器人自發互動的語音資料庫，只有語音，以詞為單位標註；共 51 位兒童 [本文] [[2008-fau-aibo]] (p. 1)。見 [[fau-aibo]]。
- **EmoReact**：YouTube 反應影片的兒童視聽資料集，以片段為單位、可多標籤；共 63 位兒童 [本文] [[2016-emoreact]] (p. 3)，標籤 17 種 [本文] [[2016-emoreact]] (p. 2)。見 [[emoreact]]。
- **設定不同，不可直接比較**：兩者的語言情境、蒐集方式（機器人互動 vs. YouTube 影片）、模態（只有語音 vs. 視聽）與標註單位（詞 vs. 片段）都不同 [[children-emotion-recognition]]。

---

# 資料集全景：成人資料集與統計口徑

- 綜述把 IEMOCAP、RAVDESS、Emo-DB、SAVEE、MELD 等歸為成人資料集 [[2026-review-ser-adults-children]] (p. 7, Table 2)。見 [[iemocap]]、[[ravdess]]、[[emo-db]]、[[savee]]、[[meld]]。
- 同一個資料集在不同論文中的規模，計數單位常不同：詞、片段、utterances，或類別對應後的樣本數 [[datasets-comparison]]。
- [[2024-ser-evals]] 的資料集數字是類別對應後的統計，綜述則是轉述原始文獻，所以兩者的數字不能直接相比 [[datasets-comparison]]。

---

# 評測為什麼不能直接比

- [[2021-pepino-wav2vec2-ser]]：IEMOCAP 每折留出一個 session、RAVDESS 依演員切分；指標是各類平均召回率（average recall）。
- [[2016-emoreact]]：person-independent 的訓練、驗證、測試切分；指標是 AUC ROC 與 skew normalized F1。
- [[2024-ser-evals]]：各資料集內切分做域內評估，資料集之間做 zero-shot 域外評估；指標是 macro-averaged F1。
- [[2026-review-ser-adults-children]]：沒有自研實驗，只轉述各研究的結果，切分與指標各不相同。
- **設定不同，不可直接比較**：差在資料集、切分、指標與族群（兒童 vs. 成人）。各篇指標名稱不同，本 wiki 不判定是否為同一指標 [[benchmark-matrix]]。

---

# 特徵與模型做法

- 手工特徵：[[2021-pepino-wav2vec2-ser]] 以 eGeMAPS 與頻譜圖為基線；[[2016-emoreact]] 以 OpenFace 與 COVAREP 擷取特徵；綜述稱 MFCC 是最常用的特徵 [[2026-review-ser-adults-children]] (p. 6)。
- 自監督表徵【可比較：同篇同協定】：IEMOCAP 上 Wav2vec2-PT 為 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)，Wav2vec2-FT 為 63.8 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率）。
- ASR 模型【可比較：同篇同協定】：域外平均 Whisper-Large-v2 為 0.194250 [本文] [[2024-ser-evals]] (p. 4, Table 3)，WavLM-Large 為 0.161098 [本文] [[2024-ser-evals]] (p. 4, Table 3)（macro-averaged F1）。
- **設定不同，不可直接比較**：[[2021-pepino-wav2vec2-ser]] 發現微調做 ASR 的模型較差，[[2024-ser-evals]] 發現以 ASR 為主要目的的 Whisper 較好；兩篇比較的對象、資料集、切分與指標都不同 [[architecture-evolution]]。本頁兩篇的數字也不可互相比較（指標分別為各類平均召回率與 macro-averaged F1）。

---

# 成人與兒童：論文怎麼說它們的差異

FAU Aibo 論文：沒有跡象顯示兒童的行為與成人有根本差異。

> "there is no indication that they behaved differently from adults in a fundamental way" [[2008-fau-aibo]] (p. 2)

EmoReact 論文：兒童比成人動得更多，使臉部與身體追蹤更困難。

> "Children move more compared to adults, which makes it challenging to successfully track their face and body gestures." [[2016-emoreact]] (p. 2)

綜述：兒童的情緒範圍較窄且變異較大，受年齡、語言發展與文化影響。

> "children display a narrower and more variable range of emotions, shaped by age, linguistic development, and cultural context" [[2026-review-ser-adults-children]] (p. 2)

- 三篇的依據與面向不同，本簡報不選邊 [[adult-vs-child-ser]]。

---

# 綜述和原始論文不一致的地方

- EmoReact 的標籤數：綜述寫 15 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) 種；原始論文為 17 種 [本文] [[2016-emoreact]] (p. 2)。
- FAU Aibo 的規模：綜述寫 17074 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) utterances；原始論文的全部詞數為 48401 [本文] [[2008-fau-aibo]] (p. 2)。
- **兩篇描述不同，不可直接比較**：綜述轉述的來源與原始論文不同、計數單位不同。
- 綜述還把 EmoReact 標為 Rajan 等人的文獻，而該文獻標題是另一個語料庫（TaMaR-EmoDB）（見 [[emoreact]]）。
- 學習重點：二手綜述的數字要回到原始論文核對。

---

# 開放問題

- 兒童資料稀缺，隱私與同意也讓資料難以釋出或標準化 [[open-challenges]]。
- 標註一致性：[[2016-emoreact]] 的 Attentiveness 一致性為 -0.16 [本文] [[2016-emoreact]] (p. 3)；[[2008-fau-aibo]] 的 AMEN 子集加權 kappa 為 0.59 [本文] [[2008-fau-aibo]] (p. 2)。**設定不同，不可直接比較**：差在一致性指標（Krippendorff's alpha vs. 加權 kappa）與計算單位（各標籤 vs. 子集整體）。
- 泛化：表現依訓練與測試組合變動很大，模型穩健性仍是挑戰 [[2024-ser-evals]] (p. 4)。
- 原始波形建模與自監督學習在兒童 SER 的應用仍有限 [[2026-review-ser-adults-children]] (p. 22)。

---

# 結論

- 兒童語音情緒辨識資料少、挑戰多，研究仍以成人為主 [[adult-vs-child-ser]]。
- 跨論文的數字因資料集、切分、指標與族群不同，不能直接比較 [[benchmark-matrix]]。
- 二手綜述的描述可能與原始論文不同，引用時要回原始論文核對 [[datasets-comparison]]。

---

# 參考來源

- [[2008-fau-aibo]]：FAU Aibo 兒童情緒語音資料庫的介紹論文。
- [[2016-emoreact]]：EmoReact 兒童視聽情緒資料集與基線。
- [[2021-pepino-wav2vec2-ser]]：以自監督語音模型的多層表徵做語音情緒辨識。
- [[2024-ser-evals]]：多語言域內與域外的語音情緒辨識基準。
- [[2026-review-ser-adults-children]]：成人與兒童語音情緒辨識綜述。
- 綜合頁：[[datasets-comparison]]、[[benchmark-matrix]]、[[adult-vs-child-ser]]、[[architecture-evolution]]、[[open-challenges]]。
