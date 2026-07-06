# 📷 怎麼把你的照片加到網站上

這份說明告訴你：圖片該放哪、檔案要怎麼命名、HTML 該怎麼改。

---

## 第一步：圖片放在 `images/` 資料夾

我已經幫你建好 5 個子資料夾：

```
images/
├── logo/         ← 公司商標（橫式 logo 圖檔）
├── hero/         ← 首頁背景大圖
├── products/
│   ├── safety/   ← 工程級 12 項產品照片
│   └── home/     ← 居家用 12 項產品照片
└── cases/        ← 施工案例照片
```

---

## 第二步：圖片規格建議（很重要！）

| 用途 | 寬度 | 格式 | 檔案大小目標 |
|------|------|------|------------|
| 公司 Logo | 400px | `.png` 或 `.svg`（需透明背景） | 50KB 以下 |
| 首頁背景 | 1920px | `.jpg` | 200KB 以下 |
| 產品照片 | 800px | `.jpg` | 100KB 以下 |
| 案例照片 | 1200px | `.jpg` | 150KB 以下 |

**為什麼要壓縮？** 圖太大網頁會慢、Google 排名會降。免費壓縮工具：

- 🔗 [TinyPNG](https://tinypng.com)：直接拖照片進去壓縮（PNG / JPG）
- 🔗 [Squoosh](https://squoosh.app)：Google 出的，更專業
- 在 Mac 上可以用「預覽程式」 → 工具 → 調整大小，把寬度改 1200 即可

---

## 第三步：檔案命名規則 ⚠️ 一定要照這樣

**全部小寫，用「-」連字號，不要中文、不要空格、不要括號。**

### Logo
```
images/logo/anlong-logo.png
```

### 產品照片（檔名要對應產品的 slug）
```
images/products/safety/construction-safety-net.jpg  ← 工地防墜網
images/products/safety/sports-court-net.jpg         ← 球類攔截網
images/products/safety/solar-panel-net.jpg          ← 太陽能板防護網
... 等 12 個

images/products/home/stairs-safety-net.jpg          ← 樓梯防墜網
images/products/home/invisible-grilles.jpg          ← 隱形鐵窗
images/products/home/colorful-safety-net.jpg        ← 創意彩色網
... 等 12 個
```

(完整檔名清單在本檔最下方)

### 案例照片
```
images/cases/01-kaohsiung-arena.jpg     ← 高雄小巨蛋
images/cases/02-taipower.jpg            ← 台電
images/cases/03-edaworld.jpg            ← 義大
... 隨意命名沒關係，但要記得自己取的名字
```

---

## 第四步：在網頁裡顯示圖片（HTML 程式碼）

### 範例 A：把產品卡的圖示換成真實照片

用 VS Code 或記事本打開 `products.html`，找到類似這段：

```html
<a href="products/safety/construction-safety-net.html" class="product-card">
  <div class="product-visual">
    <div class="product-icon" data-icon="construction"></div>
    <span class="product-tag">工程營建</span>
  </div>
  ...
```

**改成這樣**（加入 `<img>` 標籤）：

```html
<a href="products/safety/construction-safety-net.html" class="product-card">
  <div class="product-visual">
    <img src="images/products/safety/construction-safety-net.jpg"
         alt="工地防墜網"
         style="width:100%; height:200px; object-fit:cover;">
    <span class="product-tag">工程營建</span>
  </div>
  ...
```

**關鍵就是這一行：**
```html
<img src="圖片路徑" alt="圖片說明" style="width:100%; height:200px; object-fit:cover;">
```

`object-fit: cover` 會自動裁切圖片填滿框，不會變形。

---

### 範例 B：把公司 Logo 放進去（取代目前的盾牌圖示）

在每個 HTML 檔案的最上方找到這段：

```html
<a href="index.html" class="logo">
  <span class="logo-icon">
    <svg ...><path d="M12 22s8-4 8-10..."/></svg>
  </span>
  <span class="logo-text">...</span>
</a>
```

**把整個 `<svg>...</svg>` 換成：**

```html
<img src="images/logo/anlong-logo.png" alt="安隆安全網" style="height:40px;">
```

⚠️ Logo 要更新的話，每個頁面都要改一次（30 個 HTML 檔）。建議用 VS Code 的「全專案搜尋取代」功能（`Ctrl+Shift+H`）一次改完。

---

### 範例 C：在案例卡片加上照片

`cases.html` 裡找到任一個案例卡：

```html
<article class="case-card">
  <div class="case-meta">CASE / 01 · 2024</div>
  <h3>高雄小巨蛋</h3>
  <p>球類攔截網</p>
  ...
</article>
```

**在 `<div class="case-meta">` 上方加入：**

```html
<article class="case-card">
  <img src="images/cases/01-kaohsiung-arena.jpg"
       alt="高雄小巨蛋施工案例"
       style="width:100%; height:240px; object-fit:cover; border-radius:0.75rem; margin-bottom:1rem;">
  <div class="case-meta">CASE / 01 · 2024</div>
  ...
```

---

## 完整檔名對照表（產品照片）

把照片改成這些檔名再放進去：

### 工程級（`images/products/safety/`）
| 檔名 | 對應產品 |
|------|---------|
| `construction-safety-net.jpg` | 工地防墜網 |
| `building-atrium-net.jpg` | 大樓天井安全網 |
| `sports-court-net.jpg` | 室內球類攔截網 |
| `outdoor-court-net.jpg` | 戶外球場攔截網 |
| `factory-safety-net.jpg` | 工廠安全防護網 |
| `solar-panel-net.jpg` | 太陽能板防護網 |
| `bird-prevention-net.jpg` | 農業防鳥網 |
| `shade-net.jpg` | 遮光網 |
| `playground-net.jpg` | 遊樂設施防護網 |
| `climbing-net.jpg` | 攀爬訓練網 |
| `tile-protection-net.jpg` | 屋瓦防護網 |
| `barrier-net.jpg` | 工地圍籬網 |

### 居家用（`images/products/home/`）
| 檔名 | 對應產品 |
|------|---------|
| `stairs-safety-net.jpg` | 樓梯防墜網 |
| `l-shape-stairs-net.jpg` | L 型樓梯網 |
| `triangle-stairs-net.jpg` | 三角樓梯網 |
| `square-stairs-net.jpg` | 方型樓梯網 |
| `invisible-grilles.jpg` | 隱形鐵窗 |
| `window-safety-net.jpg` | 窗戶防墜網 |
| `balcony-safety-net.jpg` | 頂樓陽台防墜網 |
| `colorful-safety-net.jpg` | 創意彩色安全網 |
| `handrail-net.jpg` | 手扶梯欄桿網 |
| `escalator-net.jpg` | 電扶梯安全網 |
| `pool-safety-net.jpg` | 水池安全防護網 |
| `bumper-strip.jpg` | 防撞條 |

---

## 不想自己改 HTML？

如果你不想改 HTML，告訴我你準備好哪些照片（壓縮過、命名好），我可以**直接幫你把網站全部改好，加好所有 `<img>` 標籤**。你只要把照片放進對應的資料夾就行。

如果完全沒有現成照片，也可以暫時不加 — 目前的 SVG 圖示也很乾淨，等之後拍好再加都來得及。
