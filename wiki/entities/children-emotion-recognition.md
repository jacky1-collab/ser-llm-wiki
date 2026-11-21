---
name: "兒童情緒辨識（emotion recognition in children）"
type: topic
sources: ["2008-fau-aibo", "2016-emoreact"]
core_contribution_of: ""
---

# 兒童情緒辨識（emotion recognition in children）

## 定義
論文未定義。

## 核心屬性與特點
- [[2016-emoreact]] 認為相較成人，兒童情緒辨識的研究不足：
> "emotion recognition in children has been understudied" [[2016-emoreact]] (p. 1)
- [[2016-emoreact]] 從視覺角度認為兒童更具挑戰性：
> "children tend to fidget and move around more than adults, leading to more self-occlusions and non-frontal head poses" [[2016-emoreact]] (p. 1)
- [[2016-emoreact]] 指出缺乏公開的兒童標註資料，使多數研究者轉向成人：
> "the lack of publicly available datasets for children with annotated emotion labels leads most researchers to focus on adults" [[2016-emoreact]] (p. 1)
- [[2016-emoreact]] 指出幼兒的詞彙有限，難以分析語音通道：
> "as the subjects are toddlers, this makes it hard to analyze the vocal channel due to their very limited vocabularies" [[2016-emoreact]] (p. 2)
- [[2008-fau-aibo]] 認為兒童是自動情緒建模的合理對象：
> "Children as early adapters within an edu-/entertainment scenario should be plausible addressees for automatic emotion modelling." [[2008-fau-aibo]] (p. 2)
- [[2008-fau-aibo]] 認為語音辨識與特徵擷取需針對兒童稍作調整：
> "speech recognition and feature extraction have to be adapted slightly" [[2008-fau-aibo]] (p. 2)

## 在各論文中的應用與實驗表現
- [[2008-fau-aibo]]：建立德國兒童與 Aibo 機器人自發互動的語音情緒資料庫 [[fau-aibo]]，51 位兒童 [本文] [[2008-fau-aibo]] (p. 1)，年齡 10 [本文] [[2008-fau-aibo]] (p. 1) 至 13 歲 [本文] [[2008-fau-aibo]] (p. 1)；只有語音，以詞為單位標註；論文未做分類實驗 [[2008-fau-aibo]] (p. 1)、[[2008-fau-aibo]] (p. 2)。
- [[2016-emoreact]]：建立兒童視聽情緒資料集 [[emoreact]]，63 位兒童 [本文] [[2016-emoreact]] (p. 3)，年齡 4 [本文] [[2016-emoreact]] (p. 2, Table 1) 至 14 歲 [本文] [[2016-emoreact]] (p. 2, Table 1)；以片段為單位多標籤標註，並提供基線分類結果 [[2016-emoreact]] (p. 6, Table 5)。
- 設定不同，不可直接比較：兩篇的兒童年齡、語言情境、蒐集方式（機器人互動 vs. YouTube 反應影片）、模態（只有語音 vs. 視聽）、標註單位（詞 vs. 片段）與一致性指標（加權 kappa vs. Krippendorff's alpha）皆不同 [[2008-fau-aibo]] (p. 2)、[[2016-emoreact]] (p. 3)。

## 相關實體（Related Entities）
- [[fau-aibo]]
- [[emoreact]]

## 矛盾／待釐清
- **兒童與成人的差異（並列，不選邊）**：[[2008-fau-aibo]] 稱沒有跡象顯示兒童的行為與成人有根本差異；[[2016-emoreact]] 則稱兒童比成人動得更多、使臉部追蹤更困難。兩者談的面向不同（前者談情緒行為，後者談視覺追蹤上的動作），是否構成衝突請使用者判斷：
> "there is no indication that they behaved differently from adults in a fundamental way" [[2008-fau-aibo]] (p. 2)
> "Children move more compared to adults, which makes it challenging to successfully track their face and body gestures." [[2016-emoreact]] (p. 2)
- **兒童公開資料集的現況**：[[2016-emoreact]] 稱公開的兒童資料集很少，其比較表未包含 FAU Aibo [[2016-emoreact]] (p. 2, Table 1)；[[2008-fau-aibo]] 表示 FAU Aibo 將釋出供科學使用 [[2008-fau-aibo]] (p. 1)。兩篇都未說明 FAU Aibo 在 [[2016-emoreact]] 發表時的實際公開狀態。
