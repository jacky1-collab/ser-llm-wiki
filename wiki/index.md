# 語音情緒辨識（SER）LLM Wiki 總索引

## Papers
<!-- 單篇論文筆記列表，附帶「一句話摘要」與論文類型 -->
- [[2008-fau-aibo]]｜資料集｜介紹 FAU Aibo Emotion Corpus：德國兒童與 Sony Aibo 機器人自發互動的情緒語音資料庫，以詞為單位標註情緒，並規劃釋出時附帶強制基準評測設定。
- [[2021-pepino-wav2vec2-ser]]｜方法｜以預訓練自監督語音模型各層輸出的可訓練加權平均作為淺層神經網路的輸入進行語音情緒辨識，在 IEMOCAP 與 RAVDESS 上優於文獻中僅用聲學資訊的方法。
- [[2016-emoreact]]｜資料集｜介紹 EmoReact：從 YouTube 反應影片蒐集、以群眾外包標註多種情感狀態的兒童視聽情緒資料集，並分析最具指標性的視覺與聲學行為、提供單模態與多模態基線。
- [[2024-ser-evals]]｜基準評測｜提出以多語言、較少被使用的情緒語料評估語音情緒辨識模型域內與域外泛化能力的大規模基準，發現以語音辨識為主要目的的 Whisper 在跨語言情緒辨識上優於專用的自監督模型。

## Entities
<!-- 按 type 分組之實體筆記列表 -->

### Topics & Challenges（主題與挑戰）
<!-- type: topic -->
- [[children-emotion-recognition]]｜兒童情緒辨識（emotion recognition in children）
- [[self-supervised-learning]]｜自監督學習（self-supervised learning, SSL）

### Emotion Taxonomies（情緒標註體系）
<!-- type: taxonomy -->

### Datasets（資料集）
<!-- type: dataset -->
- [[fau-aibo]]｜FAU Aibo Emotion Corpus
- [[emo-db]]｜Emo-DB
- [[emoreact]]｜EmoReact
- [[iemocap]]｜IEMOCAP
- [[msp-podcast]]｜MSP-Podcast

### Features & Representations（聲學特徵）
<!-- type: feature -->
- [[pitch]]｜音高（pitch）

### Models & Architectures（模型與架構）
<!-- type: model -->
- [[wav2vec2]]｜wav2vec 2.0

### Metrics & Benchmarks（評測指標）
<!-- type: metric -->
- [[ser-evals]]｜SER Evals

## Synthesis
<!-- 5 篇跨論文綜合分析頁面（待 5 篇論文 Ingest 完畢後建立） -->
