# 評測與基準矩陣

## 本頁回答的問題
- 各篇論文用什麼評測協定（資料集、切分、指標、域內／域外）？
- 各篇的主要結果是什麼？哪些比較是同一篇內、同一設定下的？
- 為什麼跨論文的數字不能直接比較？

本頁不做跨論文總表，也不排名。每篇一節，只記該篇內部同一設定下的結果；文末以協定差異表說明各篇設定差在哪。

## [[2008-fau-aibo]]
- 未進行分類實驗 [[2008-fau-aibo]] (p. 4)。
- 規劃隨資料庫提供強制的評測設定，並附基準分類結果：
> "a simple two-fold cross-validation which can be computed with rather low effort" [[2008-fau-aibo]] (p. 4)
- 標註一致性：AMEN 子集的加權 kappa 為 0.59 [本文] [[2008-fau-aibo]] (p. 2)。

## [[2021-pepino-wav2vec2-ser]]
- 協定：IEMOCAP 用 5 折 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3) 交叉驗證、每折留出一個 session；RAVDESS 依演員切分；指標為各類平均召回率（average recall），報告 5 個隨機種子 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3) 的平均與標準差 [[2021-pepino-wav2vec2-ser]] (p. 3)。
- 【可比較：同篇、同協定（Table 1，依說話者正規化、Dense 模型）】
  - Wav2vec2-PT 所有層：IEMOCAP 67.2 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)、RAVDESS 84.3 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)。
  - Wav2vec2-FT 所有層：IEMOCAP 63.8 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)。
  - 基線 eGeMAPS：IEMOCAP 52.4 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)；頻譜圖：IEMOCAP 49.8 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)。
- 【可比較：同篇、同協定（Table 2，全域正規化）】Dense - Global：IEMOCAP 65.8 [本文] [[2021-pepino-wav2vec2-ser]] (p. 4, Table 2)、RAVDESS 75.7 [本文] [[2021-pepino-wav2vec2-ser]] (p. 4, Table 2)。
- Table 2 中其他論文的結果為 [引述]，例如 Sarma 等人在 IEMOCAP 為 60.7 [引述] [[2021-pepino-wav2vec2-ser]] (p. 4, Table 2)；這些結果來自各自論文，設定不一定相同。
- 仿照 Issa 等人的設定：IEMOCAP 72.1% [本文] [[2021-pepino-wav2vec2-ser]] (p. 4)、RAVDESS 84.1% [本文] [[2021-pepino-wav2vec2-ser]] (p. 4)。【設定不同，不可與 Table 1 直接比較：差在 IEMOCAP 只用 improvised 與 full agreement 樣本、RAVDESS 改用隨機切分且不合併 calm 與 neutral】。

## [[2016-emoreact]]
- 協定：person-independent 切分，訓練 432 [本文] [[2016-emoreact]] (p. 5)、驗證 303 [本文] [[2016-emoreact]] (p. 5)、測試 367 [本文] [[2016-emoreact]] (p. 5) 部影片；指標為 AUC ROC 與 skew normalized F1 [[2016-emoreact]] (p. 6)。
- 【可比較：同篇、同協定（Table 5）】RBF SVM 視聽特徵：AUC ROC 0.64 [本文] [[2016-emoreact]] (p. 6, Table 5)、F1 0.69 [本文] [[2016-emoreact]] (p. 6, Table 5)；隨機分類器 AUC ROC 0.50 [本文] [[2016-emoreact]] (p. 6, Table 5)。

## [[2024-ser-evals]]
- 協定：每個資料集 80% [本文] [[2024-ser-evals]] (p. 2, Fig. 1) 訓練、20% [本文] [[2024-ser-evals]] (p. 2, Fig. 1) 做域內測試（僅見於 Fig. 1 圖內文字）；域外為具域外資格的資料集之間做 zero-shot 評估；指標為 macro-averaged F1 [[2024-ser-evals]] (p. 3)。
- 【可比較：同篇、同協定（Table 3）】
  - Whisper-Large-v2：域內平均 0.781942 [本文] [[2024-ser-evals]] (p. 4, Table 3)、域外平均 0.194250 [本文] [[2024-ser-evals]] (p. 4, Table 3)、Weighted Average 0.345741 [本文] [[2024-ser-evals]] (p. 4, Table 3)。
  - w2v-bert-2.0：Weighted Average 0.268165 [本文] [[2024-ser-evals]] (p. 4, Table 3)。
  - 域外平均：WavLM-Large 0.161098 [本文] [[2024-ser-evals]] (p. 4, Table 3)、Whisper-Large 0.197882 [本文] [[2024-ser-evals]] (p. 4, Table 3)。

## [[2026-review-ser-adults-children]]
- 綜述沒有自研實驗；以下皆為綜述轉述他人的結果（[引述]），各研究的切分與指標不同（見 [[2026-review-ser-adults-children]] 的 Table 4、Table 5）[[2026-review-ser-adults-children]] (p. 18, Table 5)。
- FAU-AIBO 上：綜述轉述 Latif 等人的準確率 74.11% [引述] [[2026-review-ser-adults-children]] (p. 17)、Hsiao 與 Chen 的 UAR 46.3% [引述] [[2026-review-ser-adults-children]] (p. 17)、Wen 等人的準確率 42.2% [引述] [[2026-review-ser-adults-children]] (p. 17)。【設定不同，不可直接比較：差在模型、切分與指標（準確率 vs. UAR）】。
- IEMOCAP 上：綜述轉述 Sarma 等人的 R 為 60.7 [引述] [[2026-review-ser-adults-children]] (p. 14, Table 4)。

## 同一數字在兩篇中的轉述
- Sarma 等人在 IEMOCAP 的結果，[[2021-pepino-wav2vec2-ser]] 轉述為 60.7 [引述] [[2021-pepino-wav2vec2-ser]] (p. 4, Table 2)，綜述轉述為 60.7 [引述] [[2026-review-ser-adults-children]] (p. 14, Table 4)，兩篇轉述的數字一致。這是同一結果被兩篇引用，不是兩個結果的比較；兩篇的指標名稱分別為各類平均召回率與 R。

## 協定差異表
| 論文 | 資料集與族群 | 切分 | 指標 | 結果類型 |
| :--- | :--- | :--- | :--- | :--- |
| [[2008-fau-aibo]] | [[fau-aibo]]，兒童、只有語音 [[2008-fau-aibo]] (p. 1) | 規劃 two-fold cross-validation [[2008-fau-aibo]] (p. 4) | 論文未涵蓋 | 無分類結果 |
| [[2021-pepino-wav2vec2-ser]] | [[iemocap]]、[[ravdess]]（綜述歸為成人）[[2021-pepino-wav2vec2-ser]] (p. 3) | IEMOCAP 留一 session；RAVDESS 依演員 [[2021-pepino-wav2vec2-ser]] (p. 3) | 各類平均召回率 [[2021-pepino-wav2vec2-ser]] (p. 3) | 本篇結果＋轉述他人結果 |
| [[2016-emoreact]] | [[emoreact]]，兒童、視聽 [[2016-emoreact]] (p. 2) | person-independent 訓練／驗證／測試 [[2016-emoreact]] (p. 5) | AUC ROC、skew normalized F1 [[2016-emoreact]] (p. 6) | 本篇基線結果 |
| [[2024-ser-evals]] | 多語言資料集 [[2024-ser-evals]] (p. 1, Table 1) | 依 Fig. 1 切分做域內，資料集間 zero-shot 做域外 [[2024-ser-evals]] (p. 2, Fig. 1) | macro-averaged F1 [[2024-ser-evals]] (p. 3) | 本篇結果 |
| [[2026-review-ser-adults-children]] | 成人與兒童資料集 [[2026-review-ser-adults-children]] (p. 7, Table 2) | 各研究不同 [[2026-review-ser-adults-children]] (p. 18, Table 5) | 準確率、F1、R、UAR 等 [[2026-review-ser-adults-children]] (p. 17) | 只有轉述 |

跨論文：【設定不同，不可直接比較：差在資料集、切分、指標與族群（兒童 vs. 成人）】。

## 論文未涵蓋
- 在同一資料集、同一切分與同一指標下，比較五篇所涉方法的結果：論文未涵蓋。
- [[2008-fau-aibo]] 規劃的基準分類結果本身：論文未涵蓋。

## 矛盾／待釐清
以下只匯總各頁既有條目，詳見原頁：
- 各篇指標名稱不同（average recall、AUC ROC／skew normalized F1、macro-averaged F1、綜述的 unweighted accuracy (UAR)），本 wiki 不判定是否為同一指標，數值不跨篇比較（見 [[2024-ser-evals]]、[[2026-review-ser-adults-children]] 的「矛盾／待釐清」）。
- [[2021-pepino-wav2vec2-ser]] 的 RAVDESS 演員切分範圍重疊，論文未說明（見 [[2021-pepino-wav2vec2-ser]]）。
- [[2024-ser-evals]] 稱模型對 URDU 與 AESDD 泛化最好，但兩者不具域外資格（見 [[2024-ser-evals]]、[[ser-evals]]）。
- [[2024-ser-evals]] 把 [[2021-pepino-wav2vec2-ser]] 列為跨語言 SER 研究的引用脈絡（見 [[2024-ser-evals]]）。
