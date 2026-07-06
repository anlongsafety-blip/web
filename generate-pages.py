#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-pages.py — 主要頁面生成器（多頁版）
========================================
生成：index.html、products.html、cases.html、about.html、faq.html、contact.html

產品詳細頁仍由 generate-products.py 處理；上線後若資料有更新，
請依序執行：
    python3 generate-pages.py     # 主要頁面
    python3 generate-products.py  # 24 個產品頁 + sitemap
"""

import importlib.util
from pathlib import Path

# ============================================
# 配置
# ============================================
SITE_URL = "https://www.anlongsafety.com.tw"
GA4_ID = "G-XXXXXXXXXX"
SC_TOKEN = "n2u56H6tGekvNenjobW76FdALH_lMMqFdFpkvfZbAXA"
OUTPUT_DIR = Path(__file__).parent

# 從 generate-products.py 載入 PRODUCTS 資料（避免重複定義）
spec = importlib.util.spec_from_file_location("gp", OUTPUT_DIR / "generate-products.py")
gp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gp)
PRODUCTS = gp.PRODUCTS
BRAND_NAMES = {"safety": "安隆安全", "home": "安隆居家"}

# 導航定義
NAV = [
    ("index.html", "首頁", "home"),
    ("products.html", "產品型錄", "products"),
    ("cases.html", "施工案例", "cases"),
    ("about.html", "關於安隆", "about"),
    ("faq.html", "常見問題", "faq"),
    ("contact.html", "聯絡我們", "contact"),
]

# 案例資料
CASES = {
    "safety": [
        ("01", "2024", "高雄小巨蛋", "球類攔截網"),
        ("02", "2023", "台電發電廠", "廠區安全網"),
        ("03", "2023", "永安太陽能發電場", "太陽能防護網"),
        ("04", "2024", "田中棒球場", "運動攔截網"),
        ("05", "2023", "劍湖山世界", "遊樂設施防護網"),
        ("06", "2024", "義大遊樂世界", "公共安全網"),
        ("07", "2024", "南紡購物中心", "公共空間防護網"),
        ("08", "2023", "好事多賣場", "倉儲防護網"),
    ],
    "home": [
        ("01", "2024", "摩天鎮社區", "社區樓梯防墜網"),
        ("02", "2023", "小康幼兒園", "兒童安全防護網"),
        ("03", "2024", "高雄師範大學", "宿舍隱形鐵窗"),
        ("04", "2023", "德蘭幼兒園", "遊戲場防護網"),
        ("05", "2024", "梅山護理之家", "長輩樓梯防護"),
        ("06", "2023", "陽光飯店", "飯店天井安全網"),
        ("07", "2024", "聖功護專", "宿舍隱形鐵窗"),
        ("08", "2023", "建宏建設樣品屋", "創意彩色安全網"),
    ],
}

# FAQ 資料
FAQS = [
    ("Q01", "安全網有國家安裝規範嗎？", "有的。攔截高度於安全網架設平面至其上方不得超過 7 公尺；安裝完成後中心點垂墜量應介於 20%-25% 短邊長度；菱形網目任一邊長不得大於 10 公分。大樓樓梯縫隙不得超過 30 公分、手扶梯不得超過 10 公分。"),
    ("Q02", "安裝的費用如何計算？", "透天 2-4 樓樓梯防墜網約 8,000-13,000 元；遮光網安裝每坪約 1,500 元。實際價格依五金材料、現場環境、網子數量而定。歡迎來電告知您的情況，我們可以先大概報價。"),
    ("Q03", "網子的顏色有哪些選擇？", "我們提供白、黑、深藍、紫、深咖、水藍、綠、棕（淡咖）、紅、橘、黃共 11 種顏色，可任意搭配。白色為基本款一個價位，有顏色的為另一個價位（顏色越多越貴）。"),
    ("Q04", "北中南都可以服務嗎？", "本公司於高雄、台中、新竹、桃園均有駐點人員，絕非外包廠商。到場測量需事先預約（約 7 日內），施工日期則需確定後 7 日內安排。到場測量完全免費。"),
    ("Q05", "產品保固期多久？", "非人為因素及天然災害下損壞均享有：室外安裝保固 1 年、室內安裝保固 2 年。本公司投保 5,000 萬產品責任險，符合國家安全標準，給您最安心的保障。"),
    ("Q06", "我可以只買網子自行安裝嗎？", "可以。我們會在網子的四個邊穿線，四個角打結並留 1.5 米長度供您固定。請您自行測量尺寸給我們報價製作。自行購買網子的客戶恕不提供到府測量服務。"),
    ("Q07", "工程驗收會有什麼文件？", "我們會提供：1) 完工照片，2) 材質規格說明，3) 5,000 萬產品責任險證明影本，4) 國家職業安全衛生證照影本。如需更詳細的工程文件（如壓力測試報告），請於下單時告知。"),
    ("Q08", "可以開立統一發票或收據嗎？", "可以。本公司統一編號 50932767，可開立二聯式收據、三聯式發票（需公司抬頭與統編）。社區大樓、公司行號、學校等需報帳的單位，請於下單時告知開立資訊。"),
]


# ============================================
# 共用模板片段
# ============================================
def render_head(title, description, keywords, canonical_filename, jsonld_blocks=None):
    """生成完整的 <head>。canonical_filename 是 'index.html'/'products.html' 等"""
    canonical_url = f"{SITE_URL}/" if canonical_filename == "index.html" else f"{SITE_URL}/{canonical_filename}"
    extra_ld = ""
    if jsonld_blocks:
        for block in jsonld_blocks:
            extra_ld += f"""

  <script type="application/ld+json">
{block}
  </script>"""
    return f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="安隆安全網有限公司" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical_url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="zh_TW" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:site_name" content="安隆安全網有限公司" />

  <!-- Google Search Console -->
  <meta name="google-site-verification" content="{SC_TOKEN}" />

  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}', {{
      page_title: document.title,
      page_path: window.location.pathname
    }});
  </script>

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%234a8c8c'%3E%3Cpath d='M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z'/%3E%3C/svg%3E" />

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Noto+Serif+TC:wght@400;600;700;900&family=Cormorant+Garamond:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Stylesheet -->
  <link rel="stylesheet" href="styles.css" />{extra_ld}
</head>"""


def render_header(active_key):
    """渲染共用 header；active_key: home/products/cases/about/faq/contact"""
    desktop_items = []
    mobile_items = []
    for path, name, key in NAV:
        cls = ' class="active" aria-current="page"' if key == active_key else ""
        desktop_items.append(f'        <a href="{path}"{cls}>{name}</a>')
        mobile_items.append(f'      <a href="{path}"{cls}>{name}</a>')
    desktop_nav = "\n".join(desktop_items)
    mobile_nav = "\n".join(mobile_items)
    return f"""  <header class="header" id="header">
    <div class="container header-inner">
      <a href="index.html" class="logo" aria-label="安隆安全網有限公司首頁">
        <span class="logo-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </span>
        <span class="logo-text">
          <span class="logo-name">安隆</span>
          <span class="logo-en">ANLONG SAFETY</span>
        </span>
      </a>

      <nav class="nav-desktop" aria-label="主選單">
{desktop_nav}
      </nav>

      <a href="tel:07-7828005" class="header-cta">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
        </svg>
        07-7828005
      </a>

      <button class="mobile-toggle" id="mobileToggle" aria-label="開啟選單" aria-expanded="false">
        <svg class="icon-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <nav class="nav-mobile" id="navMobile" aria-label="行動選單">
{mobile_nav}
      <a href="tel:07-7828005" class="mobile-cta">立即來電 07-7828005</a>
    </nav>
  </header>"""


def render_footer():
    return f"""  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="logo footer-logo">
            <span class="logo-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </span>
            <span class="logo-text">
              <span class="logo-name">安隆安全網</span>
              <span class="logo-en">ANLONG SAFETY</span>
            </span>
          </div>
          <p class="footer-desc">專業安全網製作、批發、零售與安裝。守護每一個家、每一座工地的安全。</p>
        </div>

        <div>
          <h4>網站導覽</h4>
          <ul>
            <li><a href="products.html">產品型錄</a></li>
            <li><a href="cases.html">施工案例</a></li>
            <li><a href="about.html">關於安隆</a></li>
            <li><a href="faq.html">常見問題</a></li>
            <li><a href="contact.html">聯絡我們</a></li>
          </ul>
        </div>

        <div>
          <h4>聯絡資訊</h4>
          <ul>
            <li>電話：07-7828005</li>
            <li>手機：0925-595-175</li>
            <li>傳真：07-7817605</li>
            <li>LINE：@643qzkfp</li>
          </ul>
        </div>

        <div>
          <h4>總公司</h4>
          <p>高雄市大寮區上寮里至學路571巷65之2號</p>
          <p>週一至週五 08:00 - 17:00</p>
          <p class="footer-uni">統一編號：50932767</p>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2026 安隆安全網有限公司 All Rights Reserved.</p>
        <p class="footer-tag">SAFETY · QUALITY · TRUST</p>
      </div>
    </div>
  </footer>

  <a href="https://line.me/R/ti/p/@643qzkfp" class="line-float" target="_blank" rel="noopener noreferrer" aria-label="LINE 線上諮詢">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    <span>LINE 諮詢</span>
  </a>

  <script src="script.js" defer></script>"""


def render_breadcrumb_visible(items):
    """items: [(name, url_or_None), ...]"""
    parts = []
    for i, (name, url) in enumerate(items):
        if i > 0:
            parts.append('        <span class="separator">›</span>')
        if url:
            parts.append(f'        <a href="{url}">{name}</a>')
        else:
            parts.append(f'        <span class="current">{name}</span>')
    inner = "\n".join(parts)
    return f"""    <nav class="breadcrumb" aria-label="麵包屑">
      <div class="container">
{inner}
      </div>
    </nav>"""


def render_breadcrumb_jsonld(items):
    """items: [(name, full_url), ...]"""
    list_items = []
    for i, (name, url) in enumerate(items, 1):
        list_items.append(f"""        {{
          "@type": "ListItem",
          "position": {i},
          "name": "{name}",
          "item": "{url}"
        }}""")
    return f"""    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
{",".join(list_items)}
      ]
    }}"""


def render_page_hero(eyebrow, h1, description, brand_switcher=False):
    """頁面 hero（次級頁面用，較小）"""
    switcher_html = ""
    if brand_switcher:
        switcher_html = """
        <div class="brand-switcher" role="tablist" aria-label="品牌切換">
          <button class="brand-btn brand-btn-safety" data-brand="safety" role="tab" aria-selected="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span>安隆安全</span>
            <span class="brand-btn-en">SAFETY</span>
          </button>
          <button class="brand-btn brand-btn-home" data-brand="home" role="tab" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            <span>安隆居家</span>
            <span class="brand-btn-en">HOME</span>
          </button>
        </div>"""
    return f"""    <section class="page-hero">
      <div class="hero-bg-pattern" aria-hidden="true"></div>
      <div class="hero-glow hero-glow-1" aria-hidden="true"></div>
      <div class="hero-glow hero-glow-2" aria-hidden="true"></div>
      <div class="container">
        <div class="page-hero-inner">
          <div class="page-hero-eyebrow">{eyebrow}</div>
          <h1>{h1}</h1>
          <p>{description}</p>{switcher_html}
        </div>
      </div>
    </section>"""


def render_cta_section(title="免費現場估價", desc="到場測量完全免費，工程師約 7 日內可到府。歡迎來電、LINE 或填寫表單聯絡我們。"):
    return f"""    <section class="product-cta-section">
      <div class="hero-bg-pattern"></div>
      <div class="container">
        <h2>{title}</h2>
        <p>{desc}</p>
        <div class="cta-buttons">
          <a href="tel:07-7828005" class="btn btn-accent">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            07-7828005
          </a>
          <a href="contact.html" class="btn btn-outline">填寫詢價表單</a>
        </div>
      </div>
    </section>"""


def render_product_card(pid, p):
    """單一產品卡片（連結到產品詳細頁）"""
    return f"""          <a href="products/{p['brand']}/{p['slug']}.html" class="product-card" data-category="{p['category']}">
            <div class="product-visual">
              <div class="product-icon" data-icon="{p['icon']}"></div>
              <span class="product-tag">{p['tag']}</span>
            </div>
            <div class="product-body">
              <h3>{p['name']}</h3>
              <p>{p['summary'][:55]}...</p>
              <span class="product-link">查看詳情 →</span>
            </div>
          </a>"""


# ============================================
# 各頁面內容
# ============================================
def render_index():
    """首頁 — 多頁版 landing"""
    title = "安隆安全網有限公司｜防墜網、隱形鐵窗、樓梯安全網、球場攔截網專業安裝"
    description = "安隆安全網專營各式安全網。旗下兩大品牌：安隆安全（工程級）、安隆居家（住宅用）。北中南四大駐點，5,000 萬產品責任險，國家認證。"
    keywords = "安隆安全網,防墜網,隱形鐵窗,樓梯安全網,工地安全網,球類攔截網,高雄安全網,陽台防墜網"

    # 結構化資料
    ld_business = """    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "安隆安全網有限公司",
      "alternateName": "ANLONG SAFETY",
      "@id": "https://www.anlongsafety.com.tw/",
      "url": "https://www.anlongsafety.com.tw/",
      "telephone": "+886-7-7828005",
      "email": "a710120a710120@yahoo.com.tw",
      "priceRange": "$$",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "大寮區上寮里至學路571巷65之2號",
        "addressLocality": "高雄市",
        "addressRegion": "TW-KHH",
        "postalCode": "831",
        "addressCountry": "TW"
      },
      "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
        "opens": "08:00",
        "closes": "17:00"
      }],
      "areaServed": [
        {"@type":"City","name":"高雄市"},
        {"@type":"City","name":"台中市"},
        {"@type":"City","name":"新竹市"},
        {"@type":"City","name":"桃園市"}
      ]
    }"""
    ld_breadcrumb = render_breadcrumb_jsonld([("首頁", f"{SITE_URL}/")])
    ld_website = """    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "安隆安全網有限公司",
      "url": "https://www.anlongsafety.com.tw/",
      "inLanguage": "zh-Hant-TW"
    }"""

    # 精選產品（兩品牌各 3 個）
    featured_ids = ["s1", "s3", "s5", "h1", "h5", "h7"]
    featured_html = "\n".join(render_product_card(pid, PRODUCTS[pid]) for pid in featured_ids)

    # 精選案例（兩品牌各 3 個）
    sel_safety = CASES["safety"][:3]
    sel_home = CASES["home"][:3]

    body = f"""    <!-- ========== HERO ========== -->
    <section id="home" class="hero">
      <div class="hero-bg-pattern" aria-hidden="true"></div>
      <div class="hero-glow hero-glow-1" aria-hidden="true"></div>
      <div class="hero-glow hero-glow-2" aria-hidden="true"></div>

      <div class="container hero-inner">
        <div class="brand-switcher" role="tablist" aria-label="品牌切換">
          <button class="brand-btn brand-btn-safety active" data-brand="safety" role="tab" aria-selected="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span>安隆安全</span><span class="brand-btn-en">SAFETY</span>
          </button>
          <button class="brand-btn brand-btn-home" data-brand="home" role="tab" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            <span>安隆居家</span><span class="brand-btn-en">HOME</span>
          </button>
        </div>

        <div class="hero-content">
          <div class="hero-tag">EST. 在地深耕 · 全台駐點服務</div>
          <h1 class="hero-title">
            <span class="brand-show-safety">築起每一道<br /><span class="accent">專業安全防線</span></span>
            <span class="brand-show-home">守護家的每個<br /><span class="accent">溫柔角落</span></span>
          </h1>
          <p class="hero-subtitle">
            <span class="brand-show-safety">專業工程級防護網，符合勞安規範。從工地、廠房、球場到公共設施，安隆以二十年經驗，為您打造最堅實的安全屏障。</span>
            <span class="brand-show-home">從樓梯、陽台到窗戶，居家安全網守護每位家人。多彩客製、隱形美觀，讓防護成為居家的一部分。</span>
          </p>
          <div class="hero-actions">
            <a href="products.html" class="btn btn-accent">瀏覽產品型錄
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
            <a href="contact.html" class="btn btn-outline">免費現場估價</a>
          </div>
        </div>

        <div class="hero-stats">
          <div class="stat-item"><div class="stat-num">20+</div><div class="stat-label">年專業經驗</div></div>
          <div class="stat-item"><div class="stat-num">5000萬</div><div class="stat-label">產品責任險</div></div>
          <div class="stat-item"><div class="stat-num">100+</div><div class="stat-label">指標案場</div></div>
          <div class="stat-item"><div class="stat-num">4</div><div class="stat-label">全台駐點</div></div>
        </div>
      </div>
    </section>

    <!-- ========== 四大優勢 ========== -->
    <section class="features" aria-label="安隆四大優勢">
      <div class="container">
        <div class="features-grid">
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg></div><h3>國家認證</h3><p>職業安全衛生證照，產品符合國家安全標準</p></article>
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div><h3>專業保固</h3><p>室外保固 1 年、室內保固 2 年，安心無憂</p></article>
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div><h3>直營施工</h3><p>北中南駐點人員，絕非外包廠商</p></article>
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><h3>快速服務</h3><p>7 日內現場測量，免費估價不收費</p></article>
        </div>
      </div>
    </section>

    <!-- ========== 雙品牌展示 ========== -->
    <section class="brand-showcase">
      <div class="container">
        <div class="section-header-center">
          <div class="section-eyebrow">— OUR BRANDS</div>
          <h2 class="section-title">兩大品牌，全方位防護</h2>
          <p class="section-desc">依場景與需求，安隆提供兩個獨立品牌線</p>
        </div>
        <div class="brand-showcase-grid">
          <article class="brand-showcase-card safety">
            <div class="brand-showcase-eyebrow">ANLONG SAFETY</div>
            <h3>安隆安全 · 工程級</h3>
            <p>專業工地防墜網、球場攔截網、太陽能板防護網、廠區安全網。符合勞安規範，承載式設計。</p>
            <div class="brand-showcase-tags">
              <span class="brand-showcase-tag">工地防墜網</span>
              <span class="brand-showcase-tag">球場攔截網</span>
              <span class="brand-showcase-tag">廠區防護</span>
              <span class="brand-showcase-tag">太陽能板</span>
            </div>
            <a href="products.html" class="brand-showcase-link" data-switch-to="safety">查看工程產品 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
          </article>
          <article class="brand-showcase-card home">
            <div class="brand-showcase-eyebrow">ANLONG HOME</div>
            <h3>安隆居家 · 住宅用</h3>
            <p>樓梯防墜網、隱形鐵窗、陽台防護網、創意彩色網。多色客製，隱形美觀，貓奴友善。</p>
            <div class="brand-showcase-tags">
              <span class="brand-showcase-tag">樓梯防墜</span>
              <span class="brand-showcase-tag">隱形鐵窗</span>
              <span class="brand-showcase-tag">陽台防護</span>
              <span class="brand-showcase-tag">創意彩色</span>
            </div>
            <a href="products.html" class="brand-showcase-link" data-switch-to="home">查看居家產品 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
          </article>
        </div>
      </div>
    </section>

    <!-- ========== 精選產品 ========== -->
    <section class="products-section">
      <div class="container">
        <div class="section-header-link">
          <div>
            <div class="section-eyebrow">— FEATURED PRODUCTS</div>
            <h2 class="section-title">精選產品</h2>
          </div>
          <a href="products.html" class="section-view-all">查看全部 24 項產品
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
        <div class="products-grid">
{featured_html}
        </div>
      </div>
    </section>

    <!-- ========== 精選案例 ========== -->
    <section class="cases-section">
      <div class="container">
        <div class="section-header-link">
          <div>
            <div class="section-eyebrow">— SELECTED PROJECTS</div>
            <h2 class="section-title">指標案例</h2>
          </div>
          <a href="cases.html" class="section-view-all">查看全部案例
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
        <div class="cases-grid brand-show-safety">
""" + "\n".join(
        f'          <article class="case-card"><div class="case-meta">CASE / {n} · {y}</div><h3>{name}</h3><p>{t}</p><div class="case-footer"><span>已通過驗收</span></div></article>'
        for n, y, name, t in sel_safety
    ) + """
        </div>
        <div class="cases-grid brand-show-home">
""" + "\n".join(
        f'          <article class="case-card"><div class="case-meta">CASE / {n} · {y}</div><h3>{name}</h3><p>{t}</p><div class="case-footer"><span>已通過驗收</span></div></article>'
        for n, y, name, t in sel_home
    ) + """
        </div>
      </div>
    </section>

    <!-- ========== 關於簡介 ========== -->
    <section class="intro-section">
      <div class="container">
        <div class="intro-grid">
          <div class="intro-text">
            <div class="section-eyebrow">— ABOUT US</div>
            <h2 class="section-title">以「安全」為名<br />以「專業」為信</h2>
            <p>安隆專營各式安全防護網的批發、零售與訂製。從工程級到居家用，我們堅持依客戶需求訂製顏色與尺寸。</p>
            <p>北中南四大駐點，<strong style="color: var(--accent);">絕非外包廠商</strong>。所有人員具備國家職業安全衛生證照，投保 5,000 萬產品責任險。</p>
            <a href="about.html" class="section-view-all" style="margin-top: 1rem;">了解更多關於安隆
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
          </div>
          <div class="intro-stats">
            <div class="intro-stat"><div class="intro-stat-num">20+</div><div class="intro-stat-label">年專業經驗</div></div>
            <div class="intro-stat"><div class="intro-stat-num">100+</div><div class="intro-stat-label">指標案場</div></div>
            <div class="intro-stat"><div class="intro-stat-num">4</div><div class="intro-stat-label">全台駐點</div></div>
            <div class="intro-stat"><div class="intro-stat-num">11</div><div class="intro-stat-label">客製顏色</div></div>
          </div>
        </div>
      </div>
    </section>
""" + render_cta_section()

    head = render_head(title, description, keywords, "index.html",
                       jsonld_blocks=[ld_business, ld_website, ld_breadcrumb])
    return f"""{head}

<body data-brand="safety">
  <script>try{{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}}catch(e){{}}</script>

{render_header('home')}

  <main>
{body}
  </main>

{render_footer()}
</body>
</html>
"""


def render_products():
    """產品型錄頁"""
    title = "產品型錄｜安隆安全網有限公司 - 防墜網、隱形鐵窗、樓梯安全網一覽"
    description = "安隆兩大品牌共 24 項產品。安隆安全（工程級）：工地防墜、球場攔截、太陽能、廠區安全網。安隆居家（住宅用）：樓梯防墜、隱形鐵窗、陽台防護、創意彩色網。"
    keywords = "安全網,防墜網,隱形鐵窗,樓梯安全網,球場攔截網,工地安全網,陽台防墜網,農業防鳥網,遮光網,產品型錄"

    ld_breadcrumb = render_breadcrumb_jsonld([
        ("首頁", f"{SITE_URL}/"),
        ("產品型錄", f"{SITE_URL}/products.html"),
    ])

    # 渲染所有產品（按品牌分組）
    safety_products = "\n".join(
        render_product_card(pid, p) for pid, p in PRODUCTS.items() if p["brand"] == "safety"
    )
    home_products = "\n".join(
        render_product_card(pid, p) for pid, p in PRODUCTS.items() if p["brand"] == "home"
    )

    head = render_head(title, description, keywords, "products.html", jsonld_blocks=[ld_breadcrumb])

    page_hero = render_page_hero(
        "— PRODUCT CATALOG",
        "產品型錄",
        "從工程級到住宅用，24 項專業安全網一站找齊。點擊任一產品查看完整規格、應用場景與相關案例。",
        brand_switcher=True
    )

    breadcrumb = render_breadcrumb_visible([
        ("首頁", "index.html"),
        ("產品型錄", None),
    ])

    body = f"""{page_hero}

{breadcrumb}

    <section class="products-section" style="padding-top: 3rem;">
      <div class="container">
        <!-- 分類篩選 -->
        <div class="categories" style="margin-bottom: 2.5rem;">
          <div class="categories-group brand-show-safety">
            <button class="cat-btn active" data-category="all" data-cat-brand="safety">全部產品</button>
            <button class="cat-btn" data-category="construction" data-cat-brand="safety">工程營建</button>
            <button class="cat-btn" data-category="sports" data-cat-brand="safety">運動球場</button>
            <button class="cat-btn" data-category="industrial" data-cat-brand="safety">工業廠房</button>
            <button class="cat-btn" data-category="agriculture" data-cat-brand="safety">農業用網</button>
            <button class="cat-btn" data-category="public" data-cat-brand="safety">公共設施</button>
          </div>
          <div class="categories-group brand-show-home">
            <button class="cat-btn active" data-category="all" data-cat-brand="home">全部產品</button>
            <button class="cat-btn" data-category="stairs" data-cat-brand="home">樓梯防護</button>
            <button class="cat-btn" data-category="window" data-cat-brand="home">窗戶鐵窗</button>
            <button class="cat-btn" data-category="balcony" data-cat-brand="home">陽台頂樓</button>
            <button class="cat-btn" data-category="creative" data-cat-brand="home">創意客製</button>
          </div>
        </div>

        <!-- 安全產品 -->
        <div class="products-grid brand-show-safety" data-brand-content="safety">
{safety_products}
        </div>

        <!-- 居家產品 -->
        <div class="products-grid brand-show-home" data-brand-content="home">
{home_products}
        </div>
      </div>
    </section>

{render_cta_section()}"""

    return f"""{head}

<body data-brand="safety">
  <script>try{{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}}catch(e){{}}</script>

{render_header('products')}

  <main>
{body}
  </main>

{render_footer()}
</body>
</html>
"""


def render_cases():
    """施工案例頁"""
    title = "施工案例｜安隆安全網有限公司 - 學校、社區、商業空間實績"
    description = "安隆累積 100+ 件指標案場：高雄小巨蛋、台電發電廠、義大遊樂世界、劍湖山世界、高雄師範大學、好事多賣場等。國家認證、安全標準。"
    keywords = "安全網施工案例,高雄小巨蛋,台電工程,劍湖山,義大遊樂世界,高雄師範大學,安全網實績"

    ld_breadcrumb = render_breadcrumb_jsonld([
        ("首頁", f"{SITE_URL}/"),
        ("施工案例", f"{SITE_URL}/cases.html"),
    ])

    safety_cases = "\n".join(
        f'          <article class="case-card"><div class="case-meta">CASE / {n} · {y}</div><h3>{name}</h3><p>{t}</p><div class="case-footer"><span>已通過驗收</span></div></article>'
        for n, y, name, t in CASES["safety"]
    )
    home_cases = "\n".join(
        f'          <article class="case-card"><div class="case-meta">CASE / {n} · {y}</div><h3>{name}</h3><p>{t}</p><div class="case-footer"><span>已通過驗收</span></div></article>'
        for n, y, name, t in CASES["home"]
    )

    head = render_head(title, description, keywords, "cases.html", jsonld_blocks=[ld_breadcrumb])
    page_hero = render_page_hero(
        "— SELECTED PROJECTS",
        "施工案例",
        "從學校、公部門到商業空間，每一個指標案場都通過嚴格驗收，是安隆專業與品質的最佳證明。",
        brand_switcher=True
    )
    breadcrumb = render_breadcrumb_visible([
        ("首頁", "index.html"),
        ("施工案例", None),
    ])

    body = f"""{page_hero}

{breadcrumb}

    <section class="cases-section" style="padding-top: 3rem;">
      <div class="container">
        <div class="cases-grid brand-show-safety">
{safety_cases}
        </div>
        <div class="cases-grid brand-show-home">
{home_cases}
        </div>
      </div>
    </section>

{render_cta_section()}"""

    return f"""{head}

<body data-brand="safety">
  <script>try{{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}}catch(e){{}}</script>

{render_header('cases')}

  <main>
{body}
  </main>

{render_footer()}
</body>
</html>
"""


def render_about():
    """關於安隆頁"""
    title = "關於安隆｜安隆安全網有限公司 - 20 年專業經驗、5000 萬產品責任險"
    description = "安隆安全網有限公司專營各式安全防護網的批發、零售與訂製。20 年專業經驗、5,000 萬產品責任險、國家職業安全衛生證照、北中南四大駐點。"
    keywords = "安隆安全網,關於安隆,安全網公司,高雄安全網,直營施工,產品責任險,國家認證"

    ld_breadcrumb = render_breadcrumb_jsonld([
        ("首頁", f"{SITE_URL}/"),
        ("關於安隆", f"{SITE_URL}/about.html"),
    ])

    head = render_head(title, description, keywords, "about.html", jsonld_blocks=[ld_breadcrumb])
    page_hero = render_page_hero(
        "— ABOUT ANLONG",
        "關於安隆",
        "以「安全」為名，以「專業」為信。二十年累積，只為每一張網都成為值得信賴的守護。"
    )
    breadcrumb = render_breadcrumb_visible([
        ("首頁", "index.html"),
        ("關於安隆", None),
    ])

    body = f"""{page_hero}

{breadcrumb}

    <section class="about-section">
      <div class="about-bg-pattern" aria-hidden="true"></div>
      <div class="container about-inner">
        <div class="about-content">
          <div class="section-eyebrow-light">— OUR STORY</div>
          <h2 class="section-title-light">堅持原則<br />守護每個信任</h2>
          <div class="about-text">
            <p>安隆安全網有限公司專營各式安全防護網的批發、零售與訂製。從工程級的防墜網、球場攔截網，到居家樓梯、隱形鐵窗，我們堅持依客戶需求訂製顏色與尺寸。</p>
            <p>公司施工人員於高雄、台中、新竹、桃園均有駐點，<strong>絕非外包廠商</strong>，可以最快速度到府測量並解說。所有人員具備國家職業安全衛生證照，產品符合國家安全標準，並投保 5,000 萬產品責任險。</p>
            <p>我們相信：每一張網，都該成為一個家、一座工地、一個社區，最值得信賴的守護。</p>
          </div>
          <div class="about-tags">
            <div class="about-tag"><div class="about-tag-label">公司統編</div><div class="about-tag-value">50932767</div></div>
            <div class="about-tag"><div class="about-tag-label">產品責任險</div><div class="about-tag-value">5,000 萬</div></div>
          </div>
        </div>

        <aside class="coverage-card">
          <div class="section-eyebrow-light">SERVICE COVERAGE</div>
          <h3 class="coverage-title">全台四大駐點</h3>
          <ul class="coverage-list">
            <li class="coverage-item coverage-item-main">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <div><div class="coverage-city">高雄 <span class="coverage-badge">總公司</span></div><div class="coverage-addr">大寮區上寮里至學路571巷65之2號</div></div>
            </li>
            <li class="coverage-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><div><div class="coverage-city">台中</div><div class="coverage-addr">復興路三段</div></div></li>
            <li class="coverage-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><div><div class="coverage-city">新竹</div><div class="coverage-addr">中華路二段</div></div></li>
            <li class="coverage-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><div><div class="coverage-city">桃園</div><div class="coverage-addr">春日路</div></div></li>
          </ul>
        </aside>
      </div>
    </section>

    <section class="features">
      <div class="container">
        <div class="section-header-center">
          <div class="section-eyebrow">— OUR ADVANTAGES</div>
          <h2 class="section-title">為什麼選安隆</h2>
        </div>
        <div class="features-grid">
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg></div><h3>國家認證</h3><p>職業安全衛生證照，產品符合國家安全標準</p></article>
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div><h3>專業保固</h3><p>室外保固 1 年、室內保固 2 年，安心無憂</p></article>
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div><h3>直營施工</h3><p>北中南駐點人員，絕非外包廠商</p></article>
          <article class="feature-card"><div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><h3>快速服務</h3><p>7 日內現場測量，免費估價不收費</p></article>
        </div>
      </div>
    </section>

{render_cta_section()}"""

    return f"""{head}

<body data-brand="safety">
  <script>try{{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}}catch(e){{}}</script>

{render_header('about')}

  <main>
{body}
  </main>

{render_footer()}
</body>
</html>
"""


def render_faq():
    """FAQ 頁（含 FAQPage JSON-LD）"""
    title = "常見問題｜安隆安全網有限公司 - 安裝規範、費用、保固一次看懂"
    description = "安隆常見問題：安全網國家規範、安裝費用、顏色選擇、保固期、施工流程等 8 大問題完整解答。還有疑問歡迎來電 07-7828005 或 LINE。"
    keywords = "安全網問題,安裝費用,保固期,國家規範,安全網保固,安全網選色,自行安裝"

    ld_breadcrumb = render_breadcrumb_jsonld([
        ("首頁", f"{SITE_URL}/"),
        ("常見問題", f"{SITE_URL}/faq.html"),
    ])

    # FAQPage JSON-LD（Google 可顯示為精選摘要）
    faq_items = []
    for num, q, a in FAQS:
        # 處理 a 中的雙引號
        a_clean = a.replace('"', '\\"')
        q_clean = q.replace('"', '\\"')
        faq_items.append(f"""        {{
          "@type": "Question",
          "name": "{q_clean}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{a_clean}"
          }}
        }}""")
    ld_faqpage = f"""    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
{",".join(faq_items)}
      ]
    }}"""

    head = render_head(title, description, keywords, "faq.html",
                       jsonld_blocks=[ld_breadcrumb, ld_faqpage])
    page_hero = render_page_hero(
        "— FREQUENTLY ASKED",
        "常見問題",
        "還有疑問？以下整理了客戶最常詢問的 8 大問題。沒看到答案的話歡迎來電或加 LINE 詢問。"
    )
    breadcrumb = render_breadcrumb_visible([
        ("首頁", "index.html"),
        ("常見問題", None),
    ])

    faq_html = "\n".join(
        f'''          <details class="faq-item">
            <summary><span class="faq-num">{num}</span><span class="faq-q">{q}</span></summary>
            <div class="faq-a">{a}</div>
          </details>'''
        for num, q, a in FAQS
    )

    body = f"""{page_hero}

{breadcrumb}

    <section class="faq-section">
      <div class="container container-narrow">
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </section>

{render_cta_section()}"""

    return f"""{head}

<body data-brand="safety">
  <script>try{{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}}catch(e){{}}</script>

{render_header('faq')}

  <main>
{body}
  </main>

{render_footer()}
</body>
</html>
"""


def render_contact():
    """聯絡頁"""
    title = "聯絡我們｜安隆安全網有限公司 - 免費現場估價、北中南可服務"
    description = "電話 07-7828005、手機 0925-595-175、LINE @643qzkfp。高雄總公司、台中、新竹、桃園駐點服務。免費現場估價，7 日內可到府。"
    keywords = "安隆聯絡,免費估價,安全網詢價,高雄安全網,台中安全網,新竹安全網,桃園安全網"

    ld_breadcrumb = render_breadcrumb_jsonld([
        ("首頁", f"{SITE_URL}/"),
        ("聯絡我們", f"{SITE_URL}/contact.html"),
    ])

    head = render_head(title, description, keywords, "contact.html", jsonld_blocks=[ld_breadcrumb])
    page_hero = render_page_hero(
        "— GET IN TOUCH",
        "聯絡我們",
        "到場測量完全免費，工程師約 7 日內可到府。歡迎來電、LINE 或填寫表單，我們會盡快回覆。"
    )
    breadcrumb = render_breadcrumb_visible([
        ("首頁", "index.html"),
        ("聯絡我們", None),
    ])

    body = f"""{page_hero}

{breadcrumb}

    <section class="contact-section" style="padding-top: 3rem;">
      <div class="container">
        <div class="contact-card">
          <div class="contact-bg-pattern" aria-hidden="true"></div>
          <div class="contact-glow" aria-hidden="true"></div>

          <div class="contact-grid">
            <div class="contact-info">
              <div class="section-eyebrow-light">— CONTACT</div>
              <h2 class="section-title-light">三種方式<br />立即聯絡安隆</h2>
              <p class="contact-intro">最快回覆方式：來電或加 LINE。表單會在 1 個工作日內回覆。</p>

              <ul class="contact-list">
                <li><a href="tel:07-7828005"><div class="contact-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div><div><div class="contact-label">公司電話</div><div class="contact-value">07-7828005</div></div></a></li>
                <li><a href="tel:0925595175"><div class="contact-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div><div><div class="contact-label">手機 / LINE</div><div class="contact-value">0925-595-175</div><div class="contact-sub">LINE ID: @643qzkfp</div></div></a></li>
                <li><div class="contact-static"><div class="contact-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div><div><div class="contact-label">Email</div><div class="contact-value contact-email">a710120a710120@yahoo.com.tw</div></div></div></li>
              </ul>
            </div>

            <form class="contact-form" id="contactForm" novalidate>
              <h3>快速詢價表單</h3>
              <p>填寫您的需求，我們會在 1 個工作日內回覆</p>
              <div class="form-group"><label for="formName">姓名</label><input type="text" id="formName" name="name" placeholder="您的姓名" required /></div>
              <div class="form-row">
                <div class="form-group"><label for="formPhone">聯絡電話</label><input type="tel" id="formPhone" name="phone" placeholder="09xx-xxx-xxx" required /></div>
                <div class="form-group"><label for="formRegion">所在區域</label><select id="formRegion" name="region"><option>高雄</option><option>台中</option><option>新竹</option><option>桃園</option><option>其他</option></select></div>
              </div>
              <div class="form-group"><label for="formMessage">需求說明</label><textarea id="formMessage" name="message" rows="4" placeholder="請描述您的場地、想安裝的位置與尺寸..."></textarea></div>
              <button type="submit" class="form-submit">送出免費詢價</button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <section class="coverage-section">
      <div class="container">
        <div class="section-header-center">
          <div class="section-eyebrow">— SERVICE AREA</div>
          <h2 class="section-title">全台四大駐點</h2>
          <p class="section-desc">高雄、台中、新竹、桃園均有直營施工人員，絕非外包</p>
        </div>
        <div class="coverage-section-grid">
          <article class="coverage-section-card">
            <div class="pin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <h3>高雄<span class="badge-main">總公司</span></h3>
            <p class="addr">大寮區上寮里至學路<br />571 巷 65 之 2 號</p>
          </article>
          <article class="coverage-section-card">
            <div class="pin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <h3>台中</h3>
            <p class="addr">復興路三段</p>
          </article>
          <article class="coverage-section-card">
            <div class="pin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <h3>新竹</h3>
            <p class="addr">中華路二段</p>
          </article>
          <article class="coverage-section-card">
            <div class="pin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <h3>桃園</h3>
            <p class="addr">春日路</p>
          </article>
        </div>
      </div>
    </section>"""

    return f"""{head}

<body data-brand="safety">
  <script>try{{var b=localStorage.getItem('anlong-brand');if(b==='home'||b==='safety')document.body.setAttribute('data-brand',b);}}catch(e){{}}</script>

{render_header('contact')}

  <main>
{body}
  </main>

{render_footer()}
</body>
</html>
"""


def _ensure_svg_dimensions(html_text):
    """為沒有 width 屬性的 <svg> 加上 width/height（CSS 失效時的保險）"""
    import re
    return re.sub(r'<svg(?![^>]*\swidth=)', '<svg width="20" height="20"', html_text)


# ============================================
# 主執行
# ============================================
def main():
    pages = [
        ("index.html", render_index),
        ("products.html", render_products),
        ("cases.html", render_cases),
        ("about.html", render_about),
        ("faq.html", render_faq),
        ("contact.html", render_contact),
    ]
    for filename, fn in pages:
        out = OUTPUT_DIR / filename
        html = _ensure_svg_dimensions(fn())
        out.write_text(html, encoding="utf-8")
        print(f"  ✓ {filename}")
    print(f"\n✅ 共生成 {len(pages)} 個主要頁面")


if __name__ == "__main__":
    main()
