# 安隆安全網官網 — 開發交接文件

> 這份文件寫給接手的開發者（或 Claude Code）。讀完你會知道：專案是什麼、怎麼跑、每個檔案的角色、有哪些待辦、以及維護時的地雷。
> 最後更新：2026-07（由 Claude 對話模式產出，準備移交 Code 模式）

---

## 1. 專案一句話

台灣「安隆安全網有限公司」的**雙品牌形象官網**，純靜態網站（HTML + CSS + 原生 JS，無框架、無建置流程），部署在 GitHub Pages。核心特色是**即時品牌切換**：全站可在「安隆安全（工程）」與「安隆居家」兩個品牌間即時切換，色系、文案、案例、產品同步變化，不重新載入頁面。

**業主背景**：非技術背景的中小企業主，慣用繁體中文，會一點基礎程式。交付物必須是能直接部署、能自行維護的東西。

---

## 2. 技術棧與限制

- **前端**：純 HTML5 + CSS3 + 原生 JavaScript（ES5/ES6，無 jQuery、無 React、無任何框架）
- **建置**：無。沒有 npm、webpack、vite。檔案即成品，直接丟上主機就能跑
- **樣式**：單一 `styles.css`（約 3500 行），使用 CSS 變數（`--primary`、`--accent` 等）做品牌換色
- **腳本**：單一 `script.js`（約 340 行），兩個 IIFE 模組（主功能 + hero 輪播）
- **部署**：GitHub Pages，repo 為公開，網站在 `/web/` 子目錄下
  - 目前網址：`https://anlongsafety-blip.github.io/web/`
  - 未來正式網域：`https://www.anlongsafety.com.tw`（尚未綁定）
- **字型**：Google Fonts（Noto Sans TC、Noto Serif TC、Cormorant Garamond）
- **圖片**：全部 WebP 格式 + 原生 lazy loading

### ⚠️ 部署鐵律（重要）
1. **秘密金鑰絕不進 repo**：這是公開 repo，任何 API Secret、Token、資料庫密碼放進前端 JS 或 commit，等於公告全世界，數分鐘內會被機器人撈走。秘密只能放伺服器端環境變數。
2. **路徑用相對路徑**：因為部署在 `/web/` 子目錄，所有資源引用都是相對路徑（子目錄頁面用 `../`、`../../`），**不可改成 `/images/...` 這種根目錄絕對路徑**，否則子目錄部署會全部 404。
3. **絕對網址 vs 相對路徑**：`<head>` 裡的 canonical、og:url、JSON-LD 用的是正式網域絕對網址 `https://www.anlongsafety.com.tw/...`；頁面內的資源引用（img/css/js/連結）用相對路徑。這兩者不衝突，但改網域時前者要全站替換。

---

## 3. 檔案結構與角色

```
web/  (= anlong-website)
├── index.html              首頁（含 hero 輪播 banner）
├── products.html           產品型錄總覽
├── cases.html              施工案例總覽（11 張卡，可點進詳細頁）
├── about.html              關於安隆
├── faq.html                常見問題（48 題，9 分類，含表格與 FAQPage JSON-LD）
├── contact.html            聯絡我們（⚠️ 含「假」詢價表單，見待辦）
├── blog.html               安全知識專欄列表頁
│
├── cases/                  11 個案例詳細頁（SEO 地區長尾關鍵字）
│   ├── pingtung-tech.html         屏東科技大學（工程）
│   ├── taoyuan-mingliu.html       桃園名流城寶社區（工程）
│   ├── chiayi-minxiong.html       嘉義民雄新建大樓（工程）
│   ├── hsinchu-elite-school.html  新竹精英國際學校（工程）
│   ├── zhubei-hsr-mall.html       竹北高鐵百貨天井（工程）
│   ├── taipei-flower-market.html  臺北花木市場停車場（工程）
│   ├── lianhua-gas.html           高雄聯華氣體工廠（工程）
│   ├── nkust-bird-net.html        高科大燕巢防鳥網（工程）
│   ├── niaosong-home.html         高雄鳥松住家樓梯（居家）
│   ├── nantou-30.html             南投三十而立社區（居家）
│   └── matsu-fuxing.html          馬祖福興社區大樓（居家）
│
├── blog/                   知識專欄文章
│   ├── _template.html             ⭐ 發新文章的填空模板（37 個【】占位符）
│   ├── cns14252-safety-net-guide.html       CNS14252 法規解析
│   ├── safety-net-material-comparison.html  材質選購指南
│   └── safety-net-pricing-guide.html        價格指南
│
├── products/              24 個產品詳細頁
│   ├── safety/  (工程品牌 12 頁)
│   │   ├── construction-safety-net.html  工地防墜網 ★有實景照
│   │   ├── building-atrium-net.html      大樓天井網 ★有實景照
│   │   ├── bird-prevention-net.html      防鳥網 ★有實景照
│   │   ├── factory-safety-net.html       廠房安全網 ★有實景照
│   │   ├── tile-protection-net.html      防磁磚網
│   │   ├── barrier-net.html              攔截網
│   │   ├── climbing-net.html             攀爬網
│   │   ├── outdoor-court-net.html        戶外球場網
│   │   ├── playground-net.html           遊樂場網
│   │   ├── shade-net.html                遮光網
│   │   ├── solar-panel-net.html          太陽能板網
│   │   └── sports-court-net.html         運動場網
│   └── home/    (居家品牌 12 頁)
│       ├── invisible-grilles.html        隱形鐵窗 ★有實景照 ★唯一金屬製品
│       ├── stairs-safety-net.html        樓梯安全網
│       ├── l-shape-stairs-net.html       L型樓梯網
│       ├── square-stairs-net.html        方型樓梯網
│       ├── triangle-stairs-net.html      三角樓梯網
│       ├── handrail-net.html             扶手網
│       ├── balcony-safety-net.html       陽台安全網
│       ├── window-safety-net.html        窗戶安全網
│       ├── pool-safety-net.html          泳池安全網
│       ├── escalator-net.html            電扶梯網
│       ├── colorful-safety-net.html      彩色安全網
│       └── bumper-strip.html             防撞條
│
├── images/
│   ├── logo/         6 個 logo 檔（webp + png，含深色底白色版）
│   ├── hero/         6 張首頁輪播 banner（1600px，工程4+居家2）
│   ├── cases/        11 案例 × 3 張 = 33 張施工照
│   └── products/     5 張產品實景照（safety/4 + home/1）
│
├── styles.css        全站唯一樣式表（~3500 行）
├── script.js         全站唯一腳本（~340 行）
├── sitemap.xml       45 個 URL
├── robots.txt        含 AI 爬蟲白名單（GPTBot/ClaudeBot/PerplexityBot 等）
│
├── generate-pages.py     ⚙️ 產生器：6 主要頁面（見第 6 節）
├── generate-products.py  ⚙️ 產生器：24 產品頁 + sitemap
│
├── README.md             使用者導向的基本說明
├── HOW_TO_ADD_IMAGES.md  使用者導向的加圖教學
├── 如何新增文章.md        使用者導向的發文教學
└── HANDOFF_交接文件.md    ← 你正在讀的這份（開發者導向）
```

---

## 4. 品牌切換機制（本專案最核心的邏輯，務必理解）

這是全站的靈魂，動任何東西前先搞懂它：

1. **狀態**：`<body data-brand="safety">` 或 `data-brand="home"`，掛在 body 上
2. **持久化**：存在 `localStorage['anlong-brand']`。每頁 `<body>` 開頭有一段 inline script 在頁面繪製前就讀取並套用，避免換頁閃爍：
   ```html
   <script>try{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}catch(e){}</script>
   ```
3. **切換 UI**：導覽列的 `.header-seg`（膠囊分段鈕，`安隆安全 | 安隆居家`），由 `script.js` 的 `bindBrandSwitcher()` 綁定
4. **換色**：CSS 用 `body[data-brand="safety"]` / `body[data-brand="home"]` 覆寫 `--accent` 等變數
   - 工程 accent：`#4a8c8c`（青）／居家 accent：`#e87722`（橘）／主色 `#0f2c4a`（深藍，不變）
5. **內容顯隱**：`.brand-show-safety` / `.brand-show-home` 這兩個 class 控制哪些內容在哪個品牌下顯示。CSS 邏輯是「隱藏不匹配的品牌」：
   ```css
   body[data-brand="safety"] .brand-show-home { display: none; }
   body[data-brand="home"] .brand-show-safety { display: none; }
   ```
   ⚠️ **地雷**：曾出過 bug——早期寫成 `.brand-show-safety{display:block}`，把 grid/flex 的 display 值蓋掉導致版面崩壞。修正原則是「只隱藏不匹配的、不要強制設定匹配的 display 值」，讓元素保留它自然的 display。
6. **hero 輪播連動**：`script.js` 第二個 IIFE 用 MutationObserver 監聽 `data-brand` 變化，切換品牌時輪播會重置並只播該品牌的 banner。

---

## 5. script.js 模組地圖

單檔兩個 IIFE：

**IIFE 1（主功能）** — `init()` 統一初始化
- `setBrand()` / `bindBrandSwitcher()` — 品牌切換（見第 4 節）
- `filterByCategory()` / `bindCategoryFilter()` — 產品分類篩選
- `bindMobileMenu()` — 漢堡選單（<1200px 顯示）
- `bindContactForm()` — ⚠️ 詢價表單，目前只 `console.log` + alert，**沒有真的送出**（見待辦）
- `bindSmoothScroll()` — 錨點平滑捲動，header 偏移 80px

**IIFE 2（hero 輪播）**
- 自動輪播（`INTERVAL = 5500` 毫秒）、圓點、滑鼠停留暫停
- 監聽 `data-brand` 只播對應品牌 banner
- 尊重 `prefers-reduced-motion`

---

## 6. 產生器腳本（generate-*.py）

早期用 Python 批次產生頁面。**注意：這些腳本產生的是初版骨架，之後有大量手動編輯疊加上去**（案例頁、blog、品牌切換、輪播、社群按鈕等都是後來直接改 HTML/CSS/JS 加的）。

- `generate-pages.py`：產生 index/products/cases/about/faq/contact 六頁，內含 CASES、FAQS 資料陣列
- `generate-products.py`：產生 24 產品頁 + sitemap.xml
- 執行順序：先 pages 後 products
- ⚠️ **重要**：**現在直接重跑這些腳本會覆蓋掉所有後續手動修改**（品牌切換、輪播、48題FAQ、社群按鈕全沒了）。除非你要重構整個產生流程，否則**不要重跑**，直接編輯 HTML 檔即可。它們留著僅供理解初始結構與參考。

---

## 7. SEO / GEO 設定現況

業主很重視 SEO 與 GEO（生成式引擎優化，讓 AI 搜尋引擎引用）。已完成：

- **LocalBusiness JSON-LD**：全 46 頁都有，type 為 `HomeAndConstructionBusiness`，含公司名、統編、地址、電話、服務區、`sameAs`（FB + LINE + Google 商家）
- **各頁 JSON-LD**：案例頁有 BreadcrumbList、文章頁有 Article + FAQPage + BreadcrumbList、faq.html 有 48 題 FAQPage
- **語意化 HTML5**：`<header><main><section><article><aside><footer>`
- **robots.txt**：明確允許 GPTBot、OAI-SearchBot、ClaudeBot、PerplexityBot、Google-Extended、Applebot-Extended 等 AI 爬蟲
- **sitemap.xml**：45 個 URL
- **每頁必備**：title、meta description、canonical、og 標籤

**遵循的內容準則**（業主提供的指導方針，寫新內容時請照做）：
- H2/H3 用自然語言問句
- 問句下第一段直接給答案，禁用「這是個好問題」「隨著科技發展」等贅詞
- 步驟用 `<ol>`、資料用 `<table>`
- 論述時與同業/國際標準對比（實體關聯）
- 數據要具體；不確定的資訊留白，禁用「可能/也許」等模糊詞

---

## 8. 待辦事項（TODO，按優先序）

### 🔴 P0 — 上線前必做

1. **GA4 追蹤碼**：全站 46 頁的 `G-XXXXXXXXXX` 是佔位符，需替換成業主申請的真實 Measurement ID。
   - 位置：每頁 `<head>` 的 gtag script（兩處：script src 的 `?id=` 與 `gtag('config', ...)`）
   - 全站替換指令參考：`grep -rl "G-XXXXXXXXXX" --include="*.html" .`

2. **詢價表單是假的**：`contact.html` 的表單目前送出後資料不去任何地方（`script.js` 的 `bindContactForm` 只 console.log + alert）。這是目前最大的功能缺口——訪客以為送出了，實際上業主收不到。
   - 已與業主討論的方案（見第 9 節）

### 🟡 P1 — 近期規劃（已與業主討論，尚未實作）

3. **表單後端 + 訊息串接**：業主想要詢價單能真的送達，並希望與 LINE/FB/IG 串接。討論結論：
   - **最速解（零後端）**：表單送出改為組好文字 + 開啟 LINE OA（`https://line.me/R/ti/p/@643qzkfp`），客人直接在 LINE 傳給業主。無金鑰、無資料庫。
   - **正規解（無伺服器）**：Cloudflare Pages Functions + D1 資料庫，表單→驗證→存DB→用 LINE Messaging API 推播。Channel Token 放 Cloudflare 環境變數（絕不進 repo）。安全需求：輸入驗證、單一網域 CORS、頻率限制防灌水。
   - **第三方客服**：業主考慮嵌 tawk.to（免費 live chat widget）。若走這條，等業主給 widget embed code（形如 `https://embed.tawk.to/{id}/default`），嵌入全站 46 頁，並處理與現有 LINE 浮動鈕的位置衝突（都在右下角）。widget ID 是公開安全的。
   - ⚠️ 事實查核結論：FB Messenger 網頁聊天外掛已於 2024/5 停用、LINE Notify 已於 2025/3 終止、LINE 無官方網頁 widget。所以「網站直接嵌 FB/LINE 聊天」官方已不支援，只能用連結按鈕或第三方彙整工具。

4. **FB / IG 連結按鈕**：footer 已有 LINE/FB/Google 社群列，可再補 Messenger（`m.me/{粉專}`）與 IG（`ig.me/{帳號}`）連結。需業主提供 FB 粉專 username 與 IG 帳號。

### 🟢 P2 — 資料待補

5. **營業時間**：LocalBusiness JSON-LD 尚未填 `openingHours`，等業主提供。
6. **Meta Pixel**：若業主要投 FB/IG 廣告，需全站埋 Pixel（同 GA4 做法）。業主未定。
7. **產品實景照**：24 產品中僅 5 個有實景照，其餘用 CSS 圖形。業主手上有照片素材（原始 RAR），可陸續補齊。
8. **更多案例照片**：每案目前存 3 張、顯示 1 張封面。若要做圖片畫廊/lightbox，素材已在 `images/cases/*/`。

### 待業主確認的內容問題
- faq.html 的 CNS 技術數字（垂墜 20-25%、外延 2.5/3/4m、網線 265.3/132.7kgf 等）建議請業主的勞安人員對照標準原文複核。

---

## 9. 業主聯絡資訊與品牌資產（寫入頁面用）

```
公司全名：安隆安全網有限公司
英文：ANLONG SAFETY（工程）/ ANLONG HOME（居家）
統一編號：50932767
成立：2018-09-28
地址：高雄市大寮區上寮里至學路571巷65之2號（郵遞區號 831）
電話：07-7828005
手機：0925-595-175
傳真：07-7817605
Email：a710120a710120@yahoo.com.tw
LINE 官方帳號：@643qzkfp
  連結：https://line.me/R/ti/p/@643qzkfp
Facebook：https://www.facebook.com/100057658561456
Google 商家：https://share.google/28OpbPN2jbK9vJzaU

服務範圍：高雄、台中、新竹、桃園駐點，全台皆可服務
自有施工班（非外包），人員具國家職業安全衛生證照
保固：室外 1 年、室內 2 年（非人為與天災）
投保：5000 萬元產品責任險
免費到府丈量（需 7 天前預約）

品牌色：
  主色 primary：#0f2c4a（深藍，兩品牌共用）
  工程 accent：#4a8c8c（青）
  居家 accent：#e87722（橘）

Search Console 驗證碼：n2u56H6tGekvNenjobW76FdALH_lMMqFdFpkvfZbAXA
GA4：尚未申請（佔位符 G-XXXXXXXXXX）
```

---

## 10. 本機測試

```bash
cd web            # 進到網站根目錄
python -m http.server 8000
# 瀏覽器開 http://localhost:8000
```

⚠️ **不要直接雙擊 HTML 用 `file://` 開**——品牌切換的 localStorage、字型、部分資源在 file:// 下會失效。務必用 HTTP server。

---

## 11. 已知地雷清單（踩過的坑，別再踩）

1. **`file://` 開啟會壞**：圖片、CSS、JS 看似連不上，其實是開啟方式錯。用 HTTP server。
2. **GitHub Pages 子目錄**：網站在 `/web/` 下，相對路徑是命脈，別改成根目錄絕對路徑。圖片若在 GitHub 上連不上，先確認是否真的 push 上去了（曾懷疑 .webp 沒進 commit）。
3. **品牌 class 的 display 覆寫**：`.brand-show-*` 只能隱藏不匹配的，別強設 display 值（會壞 grid/flex）。
4. **重跑 generate-*.py 會蓋掉手動修改**：現在別重跑。
5. **巢狀 `<a>`**：曾在 cases.html 把案例卡包連結時造成 `<a>` 巢狀導致部分卡片點不了。整卡連結用單層 `<a class="case-card-link">` 包住 `<article>`，不要在裡面再放 `<a>`。
6. **CSS 選擇器打架**：曾有兩組 `.breadcrumb` 樣式衝突（產品頁的米色橫條 vs 案例頁 hero 內的）。現在案例/文章頁的麵包屑用 `.page-hero .breadcrumb` 限定範圍。改樣式時注意選擇器範圍。
7. **FAQPage JSON-LD 要與畫面同步**：faq.html 和 blog 文章的 FAQ，改問答時 `<details>` 畫面內容與 `<script type="application/ld+json">` 的 FAQPage 必須同步改，兩邊文字要一致。
8. **產品線措辭**：安隆**只有隱形鐵窗是金屬製**（316 不鏽鋼鋼索），其他都是網類（尼龍/特多龍/PE）。內容中不要出現「鋼索/鋼繩/母索」等描述其他產品（隱形鐵窗除外）。

---

## 12. 建議的下一步（若接手做 P1）

以業主規模與技術程度，建議優先級：
1. 先做「表單→開啟 LINE」的零後端改造（1 小時內，立即讓表單有用）
2. 補 FB/IG 連結按鈕（等業主給帳號）
3. 若要真後端，用 Cloudflare Pages + D1（免費、免維護主機、金鑰安全），不要租傳統 VPS
4. tawk.to 這類第三方 widget 是「網站聊天」最省事解，但 FB/IG/LINE 仍需各自 App 收訊，非真正全通路。真全通路（Chatwoot 自架）維護門檻對業主過高，不建議現階段做。
