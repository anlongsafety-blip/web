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

    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const data = {
        name: form.name.value.trim(),
        phone: form.phone.value.trim(),
        region: form.region.value,
        message: form.message.value.trim(),
      };

      if (!data.name || !data.phone) {
        alert("請填寫姓名與聯絡電話");
        return;
      }

      // 未來可改為：
      //   await fetch('/api/inquiry', { method: 'POST', body: JSON.stringify(data) });
      console.log("提交詢價資料：", data);
      alert("感謝您的詢價！我們會在 1 個工作日內回覆。\n\n（此為示意表單，實際送出請串接後端 API）");

      form.reset();
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
     10. 啟動
     ============================================ */
  function init() {
    bindBrandSwitcher();
    bindCategoryFilter();
    bindMobileMenu();
    bindContactForm();
    bindSmoothScroll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
