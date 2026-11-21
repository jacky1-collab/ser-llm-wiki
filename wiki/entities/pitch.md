---
name: "pitch"
type: feature
sources: ["2008-fau-aibo", "2021-pepino-wav2vec2-ser", "2016-emoreact"]
core_contribution_of: ""
---

# 音高（pitch）

## 定義
論文未定義。

## 核心屬性與特點
- [[2008-fau-aibo]] 指出音高在各類特徵中歷來地位突出：
> "Historically, pitch has had a prominent position w. r. t. all feature types because of the preponderance of intonation models in the last decades." [[2008-fau-aibo]] (p. 3)
- 音高被認為很重要，但無法完全可靠地擷取：
> "notoriously known as impossible to be extracted fully reliably" [[2008-fau-aibo]] (p. 3)
- 擷取方式：以音高偵測演算法（pitch detection algorithm, PDA）自動擷取；[[2008-fau-aibo]] 另以人工校正 [[2008-fau-aibo]] (p. 3)。
- 人工校正值的限制：
> "Such manually corrected pitch values do not constitute a ground truth" [[2008-fau-aibo]] (p. 3)
- [[2021-pepino-wav2vec2-ser]] 認為音高對語音辨識可能不重要，但對語音情緒辨識很關鍵：
> "information about the pitch might not be important for speech recognition, while it is essential for speech emotion recognition" [[2021-pepino-wav2vec2-ser]] (p. 3)

## 在各論文中的應用與實驗表現
- [[2008-fau-aibo]]：除自有 PDA 外，另以一個知名的逐框 PDA 為基線並人工校正其數值，涵蓋 3990 [本文] [[2008-fau-aibo]] (p. 3) 個 AMEN turn；作者表示不知道有其他情緒資料庫具備這種校正值 [[2008-fau-aibo]] (p. 3)。校正值可用來計算音高相關特徵：
> "the corrected values can be used for computing F0 features" [[2008-fau-aibo]] (p. 3)
- [[2021-pepino-wav2vec2-ser]]：未直接擷取音高特徵；作者以「微調做 ASR 會丟失音高等資訊」的假設，解釋 Wav2vec2-FT 只用 contextualized encoder 輸出的結果最差 [[2021-pepino-wav2vec2-ser]] (p. 3)，例如 IEMOCAP 為 44.6 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)，Wav2vec2-PT 對應設定為 58.5 [本文] [[2021-pepino-wav2vec2-ser]] (p. 3, Table 1)。這是作者的假設，論文未直接驗證音高資訊是否被移除。
- [[2016-emoreact]]：把音高／基頻列為韻律特徵，以 COVAREP 擷取 [[2016-emoreact]] (p. 4)、[[2016-emoreact]] (p. 5)：
> "Pitch/Fundamental Frequency (F0) indicates the pitch information in one" [[2016-emoreact]] (p. 4)
- [[2016-emoreact]] 的兒童聲學行為分析中，fear 與 disgust 出現時音高平均較高；作者解讀為較高的嗓音能量（Hedges' g 數值見 [[2016-emoreact]] 的 Table 4）：
> "the mean of MDQ is lower and the mean of F0 is higher" [[2016-emoreact]] (p. 5)
- 設定不同，不可直接比較：[[2008-fau-aibo]] 是資料庫的音高值人工校正，未做分類實驗；[[2021-pepino-wav2vec2-ser]] 是以音高解釋分類結果的假設；[[2016-emoreact]] 是以 t 檢定與效果量分析兒童視聽影片中音高與情緒出現的關聯。

## 相關實體（Related Entities）
- [[fau-aibo]]（提供人工校正的音高值）

## 矛盾／待釐清
無
