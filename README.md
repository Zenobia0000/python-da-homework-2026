<<<<<<< HEAD
# iSpan Python Data Analysis Cookbooks

> **一套經過教室實戰淬鍊的 Python 資料分析開源教材**
> 從零基礎到 GPU 加速，從單檔 Notebook 到可部署的 Python 專案架構——一次給齊。

本專案收錄作者多年於資策會 (iSpan) 授課過程中不斷迭代、補強、重寫的教學素材。所有內容以 **公開、可重現、可自學** 為原則整理成 cookbook（食譜本）形式：每一個章節都是可以直接打開就跑的 Notebook，每一個範例都對應一個真實世界的資料問題。

如果你正在尋找一套不只是「API 教學」、還想帶你建立**資料分析師思維方式**的中文教材——歡迎在這裡留下一顆 Star，然後選擇最適合你目前程度的路徑開始。

---

## 為什麼要再做一套資料分析教材？

市面上 NumPy / Pandas / Matplotlib 的教學資源並不少，但實際帶過上百位學員後，我們發現學習者卡關的點幾乎都不是「語法」，而是：

- **看得懂別人的程式，卻寫不出自己的分析**——缺少從需求到程式碼的轉譯訓練。
- **跑得動 Notebook，卻搬不進專案**——不知道如何把探索性程式整理成可維護的模組。
- **會算平均數，卻不知道怎麼把結果講成故事**——視覺化停留在「畫得出來」而不是「說得清楚」。
- **學得完基礎，卻跨不進效能/規模化**——沒人告訴他們 GPU、ETL、自動化測試的入口在哪裡。

本專案用**分級、貫穿、可驗證**三個原則重新組織教學路徑，讓學員可以從入門一路走到進階，而不需要重新找教材、重新學語法。

---

## 三條學習路徑：選一條開始

本 Repo 提供三個對應不同程度與不同學習目的的教材版本，它們共用資料集與命名規則，彼此之間可以無縫接軌。

### 1. Classic Edition — 完整章節式入門

**路徑**：`Classic-Edition_python_DA/`

如果你是 **第一次碰資料分析**，或希望用最傳統、最扎實的方式把 NumPy / Pandas / Matplotlib / Seaborn 一個指令一個指令學過去，這是最適合的版本。

- `numpy/`：陣列建立、基礎運算、進階數值運算（4 章）
- `pandas/`：Series / DataFrame 基礎 → 資料清理 → 時間序列 → 特徵工程 → 多變量統計檢定（12+ 章）
- `data_vis/`：Matplotlib、Seaborn 與小型視覺化專題

> **適合對象**：完全沒接觸過資料分析的初學者、想系統性補齊基礎的轉職者。

---

### 2. Special Edition — 12 小時精煉課程 + 自動批改作業系統

**路徑**：`Special-Edition_python_DA/`

這是作者為企業內訓與短期密集課程設計的 **6 個 Session × 2 小時** 精煉版本。全程用 **一個電商銷售貫穿式案例** 串起，從 NumPy 向量化思維一路帶到 Plotly 互動 Capstone。

| Session | 主題 | 核心工具 |
|---|---|---|
| S1 | NumPy 與向量化思維 | NumPy |
| S2 | Pandas I/O 與資料清理（ETL 第一哩路） | Pandas |
| S3 | Pandas 轉換：groupby / merge / pivot | Pandas |
| S4 | 時間序列 + EDA 實戰 | Pandas |
| S5 | 視覺化精華：5 種必懂圖 | Matplotlib + Seaborn |
| S6 | Plotly 互動 + Capstone | Plotly |

更特別的是，這個版本附上了 **`homework-template/`——一套基於 GitHub Actions 的自動批改作業系統**。學生 Fork → 寫作業 → Push → 發 PR，自動跑測試、自動打分、自動生成成績單。對想要自行開班授課的講師來說，這是一份可以直接拿去用的完整 CI/CD 教學基礎建設。

> **適合對象**：時間有限的在職工作者、想在 12 小時內建立資料分析工作流程的學員、想要自動化批改作業的講師。

---

### 3. Master Advance — 進階主題與工程化

**路徑**：`Master-Advance/`

當你已經會用 Pandas 處理資料，下一步會遇到的問題往往不再是「怎麼寫這個函式」，而是「我寫的程式能不能跑得快、擴得開、維護得住」。這個目錄收錄四個進階方向：

#### `acceleration/` — GPU 加速與 RAPIDS 實戰

從 Numba CUDA 入門，一路走到 CuPy / cuDF / cuML / cuGraph 與 Dask-CUDA 多卡處理，並以一個端到端的資料分析 pipeline 作為收尾。**如果你的 Pandas 已經跑到 CPU 極限，這裡就是你的下一站。**

- 01 `Introduction to CUDA Python with Numba`
- 02 `GPU Acceleration Overview & Environment Setup`（含 Apple Silicon 替代方案說明）
- 03 `CuPy: GPU-Accelerated NumPy`
- 04 `cuDF: GPU-Accelerated DataFrames`
- 05 `cuML: GPU-Accelerated Machine Learning`
- 06 `cuGraph: GPU-Accelerated Graph Analytics`
- 07 `Dask-CUDA: Multi-GPU & Large-Scale Processing`
- 08 `RAPIDS End-to-End Data Analysis Pipeline`

#### `ETL_course/` — 從 Notebook 到資料工程

模組化的 ETL 課程，涵蓋檔案 I/O、SQL + Python 整合、日誌系統、配置管理、Python 工具函式與整合型 Capstone。這是把「分析師腳本」升級成「可排程、可監控、可交接」資料管線的必經之路。

#### `Python_project_sample/` — 從函數寫到類別、從類別寫到專案

資料分析師最常被忽略的一塊：**軟體工程素養**。本子專案提供：

- `oop_course/`：完整的 Python 物件導向系列課程，涵蓋模組、套件、檔案路徑處理、OOP 基礎、繼承、封裝、多型、設計模式。
- `tutorials/`：10 篇循序漸進的 Markdown 教學文件，從模組匯入一路講到設計模式，是對新人做技術 Onboarding 的現成教案。
- `examples/`、`OOP/`：可跑的範例專案與範本結構。

> 當你把一份 Notebook 拆成模組、寫成套件、加上測試、發佈到 PyPI——你就不再只是會用 Python 的分析師，而是**能交付可維護系統的資料工程師**。

#### `competition/` — 競賽視角的統計與實戰

收錄智慧醫療假設檢定、智慧製造 SPC 管制圖、推論統計、Kaggle 獲獎技巧等實戰案例。用比賽的高強度情境訓練分析肌肉。

---

### 附加資源：`slides/`

- `Sunny_python_數據分析.pdf`——作者課堂使用的完整投影片
- `python-adv-key-point.xmind`——進階主題心智圖

---

## 快速開始

選擇一條路徑，進入對應目錄，依照裡面的 `README.md` 指示即可。若要一鍵安裝所有入門套件：

```bash
pip install numpy pandas matplotlib seaborn plotly jupyter pytest
```

進階課程（GPU / ETL）的相依套件請見各子目錄的 `requirements.txt`。

### 建議學習路徑

| 你的現況 | 建議起點 |
|---|---|
| 完全沒寫過 Python 資料分析 | Classic Edition → numpy/ |
| 會 Python、想快速吸收資料分析能力 | Special Edition → S1 |
| 已經會 Pandas，想突破效能瓶頸 | Master-Advance → acceleration/ |
| 想把 Notebook 升級成真實專案 | Master-Advance → Python_project_sample/ |
| 準備開課、需要現成教案與批改系統 | Special Edition → homework-template/ |

---

## 貢獻與授權

本專案以開源形式釋出，歡迎：

- 發 **Issue** 回報 Notebook 執行錯誤、說明不清楚或版本相容性問題
- 發 **Pull Request** 補充範例、翻譯、勘誤、新增測試
- **Fork** 本 Repo 改作為自己的教學教材（請保留原始出處）
- 在你的學習筆記、技術部落格、讀書會中引用本 Repo 的內容

如果這份教材對你的學習或教學有幫助，**給本專案一顆 Star** 是對作者最直接的鼓勵。

---

## 關於作者

本專案由作者於資策會 (iSpan) 開設 Python 資料分析系列課程期間持續累積而成。課堂上的每一次提問、每一個卡關、每一份學員專題，都被逐步整理回教材裡——因此你在這裡看到的不是一份「寫完就放著」的教學文件，而是一份**仍在每個新梯次持續被迭代**的活教材。

課程資訊、企業包班、公開班梯次與合作邀約，請循資策會官方管道聯繫；線上內容與社群交流則歡迎透過本 Repo 的 Issue / Discussion 進行。

---

> **學資料分析，不只是學套件；是學一種看世界的方式。**
> 願這份 cookbook 能陪你走完從「跑得動」到「說得清」、從「看得懂」到「做得出」的那段旅程。
=======
# Python 資料分析 — 自動批改作業系統

> **第一次用？** 請先讀 [Git/CI/CD/PR 教學手冊 →](docs/STUDENT_GUIDE.md)
>
> **前置條件**：你已從老師取得**作業 repo**的 GitHub 連結（**不是課程 cookbook**），且本機已安裝 Git。

## 繳交流程（4 步驟）

### Step 1：Fork 老師給的作業 repo

1. 打開老師提供的作業 repo 連結（網址結尾通常是 `xxx-homework` 之類）
2. 點擊右上角 **「Fork」** 按鈕，建立你自己的副本
3. 完成後，你的 fork 會在 `https://github.com/<你的帳號>/<repo 名稱>`

> ⚠️ 不要 fork 整個課程 cookbook — 那不會觸發批改。

### Step 2：Clone 你的 fork 並驗證 remote

```bash
git clone https://github.com/<你的帳號>/<repo 名稱>.git
cd <repo 名稱>

# 必做：確認 remote 指向你自己的 fork
git remote -v
```

預期輸出（`origin` 必須是你的帳號）：

```
origin  https://github.com/<你的帳號>/<repo 名稱>.git (fetch)
origin  https://github.com/<你的帳號>/<repo 名稱>.git (push)
```

> 如果 `origin` 不是你的帳號，Step 3 一定會 `permission denied`。請見[常見錯誤](#-常見錯誤)。

### Step 3：寫作業 → commit → push

編輯 `homework/` 內的 `.py` 檔，完成後：

```bash
git add homework/
git commit -m "完成 M1 作業"
git push
```

> push 失敗？見[常見錯誤](#-常見錯誤)。

### Step 4：發 PR 繳交

1. 到你 fork 的 repo 頁面
2. 點 **「Contribute」** → **「Open pull request」**
3. PR 標題寫：`M1 作業 — 你的姓名`
4. 點 **「Create pull request」**

> 每次 push 新的 commit，都會自動重新批改。可以無限次修改重交。

### 查看成績

批改結果會出現在你發的 **PR 留言區**：分數 + 每題對錯表 + 失敗原因。回到 PR 頁面往下滑就看得到。

> 解答不會自動發放。老師會在作業截止後統一公布。

---

## 作業列表

| 作業檔案 | 對應課程 | 滿分 |
|:---------|:---------|:----:|
| `homework/m1_numpy.py` | M1 NumPy 向量化思維 | 100 |
| `homework/m2_pandas_cleaning.py` | M2 Pandas I/O 與資料清理 | 100 |
| `homework/m3_pandas_advanced.py` | M3 Pandas 進階：merge / groupby / RFM | 100 |
| `homework/m4_timeseries.py` | M4 時間序列與 EDA | 100 |
| `homework/m5_visualization.py` | M5 Matplotlib & Seaborn 視覺化 | 100 |
| `homework/m6_plotly_capstone.py` | M6 Plotly 互動儀表板 & Capstone | 100 |
| | **總計** | **600** |

每份作業都是 🟢 送分題 30 分 + 🟡 核心題 45 分 + 🔴 挑戰題 25 分

---

## 本地測試（選用）

```bash
pip install -r requirements.txt

# 測試單一模組
python -m pytest tests/test_m1.py -v

# 測試全部
python -m pytest tests/ -v
```

## 專案結構

```
├── homework/               ← 你要編輯的作業檔案
│   ├── m1_numpy.py
│   ├── m2_pandas_cleaning.py
│   ├── m3_pandas_advanced.py
│   ├── m4_timeseries.py
│   ├── m5_visualization.py
│   └── m6_plotly_capstone.py
├── tests/                  ← 自動測試（不要改）
├── grader/                 ← 評分引擎（不要改）
├── datasets/ecommerce/     ← 資料檔（不要改）
├── docs/
│   └── STUDENT_GUIDE.md    ← Git/CI/CD/PR 教學手冊
└── .github/workflows/      ← CI/CD 設定（不要改）
```

---

## 🚨 常見錯誤

### `! [remote rejected] main -> main (permission denied)`

「驗證成功，但你沒有寫入權」。兩種可能：

**狀況 1：remote URL 不是你的 fork**

```bash
# 檢查 remote
git remote -v

# 若 origin 指向別人（老師、課程 cookbook）的 repo，改成你的 fork
git remote set-url origin https://github.com/<你的帳號>/<repo 名稱>.git
git push
```

> 另一種誤觸發：在課程 cookbook 的子目錄裡執行 `git push` — 因為 `.git` 在 cookbook 根目錄，會 push 到 cookbook 的 remote。請務必在你 clone 的 fork repo 內操作。

**狀況 2：URL 對了，但 git 用了「另一個 GitHub 帳號」的 token 認證（多帳號用戶才會撞）**

如果你在同一台電腦登入過多個 GitHub 帳號（例如公司 + 個人 + 學校），git 的 credential helper 會快取上一個登入的 token。push 時用錯 token → 被認成別人 → 沒有寫入權 → permission denied。

```bash
# 1. 檢查 gh CLI 目前用哪個帳號（Active account 那行）
gh auth status

# 2. 切到你 fork 所屬的帳號
gh auth switch -u <你的帳號>

# 3. 如果該帳號還沒登入過，加進來
gh auth login    # 選 GitHub.com → HTTPS → Login with a web browser

# 4. 重新 push
git push
```

> 沒裝 `gh` 也可以：清掉 credential helper 的快取（macOS：`git credential-osxkeychain erase` 鍵入 `host=github.com` + 兩個 Enter；Linux：`git config --global --unset credential.helper` 後重 push 會跳出帳密輸入框）。

### `Updates were rejected because the remote contains work...`

GitHub 上有你本機沒有的 commit，先合併再 push：

```bash
git pull --rebase
git push
```

### `Authentication failed` / 一直要求帳密

GitHub 已停用密碼登入。請設定 [Personal Access Token 或 SSH Key](docs/STUDENT_GUIDE.md#q-git-push-要求輸入帳號密碼)。

---

## 老師專區

### 初次部署 — 將此模板發布為獨立 repo（**排除 solutions**）

⚠️ 兩個必須遵守的點：
1. `homework-template/` 在課程 cookbook 內是**子目錄**，GitHub Actions 只認 repo 根目錄的 `.github/workflows/` → **必須先發布為獨立 repo**
2. `solutions/` **絕對不能進公開 repo** — 學生 fork 後就能直接 `cat` 看解答。批改本身不需要 solutions（tests/ 已含期望值），所以排除掉就好

```bash
# 1. 在 GitHub 建立新 repo（例：python-da-homework-2026），先不要勾選任何初始化選項

# 2. 用 rsync 複製到暫存區，排除 solutions/
rsync -a --exclude='solutions' --exclude='.git' \
  Special-Edition_python_DA/homework-template/ /tmp/homework-deploy/

# 3. 推到新 repo
cd /tmp/homework-deploy
git init -b main
git add .
git commit -m "init: homework template"
git remote add origin https://github.com/<老師帳號>/python-da-homework-2026.git
git push -u origin main

# 4. 在新 repo Settings → Actions → General → Workflow permissions
#    選 "Read and write permissions"，否則機器人無法在 PR 上留言/貼 label

# 5. 把新 repo URL 給學生，作為 Step 1 的 fork 來源
```

驗收：自己 fork 一份 → clone → 確認**沒有** `solutions/` 資料夾 → 改個 `homework/m1_numpy.py` → push → 發 PR → 確認 PR 留言區出現分數。

> 老師本地的 `homework-template/solutions/` 保留即可 — 用於維護題目、本地驗證 grader、截止後手動公布解答。

### 查看全班繳交狀況

到 repo 的 **Pull requests** 頁籤，可以看到所有學生的 PR。
- 有 `graded` label = 已批改
- `score:A` ~ `score:F` label = 成績等級

### 匯出成績總表

1. 到 **Actions** 頁籤
2. 點左側 **「📋 彙整全班成績」**
3. 點右側 **「Run workflow」**
4. 完成後在 Job Summary 看表格，或下載 `grades.csv`
>>>>>>> 1280745d3a2b247599c4d5ddd09519d9b85c9974
