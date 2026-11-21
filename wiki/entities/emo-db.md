---
name: "Emo-DB"
type: dataset
sources: ["2008-fau-aibo", "2021-pepino-wav2vec2-ser", "2024-ser-evals", "2026-review-ser-adults-children"]
core_contribution_of: ""
---

# Emo-DB

## 定義
> "some acted databases are (freely) available such as the Berlin Database of Emotional Speech" [[2008-fau-aibo]] (p. 1)

中文說明（AI 整理，待核對）：Emo-DB 是柏林情緒語音資料庫（Berlin Database of Emotional Speech），屬於演出（acted）情緒語音資料庫，在 [[2008-fau-aibo]] 中被舉為可（自由）取得的演出資料庫之例 [[2008-fau-aibo]] (p. 1)。兩篇論文都未進一步給出正式定義。

## 核心屬性與特點
- 類型：演出資料庫 [[2008-fau-aibo]] (p. 1)。
- 名稱寫法：[[2008-fau-aibo]] 寫作「Emo-DB」[[2008-fau-aibo]] (p. 1)，[[2021-pepino-wav2vec2-ser]] 寫作「EMODB」[[2021-pepino-wav2vec2-ser]] (p. 1)。
- 兩篇引用的是同一篇文獻（Burkhardt 等人）：
> "A database of german emotional speech" [[2008-fau-aibo]] (p. 4)
> "A database of german emotional speech" [[2021-pepino-wav2vec2-ser]] (p. 5)
- 類別定義：[[2008-fau-aibo]] 認為這類演出資料庫的類別是由給說話者的指示直接給定，因此定義明確：
> "rather well-defined acted databases such as Emo-DB and DES (well-defined because the classes are given trivially via speaker instructions)" [[2008-fau-aibo]] (p. 4)
- 規模：[[2021-pepino-wav2vec2-ser]] 把 EMODB 與 SAVEE、RAVDESS、IEMOCAP、MSP-Podcast 並列，並稱除 MSP-Podcast 外這些資料集都相對小：
> "With the exception of MSP-Podcast, these datasets are relatively small in size, usually including only a few dozen speakers." [[2021-pepino-wav2vec2-ser]] (p. 1)

## 在各論文中的應用與實驗表現
- [[2008-fau-aibo]]：作為「已有可取得的演出資料庫、卻沒有條件相近的自發資料庫」的對照例 [[2008-fau-aibo]] (p. 1)；並指出即使在 Emo-DB 這類資料庫上，研究者也常未選用完全相同的樣本，使跨研究比較不可能 [[2008-fau-aibo]] (p. 4)。
> "researchers often do not select exactly the same cases per class" [[2008-fau-aibo]] (p. 4)
- [[2021-pepino-wav2vec2-ser]]：僅在引言中列為訓練與評估情緒辨識模型的資料集之一，未用於該篇實驗 [[2021-pepino-wav2vec2-ser]] (p. 1)。
- [[2024-ser-evals]]：列為基準資料集之一（德語）；類別對應後為 6 類 [本文] [[2024-ser-evals]] (p. 1, Table 1)、10 位說話者 [本文] [[2024-ser-evals]] (p. 1, Table 1)、535 個樣本 [本文] [[2024-ser-evals]] (p. 1, Table 1)，平均長度 2.8 秒 [本文] [[2024-ser-evals]] (p. 1, Table 1)；不具域外資格，只用於域內測試 [[2024-ser-evals]] (p. 1, Table 1)、[[2024-ser-evals]] (p. 3)。該篇只報告跨資料集彙總指標，未列出 Emo-DB 單一資料集的結果 [[2024-ser-evals]] (p. 4, Table 3)。
> "A database of german emotional speech." [[2024-ser-evals]] (p. 5)
- [[2008-fau-aibo]] 與 [[2021-pepino-wav2vec2-ser]] 皆未報告 Emo-DB 的統計或實驗數據。
- [[2026-review-ser-adults-children]]：列為成人資料集；綜述轉述建立年 2005 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)、535 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 句、德語、10 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者（男 5 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)／女 5 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2)）、7 種 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 情緒、可免費取得。樣本數與說話者數和 [[2024-ser-evals]] 一致；可免費取得與 [[2008-fau-aibo]] 的「(freely) available」說法一致。

## 相關實體（Related Entities）
無（其他相關資料集目前皆未達建頁門檻）。

## 矛盾／待釐清
- 名稱寫法不同：Emo-DB、EMODB、EmoDB／EmoDBDataset；各篇引用文獻皆為 Burkhardt 等人的「A database of german emotional speech」。
- 情緒數：綜述轉述為 7 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 種；[[2024-ser-evals]] 類別對應後為 6 類 [本文] [[2024-ser-evals]] (p. 1, Table 1)。設定不同（原始文獻 vs. 類別對應後），不可直接比較。
