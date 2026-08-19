/* ============================================
   ANLONG SAFETY NET - JAVASCRIPT
   架構：前後端分離友善設計
   - 所有資料操作集中在頂層，方便未來改為 fetch API
   - DOM 操作與資料邏輯分離
   ============================================ */

(function () {
  "use strict";

  /* ============================================
     1. 全域狀態
     ============================================ */
  const state = {
    currentBrand: "safety", // 'safety' | 'home'
    currentCategory: "all",
  };

  // 從 localStorage 載入品牌偏好（跨頁面記住）
  try {
    const saved = localStorage.getItem("anlong-brand");
    if (saved === "safety" || saved === "home") {
      state.currentBrand = saved;
      document.body.setAttribute("data-brand", saved);
    }
  } catch (e) {
    // localStorage 可能因隱私模式關閉，忽略
  }

  /* ============================================
     2. 產品資料（未來可改為 fetch('/api/products')）
     ============================================ */
  // 產品詳細資料（給 Modal 用），key = data-product-id
  // 這部份可以未來改成：
  //   const products = await fetch('/api/products').then(r => r.json());
  const productData = {
    // 安隆安全
    s1: { name: "工地防墜安全網", desc: "符合勞安規範，攔截高度≤7M，全方位工地防護。採用高張力特多龍材質，可承受 100kg 以上衝擊負載。", tag: "勞安規範" },
    s2: { name: "大樓天井防墜網", desc: "依規定 7 米高度安裝一件，承載式設計，垂墜量 20-25%。可選鋼索加強版本，適用各式天井結構。", tag: "專業安裝" },
    s3: { name: "球場運動攔截網", desc: "棒球、網球、羽球場專用，活動式可收納設計。網目尺寸依運動類型客製，附設專用滑軌。", tag: "可訂製" },
    s4: { name: "風雨球場防護網", desc: "高耐候特多龍材質，抗 UV 防潑水，戶外保固一年。可承受 12 級強風，適合台灣海島型氣候。", tag: "戶外耐候" },
    s5: { name: "太陽能板防護網", desc: "防止鳥類築巢、異物掉落，保護光電系統。不影響光電效能，可大幅延長太陽能板壽命。", tag: "防鳥防墜" },
    s6: { name: "公司廠區安全網", desc: "物架安全網、倉儲防護網，工業級線徑訂製。可依倉儲規範裝設防墜層、防落物層。", tag: "工業級" },
    s7: { name: "農業防鳥網", desc: "果園、雞舍、農場專用，多種網目尺寸選擇。可阻擋麻雀、白鷺鷥等常見害鳥，不傷害鳥類。", tag: "農用" },
    s8: { name: "遮光網（固定/活動式）", desc: "針織 50-80%、平織 50-95% 遮光率，多種規格。安裝後室內可降溫約 2 度，節能省電。", tag: "降溫節能" },
    s9: { name: "兒童遊戲場防護網", desc: "幼兒園、公園遊樂設施專用，符合兒童安全標準。色彩鮮豔、邊角圓滑、無毒材質。", tag: "兒童安全" },
    s10: { name: "隔離阻擋用安全網", desc: "人車分流、區域隔離、活動分區用網。可快速架設、收納，活動式設計適合短期工程。", tag: "分區隔離" },
    s11: { name: "人類攀爬網", desc: "兒童遊樂場攀爬網，正方形網目設計。承載多人同時攀爬，繩結結構安全經過認證。", tag: "遊樂設施" },
    s12: { name: "防磁磚掉落網", desc: "老舊大樓外牆磁磚防護，保護行人安全。透明或細網目設計，不影響大樓外觀。", tag: "外牆防護" },
    s13: { name: "植物攀爬網", desc: "牆面、圍籬與棚架用植物攀爬網，依現場尺寸客製菱形網面，協助藤蔓植栽攀附與生長導引。", tag: "植栽綠化" },
    // 安隆居家
    h1: { name: "樓梯防墜安全網", desc: "透天樓梯標配，5mm 線徑 10×10cm 網目，國家標準。可選擇 11 種顏色搭配居家風格。", tag: "熱銷款" },
    h2: { name: "L 型樓梯安全網", desc: "依樓梯形狀客製，多色可選，安裝整潔美觀。轉角處特殊處理，線條俐落。", tag: "客製化" },
    h3: { name: "口字型樓梯安全網", desc: "中央天井包覆式設計，全周防護無死角。適合中庭式透天厝、別墅。", tag: "全周防護" },
    h4: { name: "三角型樓梯安全網", desc: "特殊樓梯結構訂製，精準貼合不留縫隙。提供現場測量服務，誤差 ≤ 1cm。", tag: "訂製款" },
    h5: { name: "隱形鐵窗", desc: "2mm 白鐵鋼索包 PVC，防鳥 2.5cm／防人 5cm 間隔。不影響採光、視野與外觀，社區規約友善。", tag: "不影響採光" },
    h6: { name: "窗戶防墜網", desc: "兒童墜落防護，安裝快速不破壞窗框。可拆卸式設計，搬家時可帶走。", tag: "兒童防墜" },
    h7: { name: "頂樓陽台防墜網", desc: "陽台、頂樓加強防護，貓咪友善不外逃。專為毛孩家庭設計，網目密度防止頭部卡住。", tag: "貓奴必備" },
    h8: { name: "創意彩色安全網", desc: "白／黑／藍／紫／咖／綠／紅／橘／黃多色搭配。可拼接漸層、條紋等創意圖案。", tag: "繽紛時尚" },
    h9: { name: "手扶梯欄桿網", desc: "4mm 線徑 7×7cm 網目，符合大樓最新管理規定。每支欄桿上下打結，單線斷不全散。", tag: "社區規範" },
    h10: { name: "電扶梯安全網", desc: "商場、車站電扶梯側邊防護。專用安裝結構，不干擾電扶梯運作。", tag: "公共空間" },
    h11: { name: "水池安全防護網", desc: "景觀池、魚池防墜，兒童寵物雙重保障。可承重式設計，承載成人重量。", tag: "水池防護" },
    h12: { name: "防撞條", desc: "牆角、柱子防撞，居家安全細節。多種顏色、軟硬度可選，自黏式安裝。", tag: "居家防護" },
  };

  /* ============================================
     3. DOM 工具
     ============================================ */
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) =>
    Array.from(parent.querySelectorAll(selector));

  /* ============================================
     4. 品牌切換
     ============================================ */
  function setBrand(brand) {
    if (brand !== "safety" && brand !== "home") return;

    state.currentBrand = brand;
    state.currentCategory = "all";

    // 切換 body 屬性，CSS 會自動套用對應主題色
    document.body.setAttribute("data-brand", brand);

    // 儲存到 localStorage，跨頁面記住偏好
    try {
      localStorage.setItem("anlong-brand", brand);
    } catch (e) {
      // 忽略
    }

    // 更新按鈕狀態（所有頁面的 .brand-btn）
    $$(".brand-btn, .seg-btn").forEach((btn) => {
      const isActive = btn.dataset.brand === brand;
      btn.classList.toggle("active", isActive);
      btn.setAttribute("aria-selected", isActive ? "true" : "false");
    });

    // 重置分類篩選
    $$(".cat-btn").forEach((btn) => {
      const isActive = btn.dataset.category === "all";
      btn.classList.toggle("active", isActive);
    });

    // 顯示所有產品
    $$(".product-card").forEach((card) => card.classList.remove("hidden"));
  }

  function bindBrandSwitcher() {
    // 同步初始狀態（從 localStorage 載入後，更新按鈕 active 狀態）
    $$(".brand-btn, .seg-btn").forEach((btn) => {
      const isActive = btn.dataset.brand === state.currentBrand;
      btn.classList.toggle("active", isActive);
      btn.setAttribute("aria-selected", isActive ? "true" : "false");
    });

    $$(".brand-btn, .seg-btn").forEach((btn) => {
      btn.addEventListener("click", () => setBrand(btn.dataset.brand));
    });

    // Footer 內的品牌切換連結
    $$("[data-switch-to]").forEach((link) => {
      link.addEventListener("click", () => {
        const targetBrand = link.dataset.switchTo;
        if (targetBrand !== state.currentBrand) {
          setBrand(targetBrand);
        }
      });
    });
  }

  /* ============================================
     5. 分類篩選
     ============================================ */
  function filterByCategory(category) {
    state.currentCategory = category;

    // 找到目前品牌的產品網格
    const grid = $(`.products-grid[data-brand-content="${state.currentBrand}"]`);
    if (!grid) return;

    // 篩選顯示
    $$(".product-card", grid).forEach((card) => {
      const matches = category === "all" || card.dataset.category === category;
      card.classList.toggle("hidden", !matches);
    });
  }

  function bindCategoryFilter() {
    $$(".cat-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const brand = btn.dataset.catBrand;
        if (brand !== state.currentBrand) return;

        // 同品牌內的按鈕切換 active
        $$(`.cat-btn[data-cat-brand="${brand}"]`).forEach((b) =>
          b.classList.toggle("active", b === btn)
        );

        filterByCategory(btn.dataset.category);
      });
    });
  }

  /* ============================================
     6. 行動版選單
     ============================================ */
  function bindMobileMenu() {
    const toggle = $("#mobileToggle");
    const menu = $("#navMobile");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", () => {
      const isOpen = menu.classList.toggle("open");
      toggle.classList.toggle("active", isOpen);
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    // 點擊連結後自動關閉
    $$("a", menu).forEach((link) => {
      link.addEventListener("click", () => {
        menu.classList.remove("open");
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ============================================
     7. 已棄用：產品 Modal
     ============================================
     舊版會點擊卡片彈出 Modal；現在改為直接連到
     /products/[brand]/[slug].html 詳細頁面（利於 SEO 與長尾關鍵字）。
     如未來想恢復 Modal 預覽，將 bindProductModal 加回 init() 即可。
  */

  /* ============================================
     8. 表單提交
     ============================================ */
  function bindContactForm() {
    const form = $("#contactForm");
    if (!form) return;

    const status = $("#formStatus", form);
    const lineAccountId = "%40643qzkfp";

    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const data = {
        name: form.name.value.trim(),
        phone: form.phone.value.trim(),
        region: form.region.value,
        message: form.message.value.trim(),
      };

      if (!data.name || !data.phone) {
        if (status) status.textContent = "請填寫姓名與聯絡電話。";
        const firstInvalid = !data.name ? form.name : form.phone;
        firstInvalid.focus();
        return;
      }

      const message = [
        "您好，我想詢問安全網安裝：",
        `姓名：${data.name}`,
        `電話：${data.phone}`,
        `區域：${data.region || "未填寫"}`,
        `需求：${data.message || "希望由專人聯絡說明"}`,
        `來源頁面：${window.location.href}`,
      ].join("\n");

      if (status) status.textContent = "正在開啟 LINE，訊息帶入後請確認並按下送出。";
      if (typeof window.gtag === "function") {
        window.gtag("event", "generate_lead", { method: "LINE inquiry form" });
      }
      window.location.assign(
        `https://line.me/R/oaMessage/${lineAccountId}/?${encodeURIComponent(message)}`
      );
    });
  }

  /* ============================================
     9. 平滑捲動 + Header 偏移修正
     ============================================ */
  function bindSmoothScroll() {
    $$('a[href^="#"]').forEach((link) => {
      link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (href === "#" || href.length < 2) return;

        const target = $(href);
        if (target) {
          e.preventDefault();
          const offset = 80; // header 高度
          const top =
            target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: "smooth" });
        }
      });
    });
  }

  /* ============================================
     10. 輕量站內搜尋
     ============================================ */
  function bindSiteSearch() {
    const headerInner = $(".header-inner");
    const mobileToggle = $("#mobileToggle", headerInner || document);
    if (!headerInner || !mobileToggle || $("#siteSearchTrigger")) return;

    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "site-search-trigger";
    trigger.id = "siteSearchTrigger";
    trigger.setAttribute("aria-label", "開啟站內搜尋");
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.setAttribute("aria-controls", "siteSearch");
    trigger.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.65" y2="16.65"></line></svg><span>搜尋</span>';
    headerInner.insertBefore(trigger, mobileToggle);

    const overlay = document.createElement("div");
    overlay.className = "site-search-overlay";
    overlay.id = "siteSearch";
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-labelledby", "siteSearchTitle");
    overlay.innerHTML = `
      <div class="site-search-panel">
        <div class="site-search-head">
          <div>
            <div class="site-search-eyebrow">SITE SEARCH</div>
            <h2 id="siteSearchTitle">快速搜尋</h2>
          </div>
          <button type="button" class="site-search-close" aria-label="關閉搜尋">×</button>
        </div>
        <label class="site-search-field">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.65" y2="16.65"></line></svg>
          <input type="search" id="siteSearchInput" placeholder="搜尋產品、案例、地區或問題…" autocomplete="off" />
        </label>
        <div class="site-search-popular" aria-label="熱門搜尋">
          <span>熱門：</span>
          <button type="button" data-query="樓梯安全網">樓梯安全網</button>
          <button type="button" data-query="防鳥網">防鳥網</button>
          <button type="button" data-query="高雄">高雄</button>
          <button type="button" data-query="球場">球場</button>
          <button type="button" data-query="保固">保固</button>
        </div>
        <p class="site-search-status" id="siteSearchStatus" aria-live="polite">輸入關鍵字即可搜尋全站內容。</p>
        <div class="site-search-results" id="siteSearchResults"></div>
      </div>`;
    document.body.appendChild(overlay);

    const input = $("#siteSearchInput", overlay);
    const results = $("#siteSearchResults", overlay);
    const status = $("#siteSearchStatus", overlay);
    const closeButton = $(".site-search-close", overlay);
    const index = Array.isArray(window.ANLONG_SEARCH_INDEX)
      ? window.ANLONG_SEARCH_INDEX
      : [];
    const root = new URL(window.ANLONG_SEARCH_ROOT || "./", window.location.href);
    let lastFocus = null;

    function normalize(value) {
      return String(value || "").normalize("NFKC").toLowerCase().replace(/\s+/g, "");
    }

    const prepared = index.map((item) => ({
      item,
      title: normalize(item.title),
      summary: normalize(item.summary),
      keywords: normalize(item.keywords),
      type: normalize(item.type),
    }));

    function findMatches(query) {
      const simplified = query.replace(
        /(請問|多久|多少|如何|怎麼|可以|是否|什麼|哪裡|哪個|為什麼|有沒有)/g,
        " "
      );
      const terms = simplified.trim().split(/\s+/).map(normalize).filter(Boolean);
      if (!terms.length) return [];
      return prepared
        .map((entry) => {
          const haystack = `${entry.title} ${entry.keywords} ${entry.summary} ${entry.type}`;
          if (!terms.every((term) => haystack.includes(term))) return null;
          let score = 0;
          terms.forEach((term) => {
            if (entry.title === term) score += 80;
            else if (entry.title.startsWith(term)) score += 45;
            else if (entry.title.includes(term)) score += 30;
            if (entry.keywords.includes(term)) score += 12;
            if (entry.summary.includes(term)) score += 4;
          });
          return { item: entry.item, score };
        })
        .filter(Boolean)
        .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title, "zh-Hant"));
    }

    function renderResults(query) {
      results.replaceChildren();
      const matches = findMatches(query);
      if (!query.trim()) {
        status.textContent = "輸入關鍵字即可搜尋全站內容。";
        return;
      }
      status.textContent = matches.length
        ? `找到 ${matches.length} 筆結果${matches.length > 12 ? "，顯示最相關的 12 筆" : ""}。`
        : "找不到符合的內容，請嘗試較短的關鍵字。";

      matches.slice(0, 12).forEach(({ item }) => {
        const link = document.createElement("a");
        link.className = "site-search-result";
        link.href = new URL(item.url, root).href;

        const top = document.createElement("span");
        top.className = "site-search-result-top";
        const title = document.createElement("strong");
        title.textContent = item.title;
        const type = document.createElement("span");
        type.className = "site-search-result-type";
        type.textContent = item.type;
        top.append(title, type);

        const summary = document.createElement("span");
        summary.className = "site-search-result-summary";
        summary.textContent = item.summary;
        link.append(top, summary);
        results.appendChild(link);
      });
    }

    function openSearch(initialQuery = "") {
      lastFocus = document.activeElement;
      overlay.hidden = false;
      document.body.classList.add("search-open");
      input.value = initialQuery;
      renderResults(initialQuery);
      window.requestAnimationFrame(() => input.focus());
    }

    function closeSearch() {
      overlay.hidden = true;
      document.body.classList.remove("search-open");
      if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
    }

    trigger.addEventListener("click", () => openSearch());
    closeButton.addEventListener("click", closeSearch);
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) closeSearch();
    });
    input.addEventListener("input", () => renderResults(input.value));
    $$("[data-query]", overlay).forEach((button) => {
      button.addEventListener("click", () => {
        input.value = button.dataset.query;
        renderResults(input.value);
        input.focus();
      });
    });
    document.addEventListener("keydown", (event) => {
      const tag = document.activeElement && document.activeElement.tagName;
      if (event.key === "Escape" && !overlay.hidden) closeSearch();
      if (
        event.key === "/" &&
        overlay.hidden &&
        tag !== "INPUT" &&
        tag !== "TEXTAREA" &&
        tag !== "SELECT"
      ) {
        event.preventDefault();
        openSearch();
      }
    });

    let anchoredFaq = null;
    try {
      anchoredFaq = window.location.hash
        ? document.querySelector(window.location.hash)
        : null;
    } catch (e) {
      anchoredFaq = null;
    }
    if (anchoredFaq && anchoredFaq.matches("details.faq-item")) anchoredFaq.open = true;
  }

  /* ============================================
     11. 啟動
     ============================================ */
  function init() {
    bindBrandSwitcher();
    bindCategoryFilter();
    bindMobileMenu();
    bindContactForm();
    bindSmoothScroll();
    bindSiteSearch();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

/* ============================================
   Hero 輪播 Banner
   ============================================ */
(function () {
  var carousel = document.querySelector(".hero-carousel");
  if (!carousel) return;

  var allSlides = Array.prototype.slice.call(carousel.querySelectorAll(".hero-slide"));
  var dotsWrap = carousel.querySelector(".hero-dots");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var timer = null;
  var idx = 0;
  var INTERVAL = 5500;

  function currentBrand() {
    return document.body.getAttribute("data-brand") === "home" ? "home" : "safety";
  }

  function activeSlides() {
    var brand = currentBrand();
    return allSlides.filter(function (s) { return s.getAttribute("data-brand") === brand; });
  }

  function render() {
    var slides = activeSlides();
    allSlides.forEach(function (s) { s.classList.remove("is-active"); });
    if (!slides.length) return;
    if (idx >= slides.length) idx = 0;
    slides[idx].classList.add("is-active");

    // 圓點
    dotsWrap.innerHTML = "";
    slides.forEach(function (_, i) {
      var b = document.createElement("button");
      b.className = "hero-dot" + (i === idx ? " is-active" : "");
      b.setAttribute("aria-label", "第 " + (i + 1) + " 張");
      b.addEventListener("click", function () {
        idx = i;
        render();
        restart();
      });
      dotsWrap.appendChild(b);
    });
  }

  function next() {
    idx = (idx + 1) % activeSlides().length;
    render();
  }

  function restart() {
    if (timer) clearInterval(timer);
    if (!reduceMotion && activeSlides().length > 1) {
      timer = setInterval(next, INTERVAL);
    }
  }

  // 滑鼠停留暫停
  carousel.addEventListener("mouseenter", function () { if (timer) clearInterval(timer); });
  carousel.addEventListener("mouseleave", restart);

  // 品牌切換時重置輪播
  new MutationObserver(function (muts) {
    muts.forEach(function (m) {
      if (m.attributeName === "data-brand") {
        idx = 0;
        render();
        restart();
      }
    });
  }).observe(document.body, { attributes: true });

  render();
  restart();
})();
