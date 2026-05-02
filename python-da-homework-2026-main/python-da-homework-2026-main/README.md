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
