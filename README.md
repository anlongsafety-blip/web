# 安隆安全網有限公司 - 官方網站

> 多頁式品牌網站｜兩大品牌：安隆安全（工程級）+ 安隆居家（住宅用）

## 網站結構（6 頁主站 + 24 頁產品詳細頁）

```
anlong-website/
├── index.html              ← 首頁（雙品牌介紹、精選產品、精選案例）
├── products.html           ← 產品型錄（全部 24 項，可篩選品牌與分類）
├── cases.html              ← 施工案例（16 個指標案場）
├── about.html              ← 關於安隆（公司介紹、四大駐點）
├── faq.html                ← 常見問題（8 大常見問題 + FAQPage JSON-LD）
├── contact.html            ← 聯絡我們（電話、LINE、表單、服務區域）
│
├── products/
│   ├── safety/  (12 個工程級產品頁)
│   └── home/    (12 個居家用產品頁)
│
├── styles.css              ← 樣式（雙品牌主題色透過 CSS Variables 切換）
├── script.js               ← 互動（含 localStorage 品牌記憶）
├── sitemap.xml             ← 共 30 筆 URL（Google 索引用）
├── robots.txt              ← 搜尋引擎爬蟲指引
│
├── generate-pages.py       ← 生成主要頁面（6 頁）
└── generate-products.py    ← 生成產品詳細頁（24 頁）+ sitemap
```

## 兩大特色

### 1. 雙品牌主題切換
網站隨時可切換兩大品牌的視覺主題色：
- **安隆安全（SAFETY）** → 主色 `#4a8c8c`（湖水綠／專業沉穩）
- **安隆居家（HOME）** → 主色 `#e87722`（暖橘／溫馨親近）

切換方式：點擊首頁、產品頁或案例頁的品牌按鈕。**選擇後會記住，切換到其他頁面也會保持**（使用 localStorage）。

### 2. SEO 完整佈署
- 每頁有獨立 `<title>`、`<meta description>`、`<canonical>`
- BreadcrumbList 麵包屑結構化資料（每頁皆有）
- LocalBusiness 結構化資料（首頁）
- FAQPage 結構化資料（FAQ 頁，可在 Google 上顯示精選摘要）
- WebSite 結構化資料（首頁）
- Open Graph 標籤（Facebook / LINE 分享預覽）
- 完整 sitemap.xml（30 筆 URL）
- robots.txt
- Google Search Console 驗證 meta 已內建

## 上線前必做的 3 件事

### 1. 換掉 GA4 追蹤碼
全網站搜尋 `G-XXXXXXXXXX` 並改成您的實際 ID。

開啟終端機，到網站資料夾後執行：
```bash
# Mac/Linux
find . -name "*.html" -exec sed -i '' 's/G-XXXXXXXXXX/G-您的ID/g' {} \;

# 或手動：用 VS Code 全專案搜尋取代
```

### 2. 確認 Search Console 驗證碼
首頁、各主要頁面與所有產品頁的 `<head>` 內都已加入：
```html
<meta name="google-site-verification" content="n2u56H6tGekvNenjobW76FdALH_lMMqFdFpkvfZbAXA" />
```
如需要換新 token，請修改 `generate-pages.py` 與 `generate-products.py` 開頭的 `SC_TOKEN` 後重新執行。

### 3. 提交 sitemap 給 Google
登入 Google Search Console → 左側「Sitemap」→ 輸入：
```
https://www.anlongsafety.com.tw/sitemap.xml
```

## 維護方式

### 簡單修改（推薦給非技術用戶）
直接用 VS Code 或記事本打開 `.html` 檔修改文字，存檔後上傳即可。

### 大量修改（推薦給有 Python 基礎）
1. 修改 `generate-pages.py` 內的 `CASES`、`FAQS` 等資料
2. 修改 `generate-products.py` 內的 `PRODUCTS` 字典
3. 依序執行：
   ```bash
   python3 generate-pages.py     # 生成 6 個主要頁面
   python3 generate-products.py  # 生成 24 個產品頁 + sitemap
   ```

## 部署選項

### 選項 A：GitHub Pages（免費 + 自動 HTTPS，推薦）
1. 把整個 `anlong-website/` 上傳到 GitHub repository
2. Settings → Pages → 選 `main` 分支
3. 等 1-3 分鐘，網站就上線了
4. 可綁定 `www.anlongsafety.com.tw` 自訂網域

### 選項 B：傳統虛擬主機（FTP 上傳）
1. 用 FileZilla 或主機商提供的工具
2. 把整個 `anlong-website/` 內容上傳到主機根目錄（通常是 `public_html/` 或 `htdocs/`）
3. 確認 `index.html` 是首頁

## 聯絡資訊

公司：安隆安全網有限公司
電話：07-7828005　手機：0925-595-175　LINE：@643qzkfp
地址：高雄市大寮區上寮里至學路 571 巷 65 之 2 號
統一編號：50932767
