# 資料集全景對照

## 本頁回答的問題
- 五篇論文提到哪些情緒資料集？各自的族群、語言、模態、規模與標註方式為何？
- 哪些論文在實驗中真正使用了這些資料集，哪些只是提及？
- 同一個資料集在不同論文中的描述是否一致？

本頁只整理 wiki 論文頁與實體頁已有的內容；族群（成人／兒童）的歸類依 [[2026-review-ser-adults-children]] Table 2 與 Table 3 的分類 [[2026-review-ser-adults-children]] (p. 7, Table 2)、[[2026-review-ser-adults-children]] (p. 9, Table 3)。

## 兒童資料集
**[[fau-aibo]]**
- [[2008-fau-aibo]]：德國兒童與 Aibo 機器人自發互動的語音資料庫 [[2008-fau-aibo]] (p. 1)；51 位兒童 [本文] [[2008-fau-aibo]] (p. 1)，年齡 10 [本文] [[2008-fau-aibo]] (p. 1) 至 13 歲 [本文] [[2008-fau-aibo]] (p. 1)；全部詞數 48401 [本文] [[2008-fau-aibo]] (p. 2)；以詞為單位由多位標註者標註，以多數決決定標籤 [[2008-fau-aibo]] (p. 2)。
- [[2026-review-ser-adults-children]]：寫作 FAU-AIBO，規模為 17074 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) utterances。
- 【設定不同，不可直接比較：差在計數單位（詞 vs. utterances），且綜述引用的是另一篇 Batliner 等人的文獻】。兒童人數與年齡兩篇一致（見 [[fau-aibo]]）。

**[[emoreact]]**
- [[2016-emoreact]]：YouTube 反應影片的兒童視聽資料集；1102 [本文] [[2016-emoreact]] (p. 3) 部片段、63 位兒童 [本文] [[2016-emoreact]] (p. 3)、年齡 4 [本文] [[2016-emoreact]] (p. 2, Table 1) 至 14 歲 [本文] [[2016-emoreact]] (p. 2, Table 1)；17 種 [本文] [[2016-emoreact]] (p. 2) 標籤，群眾外包標註 [[2016-emoreact]] (p. 3)。
- [[2026-review-ser-adults-children]]：片段數與兒童數與上述一致，情緒數寫 15 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3)。
- 標籤數兩篇不同，見「矛盾／待釐清」。

**[[mesd]]**
- [[2024-ser-evals]]（類別對應後）：6 位說話者 [本文] [[2024-ser-evals]] (p. 1, Table 1)、1150 個樣本 [本文] [[2024-ser-evals]] (p. 1, Table 1)；未提及說話者年齡。
- [[2026-review-ser-adults-children]]：列為兒童資料集，288 [引述] [[2026-review-ser-adults-children]] (p. 9, Table 3) utterances。
- 【設定不同，不可直接比較：差在類別對應後的統計 vs. 綜述轉述原始文獻】。

## 成人資料集
（依 [[2026-review-ser-adults-children]] Table 2 的分類 [[2026-review-ser-adults-children]] (p. 7, Table 2)）

**[[iemocap]]**
- [[2021-pepino-wav2vec2-ser]]：約 12 小時 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)、10 位說話者 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)、session 數 5 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)；實驗只用 4 類 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2026-review-ser-adults-children]]：7433 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) utterances、10 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者。
- [[2024-ser-evals]]：只在相關研究中提及，未列入其基準 [[2024-ser-evals]] (p. 2)。
- 說話者數兩篇一致；其餘【設定不同，不可直接比較：差在計數單位（小時 vs. utterances）與實驗選用類別】。

**[[ravdess]]**
- [[2021-pepino-wav2vec2-ser]]：24 位演員 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)、8 種情緒 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)，實驗合併為 7 種 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3)。
- [[2026-review-ser-adults-children]]：7356 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 個檔案、24 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者。
- 人數一致；情緒數的描述見「矛盾／待釐清」。

**[[emo-db]]**
- [[2008-fau-aibo]]：作為可（自由）取得的演出資料庫之例 [[2008-fau-aibo]] (p. 1)。
- [[2021-pepino-wav2vec2-ser]]：只在引言中列名 [[2021-pepino-wav2vec2-ser]] (p. 1)。
- [[2024-ser-evals]]（類別對應後）：535 個樣本 [本文] [[2024-ser-evals]] (p. 1, Table 1)、10 位說話者 [本文] [[2024-ser-evals]] (p. 1, Table 1)、6 類 [本文] [[2024-ser-evals]] (p. 1, Table 1)，只用於域內測試 [[2024-ser-evals]] (p. 3)。
- [[2026-review-ser-adults-children]]：535 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 句、7 種 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 情緒。
- 樣本數與說話者數一致；情緒數【設定不同，不可直接比較：差在類別對應後 vs. 原始文獻】。

**[[meld]]**
- [[2024-ser-evals]]（類別對應後）：407 位說話者 [本文] [[2024-ser-evals]] (p. 1, Table 1)、12924 個樣本 [本文] [[2024-ser-evals]] (p. 1, Table 1)、7 類 [本文] [[2024-ser-evals]] (p. 1, Table 1)。
- [[2026-review-ser-adults-children]]：約 13000 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) utterances、407 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者。
- 說話者數一致；規模【設定不同，不可直接比較：差在類別對應後 vs. 原始文獻】。

**[[baum]]**
- [[2024-ser-evals]]（類別對應後）：31 位說話者 [本文] [[2024-ser-evals]] (p. 1, Table 1)、1398 個樣本 [本文] [[2024-ser-evals]] (p. 1, Table 1)、8 類 [本文] [[2024-ser-evals]] (p. 1, Table 1)。
- [[2026-review-ser-adults-children]]：名稱與數字見原文：
> "BAUM-1 (Zhalehpour et al., 2017) 2016 1184 utterances Turkish 31 (18/13) 18–66 13 Free" [[2026-review-ser-adults-children]] (p. 7, Table 2)
- 說話者數一致；規模與情緒數【設定不同，不可直接比較：差在類別對應後 vs. 原始文獻】。

**[[savee]]**
- [[2021-pepino-wav2vec2-ser]]：只在引言中列名 [[2021-pepino-wav2vec2-ser]] (p. 1)。
- [[2026-review-ser-adults-children]]：480 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 句、4 位 [引述] [[2026-review-ser-adults-children]] (p. 7, Table 2) 說話者。

**[[des]]、[[msp-podcast]]**
- [[des]]：[[2008-fau-aibo]] 舉為演出資料庫之例 [[2008-fau-aibo]] (p. 1)；[[2026-review-ser-adults-children]] 只在 Table 4 的資料集欄出現 [[2026-review-ser-adults-children]] (p. 13, Table 4)。
- [[msp-podcast]]：[[2021-pepino-wav2vec2-ser]] 稱它是唯一不屬於「相對小」的資料集 [[2021-pepino-wav2vec2-ser]] (p. 1)；[[2024-ser-evals]] 稱它是知名基準 [[2024-ser-evals]] (p. 2)。

## 各資料集在各論文中的角色
| 資料集 | 用於實驗或基準 | 只是提及或列表 |
| :--- | :--- | :--- |
| [[fau-aibo]] | [[2008-fau-aibo]] 為資料庫本身（未做分類實驗）[[2008-fau-aibo]] (p. 4) | [[2026-review-ser-adults-children]] 列表並轉述他人結果 [[2026-review-ser-adults-children]] (p. 17) |
| [[emoreact]] | [[2016-emoreact]] 建立並提供基線 [[2016-emoreact]] (p. 5) | [[2026-review-ser-adults-children]] 列表 [[2026-review-ser-adults-children]] (p. 9, Table 3) |
| [[iemocap]]、[[ravdess]] | [[2021-pepino-wav2vec2-ser]] 實驗 [[2021-pepino-wav2vec2-ser]] (p. 3) | [[2024-ser-evals]] 提及 IEMOCAP [[2024-ser-evals]] (p. 2)；[[2026-review-ser-adults-children]] 列表 [[2026-review-ser-adults-children]] (p. 7, Table 2) |
| [[emo-db]]、[[meld]]、[[mesd]]、[[baum]] | [[2024-ser-evals]] 基準成員 [[2024-ser-evals]] (p. 1, Table 1) | [[2026-review-ser-adults-children]] 列表 [[2026-review-ser-adults-children]] (p. 7, Table 2)、[[2026-review-ser-adults-children]] (p. 9, Table 3) |
| [[savee]]、[[des]]、[[msp-podcast]] | 無 | [[2008-fau-aibo]]、[[2021-pepino-wav2vec2-ser]]、[[2024-ser-evals]]、[[2026-review-ser-adults-children]] 提及（見上方各節） |

## 論文未涵蓋
- 各資料集在五篇論文以外的版本或後續更新：論文未涵蓋。
- [[des]]、[[msp-podcast]] 的規模、說話者數等統計：論文未涵蓋。
- [[emoreact]] 的語言：[[2016-emoreact]] 未提及（綜述的寫法見「矛盾／待釐清」）。
- [[iemocap]]、[[ravdess]] 說話者的年齡：[[2021-pepino-wav2vec2-ser]] 未提及；本頁的成人歸類只依綜述 Table 2。

## 矛盾／待釐清
以下只匯總各頁既有條目，詳見原頁：
- FAU Aibo：[[2008-fau-aibo]] 內部的 AMEN 詞數與 turn 數不一致；綜述對規模、建立年、情緒數、語言與引用來源的描述與 [[2008-fau-aibo]] 不同（見 [[2008-fau-aibo]]、[[fau-aibo]]、[[2026-review-ser-adults-children]] 的「矛盾／待釐清」）。
- EmoReact：[[2016-emoreact]] 內部 Valence 未被選入；綜述對語言、情緒數、取得方式與引用來源的描述與 [[2016-emoreact]] 不同（見 [[2016-emoreact]]、[[emoreact]]）。
- 同名資料集的數字在 [[2024-ser-evals]] 與綜述之間不同：Emo-DB 情緒數、MESD 規模與全名、BAUM 規模／情緒數／錄製方式、MELD 規模（見 [[emo-db]]、[[mesd]]、[[baum]]、[[meld]]）。
- 綜述內部：RAVDESS 的年份與情緒數、SAVEE 與 BAUM 的年份、成人資料集總數與 Table 2 列數（見 [[ravdess]]、[[savee]]、[[baum]]、[[2026-review-ser-adults-children]]）。
- 兒童資料集的公開／授權狀態，在 [[2008-fau-aibo]]、[[2016-emoreact]] 與綜述之間說法不同（見 [[children-emotion-recognition]]）。
