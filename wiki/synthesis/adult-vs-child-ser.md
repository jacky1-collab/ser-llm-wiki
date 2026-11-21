# 成人 vs. 兒童 SER 對比

## 本頁回答的問題
- 論文提出了哪些兒童語音情緒辨識（SER）的挑戰？
- 成人與兒童在資料、特徵、模型與結果上，論文怎麼說？
- 各篇對「兒童與成人是否不同」的說法是否一致？

族群歸類：本頁把 [[iemocap]]、[[ravdess]] 等列為成人資料集，是依 [[2026-review-ser-adults-children]] Table 2 的分類 [[2026-review-ser-adults-children]] (p. 7, Table 2)；[[2021-pepino-wav2vec2-ser]] 本身未提及說話者年齡。

## 兒童 SER 的挑戰（各篇說法並列）
- [[2016-emoreact]]：兒童較成人更常扭動、移動，造成更多自我遮擋與非正面頭部姿勢；且缺乏公開的兒童標註資料 [[2016-emoreact]] (p. 1)。
- [[2026-review-ser-adults-children]]：音高、音色、音量的差異，常見發音錯誤與不完整句子，重疊的聲學模式，快速的情緒轉換，以及強烈的說話者依賴性 [[2026-review-ser-adults-children]] (p. 2)。
- [[2008-fau-aibo]]：語音辨識與特徵擷取需針對兒童稍作調整：
> "speech recognition and feature extraction have to be adapted slightly" [[2008-fau-aibo]] (p. 2)
- 三篇談的面向不同（視覺追蹤、聲學與語言特性、系統調整），屬並列而非比較。

## 資料面
- [[2026-review-ser-adults-children]] 稱成人 SER 有 15 個 [本文] [[2026-review-ser-adults-children]] (p. 21) 資料集，專門針對兒童的只有 7 個 [本文] [[2026-review-ser-adults-children]] (p. 21)。
- [[2016-emoreact]] 稱公開的兒童資料集很少，只有一個含影片 [[2016-emoreact]] (p. 2)。
- 兒童資料集規模：[[fau-aibo]] 為 51 位兒童 [本文] [[2008-fau-aibo]] (p. 1)；[[emoreact]] 為 63 位兒童 [本文] [[2016-emoreact]] (p. 3)。【設定不同，不可直接比較：差在語言情境、蒐集方式（機器人互動 vs. YouTube 影片）、模態（只有語音 vs. 視聽）與標註單位（詞 vs. 片段）】（見 [[children-emotion-recognition]]）。
- 資料集比較細節見 [[datasets-comparison]]。

## 特徵面
- [[2026-review-ser-adults-children]] 認為成人 SER 以頻譜特徵表現最好，兒童 SER 則更依賴音高、能量變化與強度等特徵 [[2026-review-ser-adults-children]] (p. 21)。
- [[2016-emoreact]] 在兒童影片的聲學行為分析中，MFCC、嗓音品質特徵與韻律特徵對各情緒的影響最大 [[2016-emoreact]] (p. 5)；fear 與 disgust 出現時音高平均較高 [[2016-emoreact]] (p. 5)。
- [[2008-fau-aibo]] 為兒童語料提供人工校正的音高值 [[2008-fau-aibo]] (p. 3)。
- 【設定不同，不可直接比較：差在證據類型（綜述論述、效果量分析、資料庫標註）】。相關實體見 [[pitch]]、[[mfcc]]。

## 模型與結果面
- 兒童：wiki 中的兒童分類結果只有 [[2016-emoreact]] 的基線與綜述轉述的 FAU-AIBO 結果。
  - [[2016-emoreact]]：RBF SVM 視聽特徵的 AUC ROC 為 0.64 [本文] [[2016-emoreact]] (p. 6, Table 5)。
  - 綜述轉述 Latif 等人在 FAU-AIBO 的準確率為 74.11% [引述] [[2026-review-ser-adults-children]] (p. 17)。
- 成人：[[2021-pepino-wav2vec2-ser]] 在 IEMOCAP 為 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)（各類平均召回率）。
- 【設定不同，不可直接比較：差在族群、資料集、切分與指標（AUC ROC、準確率、各類平均召回率）】。
- [[2026-review-ser-adults-children]] 認為兒童 SER 需要混合架構、動態 RNN 與遷移學習等策略，且在兒童 SER 中手工特徵方法目前優於原始波形模型 [[2026-review-ser-adults-children]] (p. 22)。相關實體見 [[transfer-learning]]。

## 「兒童是否與成人不同」的說法比較
- [[2008-fau-aibo]]：
> "there is no indication that they behaved differently from adults in a fundamental way" [[2008-fau-aibo]] (p. 2)
- [[2016-emoreact]]：
> "Children move more compared to adults, which makes it challenging to successfully track their face and body gestures." [[2016-emoreact]] (p. 2)
- [[2026-review-ser-adults-children]]：
> "children display a narrower and more variable range of emotions, shaped by age, linguistic development, and cultural context" [[2026-review-ser-adults-children]] (p. 2)
- 三篇的依據與面向不同，本頁不選邊（見「矛盾／待釐清」）。

## 論文未涵蓋
- 在同一資料集與同一指標下，同時比較成人與兒童語音的實驗：論文未涵蓋。
- 兒童年齡分層（例如不同年齡段）的辨識結果：論文未涵蓋。
- 從成人資料遷移到兒童資料的實際實驗結果：論文未涵蓋（綜述只列為未來方向）。

## 矛盾／待釐清
以下只匯總各頁既有條目，詳見原頁：
- 兒童與成人差異的說法：[[2008-fau-aibo]]、[[2016-emoreact]] 與綜述三方說法並列，不選邊（見 [[children-emotion-recognition]]、[[2026-review-ser-adults-children]]）。
- [[2008-fau-aibo]] 與 [[2016-emoreact]] 的兒童語料：設定不同，不可直接比較（見 [[2016-emoreact]]、[[children-emotion-recognition]]）。
- 兒童資料集的公開或授權狀態說法不同（見 [[children-emotion-recognition]]）。
- 各篇指標名稱不同（average recall、AUC ROC／skew normalized F1、macro-averaged F1、綜述的 unweighted accuracy (UAR)），本 wiki 不判定是否為同一指標，數值不跨篇比較。
