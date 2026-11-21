# 核心挑戰與開放問題

## 本頁回答的問題
- 五篇論文各自提出了哪些未解的挑戰？
- 這些挑戰在哪幾篇論文中被提到？各篇的說法與證據類型為何？

每項只列出提出的論文與頁碼，不合併成單一結論。

## 資料稀缺（尤其兒童）
- [[2016-emoreact]]：缺乏公開的兒童標註資料，使多數研究者轉向成人 [[2016-emoreact]] (p. 1)。
- [[2026-review-ser-adults-children]]：兒童資料集只有 7 個 [本文] [[2026-review-ser-adults-children]] (p. 21)，並把擴充兒童資料集列為未來方向 [[2026-review-ser-adults-children]] (p. 22)。
- [[2021-pepino-wav2vec2-ser]]：情緒辨識資料集相對小，使深度學習難以應用 [[2021-pepino-wav2vec2-ser]] (p. 1)。
- 見 [[children-emotion-recognition]]、[[datasets-comparison]]。

## 類別不平衡與樣本捨棄
- [[2008-fau-aibo]]：類別分布非常不平衡 [[2008-fau-aibo]] (p. 2)。
- [[2016-emoreact]]：以下取樣負例與 ensemble 分類器處理不平衡 [[2016-emoreact]] (p. 6)。
- [[2021-pepino-wav2vec2-ser]]：在註腳承認捨棄無一致標籤與非目標情緒的樣本並不理想 [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2024-ser-evals]]：以 logit adjustment 處理資料集間不同的類別分布 [[2024-ser-evals]] (p. 3)。

## 泛化：域外與跨語言
- [[2024-ser-evals]]：高標準差顯示表現依訓練／測試組合而變動很大，模型穩健性仍是挑戰 [[2024-ser-evals]] (p. 4)。
- [[2026-review-ser-adults-children]]：只在單一資料集上訓練的模型能否泛化仍不清楚 [[2026-review-ser-adults-children]] (p. 16)。
- 見 [[ser-evals]]、[[benchmark-matrix]]。

## 標註一致性
- [[2008-fau-aibo]]：AMEN 子集的加權 kappa 為 0.59 [本文] [[2008-fau-aibo]] (p. 2)。
- [[2016-emoreact]]：各標籤的 Krippendorff's alpha 差異大，例如 Attentiveness 為 -0.16 [本文] [[2016-emoreact]] (p. 3)；後續只使用一致性高於 0.4 [本文] [[2016-emoreact]] (p. 3) 的標籤。
- 【設定不同，不可直接比較：差在一致性指標（加權 kappa vs. Krippendorff's alpha）與計算單位（子集整體 vs. 各標籤）】。

## 跨研究可比性與標準化
- [[2008-fau-aibo]]：研究者常未選用完全相同的樣本，使跨研究比較不可能，因此規劃強制基準 [[2008-fau-aibo]] (p. 4)。
- [[2024-ser-evals]]：現有基準偏重少數資料集與域內評估 [[2024-ser-evals]] (p. 1)。

## 特徵可靠度
- [[2008-fau-aibo]]：音高被認為重要但無法完全可靠地擷取；人工校正值也不是 ground truth [[2008-fau-aibo]] (p. 3)。
- [[2021-pepino-wav2vec2-ser]]：作者認為 wav2vec 2.0 特徵可能缺少部分韻律資訊 [[2021-pepino-wav2vec2-ser]] (p. 4)。
- 見 [[pitch]]。

## 雜訊、遮擋與多模態
- [[2016-emoreact]]：視覺分類器受張嘴、遮擋、快速動作影響，音訊受背景聲音影響 [[2016-emoreact]] (p. 6)。
- [[2026-review-ser-adults-children]]：自然或吵雜環境下的穩健性、多模態分析、聲學與語言融合在兒童研究中尤其缺乏 [[2026-review-ser-adults-children]] (p. 2)。

## 隱私與倫理
- [[2008-fau-aibo]]：隱私常使自發資料無法釋出，錄影也因隱私不提供 [[2008-fau-aibo]] (p. 1)、[[2008-fau-aibo]] (p. 4)。
- [[2026-review-ser-adults-children]]：兒童資料的隱私與同意要求使標準化資料集難以建立 [[2026-review-ser-adults-children]] (p. 2)。

## 原始波形、自監督學習與遷移學習在兒童 SER 的應用
- [[2026-review-ser-adults-children]]：原始波形建模在兒童 SER 的應用有限；非監督與自監督學習、跨領域遷移學習都列為未來方向 [[2026-review-ser-adults-children]] (p. 22)。
- 見 [[self-supervised-learning]]、[[transfer-learning]]、[[architecture-evolution]]。

## 各篇的未來研究方向（並列）
- [[2016-emoreact]]：為資料集加上字幕以研究語言模態，並探討性別對兒童情緒表達的影響 [[2016-emoreact]] (p. 7)。
- [[2024-ser-evals]]：領域適應、few-shot learning、meta-learning，以及研究哪些資料集特性有助泛化 [[2024-ser-evals]] (p. 4)。
- [[2026-review-ser-adults-children]]：見上方各節 [[2026-review-ser-adults-children]] (p. 22)。
- [[2008-fau-aibo]]：作者認為規模再大上某個量級的資料庫是此領域標準化的前提之一，並期望以基準設定形成「islands of standardization」[[2008-fau-aibo]] (p. 4)。
- [[2021-pepino-wav2vec2-ser]]：論文未提及。

## 論文未涵蓋
- 上述挑戰的解決方案在五篇論文中的實證比較：論文未涵蓋。
- 兒童 SER 中隱私保護方法的具體做法：論文未涵蓋。

## 矛盾／待釐清
以下只交叉引用其他綜合頁與原頁的既有條目，不另行展開：
- 資料集描述的差異：見 [[datasets-comparison]]。
- 指標名稱與評測協定的差異：見 [[benchmark-matrix]]。
- 兒童與成人差異的說法：見 [[adult-vs-child-ser]]。
- ASR 與 SER 的關係：見 [[architecture-evolution]]。
