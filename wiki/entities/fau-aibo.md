---
name: "FAU Aibo Emotion Corpus"
type: dataset
sources: ["2008-fau-aibo"]
core_contribution_of: "2008-fau-aibo"
---

# FAU Aibo Emotion Corpus

## 定義
> "We report on a thoroughly processed and annotated German emotional speech database" [[2008-fau-aibo]] (p. 1)

中文說明（AI 整理，待核對）：FAU Aibo Emotion Corpus（簡稱 FAU Aibo）是德國兒童與 Sony 的 Aibo 機器人互動時錄製的自發情緒語音資料庫，以詞為單位標註情緒使用者狀態，並另做多種附加標註與對應到較大單位的處理 [[2008-fau-aibo]] (p. 1)。

## 核心屬性與特點
- 語言與情境：德語；兒童以綠野仙蹤法（Wizard-of-Oz）與遙控的 Aibo 互動，Aibo 照固定動作序列行動、不理會兒童說了什麼 [[2008-fau-aibo]] (p. 1)。
- 說話者：51 位兒童 [本文] [[2008-fau-aibo]] (p. 1)，年齡 10 [本文] [[2008-fau-aibo]] (p. 1) 至 13 歲 [本文] [[2008-fau-aibo]] (p. 1)，男性 21 [本文] [[2008-fau-aibo]] (p. 1)、女性 30 [本文] [[2008-fau-aibo]] (p. 1)。
- 規模：約 9.2 小時 [本文] [[2008-fau-aibo]] (p. 2) 語音，共 48401 [本文] [[2008-fau-aibo]] (p. 2) 個詞。
- 錄音規格：取樣率 48 kHz [本文] [[2008-fau-aibo]] (p. 1)、量化 16 bit [本文] [[2008-fau-aibo]] (p. 1)，降頻至 16 kHz [本文] [[2008-fau-aibo]] (p. 1)。
- 標註：5 位標註者 [本文] [[2008-fau-aibo]] (p. 3) 逐詞標註，以多數決（majority voting, MV）決定詞的標籤 [[2008-fau-aibo]] (p. 2)。
> "if three or more labellers agree, the label is attributed to the word" [[2008-fau-aibo]] (p. 2)
- AMEN 子集：把 touchy、reprimanding 與 angry 合併為 Angry，形成 4 類 [本文] [[2008-fau-aibo]] (p. 2) 問題（Angry、Motherese、Emphatic、Neutral），加權 kappa（weighted kappa）為 0.59 [本文] [[2008-fau-aibo]] (p. 2)。
- 多層單位：詞層級標籤可再對應到 turn 與 chunk；turn 標籤合計 3990 [本文] [[2008-fau-aibo]] (p. 3)。
- 人工校正：自動詞切分與音高（pitch）值皆經人工校正 [[2008-fau-aibo]] (p. 3)。
- 附加資料：[± co-operative] 標註（約一半資料）、EDE 與 eLabel 軟體、CEICES 特徵編碼規格、其他類型錄音 [[2008-fau-aibo]] (p. 3)。

## 在各論文中的應用與實驗表現
- 在 [[2008-fau-aibo]] 中，本資料庫是該論文的核心貢獻；論文未報告分類實驗結果，僅說明將隨釋出內容提供評測設定與基準分類結果 [[2008-fau-aibo]] (p. 4)：
> "a simple two-fold cross-validation which can be computed with rather low effort" [[2008-fau-aibo]] (p. 4)

## 相關實體（Related Entities）
無（其他相關實體目前皆未達建頁門檻，僅以純文字記於 [[2008-fau-aibo]] 的提及實體清單）。

## 矛盾／待釐清
- AMEN 四類詞數 1557 [本文] [[2008-fau-aibo]] (p. 2)、1224 [本文] [[2008-fau-aibo]] (p. 2)、1645 [本文] [[2008-fau-aibo]] (p. 2)、1645 [本文] [[2008-fau-aibo]] (p. 2) 相加後，比同篇後文的 AMEN 詞數 6070 [本文] [[2008-fau-aibo]] (p. 3) 多出一個詞；論文未說明原因。
- 含 AMEN 詞的 turn 數為 3996 [本文] [[2008-fau-aibo]] (p. 3)，turn 標籤合計為 3990 [本文] [[2008-fau-aibo]] (p. 3)；論文未說明差異原因。
