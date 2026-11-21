---
title: "Releasing a thoroughly annotated and processed spontaneous emotional database: the FAU Aibo Emotion Corpus"
authors: ["A. Batliner", "S. Steidl", "E. Nöth"]
year: 2008
type: dataset
pdf: "raw/2008-fau-aibo.pdf"
one_sentence_summary: "介紹 FAU Aibo Emotion Corpus：德國兒童與 Sony Aibo 機器人自發互動的情緒語音資料庫，以詞為單位標註情緒，並規劃釋出時附帶強制基準評測設定。"
---

# Releasing a thoroughly annotated and processed spontaneous emotional database: the FAU Aibo Emotion Corpus

## 基本資訊
- **篇名**：Releasing a thoroughly annotated and processed spontaneous emotional database: the FAU Aibo Emotion Corpus
- **作者**：A. Batliner、S. Steidl、E. Nöth（Friedrich-Alexander-University Erlangen-Nuremberg, FAU）
- **發表年份**：2008
- **發表會議／期刊**：Proc. of a Satellite Workshop of LREC 2008 on Corpora for Research on Emotion and Affect, Marrakesh
- **論文類型**：資料集
- **原始檔案**：raw/2008-fau-aibo.pdf

## 研究動機與欲解決問題（Problem & Motivation）
- 作者指出，一般共識是應以非演出（non-acted）的情緒資料庫為目標，因為分類器必須用盡量接近「真實」資料的資料來訓練 (p. 1)。
> "non-acted emotional databases should be aimed at" (p. 1)
- 錄製與標註自發情緒資料庫的成本遠高於演出資料；目前可取得的是演出資料庫，例如柏林情緒語音資料庫（Emo-DB）與丹麥情緒語音資料庫（DES），作者表示據其所知沒有條件相近的自發資料庫可取得 (p. 1)。
- 隱私也常使這類資料無法釋出給第三方 (p. 1)：
> "privacy reasons often prevent such data to be released to third parties" (p. 1)
- 因此作者認為，取得自發資料是「realistic」情緒處理與分類最嚴重的瓶頸 (p. 1)：
> "access to spontaneous data is the most severe bottleneck for" (p. 1)
- 此資料庫過去在多篇論文中只有簡短描述；作者決定將其釋出供科學使用，本文提供各面向、標註與使用條件的濃縮總覽 (p. 1)。
- 此外作者指出，因為缺乏可自由取得的自發資料庫，跨研究的效能比較實際上不可能；即使是演出資料庫，研究者也常未選用完全相同的樣本 (p. 4)。

## 方法與架構（Methodology & Architecture）
**資料蒐集**
- 蒐集時程：於 2002 [本文] (p. 1) 至 2004 [本文] (p. 1) 年在 EU 計畫 PF-STAR 中蒐集並處理；2005 [本文] (p. 1) 至 2007 [本文] (p. 1) 年在 CEICES 倡議（NoE HUMAINE 內）內外進一步標註與處理 (p. 1)。
- 情境：人機溝通、兒童語音（children's speech），以及情緒使用者狀態的誘發與辨識；機器人為 Sony 的 AIBO (p. 1)。
- 綠野仙蹤法（Wizard-of-Oz）：兒童被告知像對朋友說話一樣對 Aibo 說話，並以為 Aibo 會回應指令；實際上 Aibo 由人類操作員以「Aibo Navigator」軟體透過無線區域網路遙控，未使用 Aibo 內建語音辨識模組 (p. 1)。
> "The wizard causes the Aibo to perform a fixed, pre-determined sequence of actions, which takes no account of what the child says" (p. 1)
- 動作序列刻意在服從與不服從之間取捨，以誘發情緒行為，但不讓兒童中途放棄實驗 (p. 1)。
- 錄音地點為學校 Mont 與 Ohm 的教室；語音以無線頭戴式麥克風傳輸、以 DAT 錄音機錄製 (p. 1)。
- 取樣率 48 kHz [本文] (p. 1)，量化 16 bit [本文] (p. 1)，之後降頻至 16 kHz [本文] (p. 1)。
- 每次錄音約 30 分鐘 [本文] (p. 2)。
- 切分 turn：自動切分語音檔，停頓達 1.5 秒 [本文] (p. 2) 以上即設為 turn 邊界；此處的「turn」不具語言學意義 (p. 2)。

**轉寫與詞彙表**
- 正字轉寫採精簡的 VERBMOBIL 記法，由進階學生完成並經督導交叉檢查；音標詞彙表採 SAMPA 記法 (p. 2)。
- 另建立句法－語意詞彙表，含粗略的詞性（part-of-speech, POS）標籤與粗略的高層語意標籤 (p. 2)：
> "with coarse part-of-speech (POS) labels per word (six classes)" (p. 2)

**以詞為單位的情緒標註（word-based annotation）**
- 作者將詞視為最小的情緒單位 (p. 2)：
> "We conceive the word as the smallest possible emotional unit" (p. 2)
> "By annotating word-based, we are later on free to map words onto longer units." (p. 2)
- 標註者組成：
> "Five labellers (advanced students of linguistics, 4 females, 1 male)" (p. 2)
- 標註者依序聆聽語音檔，彼此獨立地為每個詞標註為 neutral 或其他類別之一，類別是檢視資料後得出 (p. 2)：
> "annotated independently from each other each word as neutral (default) or as belonging to one of ten other classes" (p. 2)
- 多數決（majority voting, MV）規則 (p. 2)：
> "if three or more labellers agree, the label is attributed to the word" (p. 2)
> "if four or five labellers agree, we assume some sort of prototypes" (p. 2)

**子樣本劃分（AMEN 子集）**
- 只取 MV 數超過 50 [本文] (p. 2) 的標籤，構成 7 類 [本文] (p. 2) 問題；但類別分布非常不平衡 (p. 2)。
- 因此對 neutral 與 emphatic 降取樣，並把 touchy、reprimanding 與 angry 合併為 Angry，形成較平衡的 4 類 [本文] (p. 2) 問題 AMEN（Angry、Motherese、Emphatic、Neutral）(p. 2)。
> "Cases where less than three labellers agreed were omitted as well as those cases where other than these four main classes were labelled." (p. 2)
- 作者表示此子樣本將定義為主要「canonical」樣本（的基礎）(p. 2)。

**對應到 turn 與 chunk**
- 作者認為簡單的 50% [本文] (p. 2) 門檻並不理想，因為部分詞（尤其功能詞）不太可能以帶情緒的方式說出 (pp. 2–3)。
- 以片段（fragments）與助動詞（auxiliaries）為停用詞，加總每個 turn 內 5 位標註者 [本文] (p. 3) 給出的標籤 (p. 3)。
- turn 判為 neutral 需有 70% [本文] (p. 3) 標籤為 neutral；非 neutral 標籤達 30% [本文] (p. 3) 以上時，turn 為 A、M 或 E；非 neutral 標籤中至少 50% [本文] (p. 3) 為 M 時判為 M；A 與 E 相等時判為 A；既非 A 也非 M 則為 E (p. 3)。
- 作者稱此為一種「markedness」條件：M 比 A 有標，A 比 E 有標，三者皆比 N 有標 (p. 3)。
- chunk：先以粗略的句法邊界系統標註整個資料庫，再用與 turn 類似的對應規則；規則將於另一篇即將發表的論文中以結構圖說明 (p. 3)。

**人工校正**
- 以轉寫做自動強制對齊（forced alignment），並對整個資料庫的自動詞切分做人工校正；3990 [本文] (p. 3) 個 AMEN turn 的切分由第一作者交叉檢查 (p. 3)。
- 音高（pitch）：除自有的音高偵測演算法（pitch detection algorithm, PDA）外，另以一個知名的逐框 PDA 為基線，並人工校正其數值；此項針對 3990 [本文] (p. 3) 個 AMEN turn，由第一作者完成 (p. 3)。

**其他附加標註、軟體與資料類型**
- 標註 Aibo 的 [± co-operative] 動作，但因工作量只標了約一半資料；不在預設釋出內容中，可依雙邊協議提供 (p. 3)。
- 已釋出兩套軟體：EDE（Evaluating Decoders using Entropy）與 eLabel（Labelling of Emotions）(p. 3)。
- CEICES 倡議中發展了特徵編碼規格，以 ASCII 為基礎，可依需求提供 (p. 3)。
- 除近講麥克風錄音外，另有攝影機麥克風錄音（含噪音與迴響）與人工加迴響的錄音，可依雙邊協議提供 (pp. 3–4)。

## 實驗設定（Experimental Setup）
不適用（本文未進行分類實驗，僅定義將隨資料庫提供的評測設定）。
- 作者計畫在釋出內容中定義「evaluation setting」並提供該設定的分類結果作為基準，該設定的處理將為強制 (p. 4)：
> "a simple two-fold cross-validation which can be computed with rather low effort" (p. 4)
> "its processing – in addition to any other processing – will be mandatory" (p. 4)

## 核心數據與成果（Key Results & Metrics）
**整體規模**
- 兒童：51 位兒童 [本文] (p. 1)，年齡 10 [本文] (p. 1) 至 13 歲 [本文] (p. 1)，男性 21 [本文] (p. 1)、女性 30 [本文] (p. 1)。
- 語音總長約 9.2 小時 [本文] (p. 2)；全部詞數 48401 [本文] (p. 2)。
- 標註者：5 位標註者 [本文] (p. 3)。

**各類 MV 詞數**
- joyful：101 [本文] (p. 2)
- surprised：0 [本文] (p. 2)
- emphatic：2528 [本文] (p. 2)
- helpless：3 [本文] (p. 2)
- touchy（irritated）：225 [本文] (p. 2)
- angry：84 [本文] (p. 2)
- motherese：1260 [本文] (p. 2)
- bored：11 [本文] (p. 2)
- reprimanding：310 [本文] (p. 2)
- rest（非 neutral 但不屬其他類別）：3 [本文] (p. 2)
- neutral：39169 [本文] (p. 2)
- 無 MV 的詞：4707 [本文] (p. 2)

**AMEN 子集（詞層級）**
- Angry（A）：1557 [本文] (p. 2)
- Motherese（M）：1224 [本文] (p. 2)
- Emphatic（E）：1645 [本文] (p. 2)
- Neutral（N）：1645 [本文] (p. 2)
- 加權 kappa（weighted kappa）：0.59 [本文] (p. 2)

**轉換為 turn 的統計**
- 含 AMEN 詞的 turn：AMEN 詞 6070 [本文] (p. 3)，對應 17618 [本文] (p. 3) 個詞、3996 [本文] (p. 3) 個 turn。
- 停用詞：片段 596 [本文] (p. 3)、助動詞 196 [本文] (p. 3)（有些詞兩者皆是），剩餘 16856 [本文] (p. 3) 個詞。
- turn 標籤：A 868 [本文] (p. 3)（21.7% [本文] (p. 3)）、E 1347 [本文] (p. 3)（33.7% [本文] (p. 3)）、M 495 [本文] (p. 3)（12.4% [本文] (p. 3)）、N 1280 [本文] (p. 3)（32.0% [本文] (p. 3)），合計 3990 [本文] (p. 3)。
- turn 最長可達 53 [本文] (p. 3) 個詞。

**成本**
作者在註腳中自稱為非常粗略的估計 (p. 4)：
> "A (very!) coarse estimate of our expenses" (p. 4)
> "amounts to > 80 K Euros for researchers and students" (p. 4)

## 核心貢獻與作者觀點（Contributions & Insights）
- [作者聲稱] 資料庫將釋出供科學使用，授權協議中計畫納入強制的基準設定，使跨研究單位的比較成為可能 (p. 1)。
- [作者聲稱] 以詞為最小情緒單位標註，之後可自由對應到更長的單位，從而依經驗找出「最佳」分析單位 (p. 2)。
- [作者聲稱] 資料相當能代表真實資料：「classic」大情緒很少、分布非常偏斜，並出現 motherese 這類情緒相關狀態 (p. 2)。
- [作者聲稱] 人工校正的切分可排除錯誤切分造成的誤判，使不同方法間的比較更可靠 (p. 3)。
- [作者聲稱] 帶有校正音高值的資料庫很少，作者不知道有其他情緒資料庫具備這種校正值 (p. 3)。
- [作者聲稱] chunk 在句法上（因而在語意上）有明確定義，作者認為 chunk 是較理想的單位 (p. 3)。
- [作者聲稱] 依作者經驗，方便的子樣本選擇對分類效能的影響常大於特徵選擇程序或分類器的選擇，因此需要基準設定 (p. 4)。
- [作者聲稱] 自動情緒分類領域仍在起步階段，作者期望以此資料庫的基準設定形成「islands of standardization」(p. 4)。

## 論文提及之局限性（Limitations & Future Work）
- 情緒類別只適用於此特定情境中的這些兒童，作者不主張其代表兒童情緒的一般情況 (p. 2)：
> "only that they are adequate for the modelling of the behaviour of these children in this specific scenario" (p. 2)
- 類別分布非常不平衡 (p. 2)：
> "the distribution of classes is very unbalanced" (p. 2)
- turn 並非理想單位 (p. 3)：
> "As they can consist of up to 53 words, they are not really optimal" (p. 3)
- 人工校正的音高值不是 ground truth，且偏向所使用的自動 PDA；因時間限制未做 pitch-synchronous 校正 (p. 3)：
> "Such manually corrected pitch values do not constitute a ground truth" (p. 3)
- [± co-operative] 標註只涵蓋約一半資料 (p. 3)：
> "only for roughly half of the data" (p. 3)
- 錄影因隱私不會提供 (p. 4)：
> "for privacy reasons, the video recordings will not be available" (p. 4)
- 作者另指出，建立資料庫成本高，而規模再大上某個量級的資料庫是此領域標準化的前提之一 (p. 4)：
> "databases greater by some order of magnitude would be one prerequisite for standardization" (p. 4)

## 提及實體清單（Referenced Entities）
- [[fau-aibo]]（本篇核心貢獻）
- AMEN 子集（未達建頁門檻）
- 多數決（majority voting, MV）（未達建頁門檻）
- 加權 kappa（weighted kappa）（未達建頁門檻）
- [[emo-db]]
- DES（未達建頁門檻）
- 綠野仙蹤法（Wizard-of-Oz）（未達建頁門檻）
- [[children-emotion-recognition]]（本篇寫作 children's speech）
- [[pitch]]（另提及音高偵測演算法（PDA），未達建頁門檻）
- two-fold cross-validation（未達建頁門檻）
- 以詞為單位的情緒標註（word-based annotation）（未達建頁門檻）
- chunk（未達建頁門檻）

## 矛盾／待釐清
1. **AMEN 詞數（論文內部數字不一致）**：AMEN 四類詞數 1557 [本文] (p. 2)、1224 [本文] (p. 2)、1645 [本文] (p. 2)、1645 [本文] (p. 2) 相加後，比後文所寫的 AMEN 詞數 6070 [本文] (p. 3) 多出一個詞。論文未說明原因，此處並列原文、不選邊：
> "1557 words for Angry (A), 1224 words for Motherese (M), and 1645 words each for Emphatic (E),and for Neutral (N), are used" (p. 2)
> "for the turns containing our 6070 AMEN words" (p. 3)
2. **turn 數（論文未說明差異原因）**：含 AMEN 詞的 turn 數為 3996 [本文] (p. 3)，同段 turn 標籤合計為 3990 [本文] (p. 3)；論文未說明兩者差異的原因。
> "this means 17618 words, 3996 turns" (p. 3)
> "summing up to 3990 (100 %) labels = turns" (p. 3)
