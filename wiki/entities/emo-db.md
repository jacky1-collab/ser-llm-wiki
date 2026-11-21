---
name: "Emo-DB"
type: dataset
sources: ["2008-fau-aibo", "2021-pepino-wav2vec2-ser"]
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
- 兩篇皆未報告在 Emo-DB 上的實驗數據。

## 相關實體（Related Entities）
無（其他相關資料集目前皆未達建頁門檻）。

## 矛盾／待釐清
無（兩篇只有名稱寫法不同：Emo-DB 與 EMODB，引用文獻相同）。
