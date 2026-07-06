#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
產品獨立頁面生成器
==================
此腳本會根據下方的 PRODUCTS 資料，為每個產品生成獨立 HTML 頁面。
未來如要新增/修改產品，編輯 PRODUCTS 後重新執行即可。

用法：
    python3 generate-products.py
"""

import os
import re
from pathlib import Path

# ============================================
# 共用設定
# ============================================
SITE_URL = "https://www.anlongsafety.com.tw"
GA4_ID = "G-XXXXXXXXXX"  # ← 替換為實際 GA4 測量 ID
OUTPUT_DIR = Path(__file__).parent  # 與本腳本同目錄
PRODUCTS_DIR = OUTPUT_DIR / "products"

BRAND_NAMES = {"safety": "安隆安全", "home": "安隆居家"}
BRAND_NAMES_EN = {"safety": "ANLONG SAFETY", "home": "ANLONG HOME"}

# 共用品牌規格（每個產品都套用）
COMMON_SPECS = {
    "保固期": "室外安裝 1 年，室內安裝 2 年（非人為因素及天然災害下損壞）",
    "服務區域": "高雄、台中、新竹、桃園駐點，全台可服務",
    "訂製選項": "顏色、尺寸、網目、線徑均可依需求調整",
    "材質": "尼龍（室內）／特多龍（戶外），抗 UV、防潑水",
    "顏色": "白、黑、深藍、紫、深咖、水藍、綠、棕（淡咖）、紅、橘、黃 共 11 色",
    "責任險": "投保 5,000 萬產品責任險",
    "認證": "公司施工人員具國家職業安全衛生證照，產品符合國家安全標準",
}

# ============================================
# 產品資料（24 項）
# ============================================
PRODUCTS = {
    # ============== 安隆安全 ==============
    "s1": {
        "brand": "safety", "slug": "construction-safety-net",
        "name": "工地防墜安全網", "tag": "勞安規範", "icon": "shield",
        "category": "construction", "category_name": "工程營建",
        "summary": "符合勞動部勞工安全衛生規範，攔截高度 ≤ 7 公尺。採用高張力特多龍材質，可承受 100kg 以上的衝擊負載，全方位工地防護首選。",
        "description": "工地防墜安全網是建築工程現場的法定基本配備。安隆採用高張力特多龍紗線編織，每網經過拉力測試，符合勞動部「營造安全衛生設施標準」第 18 條規範。網目為菱形 10×10 公分以下，可有效攔截作業人員與工具墜落。",
        "features": [
            "符合「營造安全衛生設施標準」第 18 條規定",
            "攔截高度 ≤ 7 公尺，可承受人員墜落衝擊",
            "高張力特多龍材質，斷裂強度 ≥ 23kN",
            "菱形網目，邊長 ≤ 10 公分",
            "中心點垂墜量 20%–25% 短邊長度，符合標準",
            "可承受 100kg 以上重物衝擊負載",
            "邊繩穿線、四角打結，現場快速架設",
        ],
        "specs": {
            "線徑": "5mm（標準）／可加粗訂製",
            "網目": "10×10 cm 菱形（國家標準）",
            "材質": "高張力特多龍（戶外）",
            "顏色": "白色為主，可訂製其他顏色",
            "尺寸": "依工區面積客製",
        },
        "use_cases": [
            ("大型營建工地", "高樓施工、外牆作業時的防墜攔截"),
            ("橋樑與隧道工程", "高架道路、橋樑下方防止物件墜落"),
            ("廠房整修", "工廠屋頂作業、設備維修期間防護"),
        ],
        "keywords": "工地安全網,工地防墜網,營造安全網,勞安規範,建築安全網,工地防護網,高雄工地安全網",
    },
    "s2": {
        "brand": "safety", "slug": "building-atrium-net",
        "name": "大樓天井防墜網", "tag": "專業安裝", "icon": "shield",
        "category": "construction", "category_name": "工程營建",
        "summary": "依規定 7 米高度安裝一件，承載式設計，垂墜量精準控制 20%–25%。專為大樓中庭、樓梯間天井設計，可選鋼索加強版本。",
        "description": "大樓天井防墜網是社區與商業大樓不可或缺的安全設施，可有效防止人員、物品墜落。依「建築技術規則」與大樓管理條例，天井應每 7 米安裝一片防墜網。安隆採用承載式設計，網體可承受成人衝擊。",
        "features": [
            "依規定 7 米高度安裝一件（約 2–3 層樓）",
            "承載式設計，垂墜量精準 20%–25%",
            "可選鋼索加強版本，固定點 75–85cm 一處",
            "適用各式天井：樓梯間、中庭、採光井",
            "逃生梯天井建議一層裝一件（轉角多）",
            "符合最新大樓管理規範",
            "施工人員國家證照，安裝過程不破壞建築結構",
        ],
        "specs": {
            "線徑": "5mm 起，依高度可加粗",
            "網目": "10×10 cm 菱形",
            "固定方式": "膨脹螺絲 / 不鏽鋼鋼索",
            "適用樓層": "2–30 層大樓均可施作",
            "尺寸": "依天井寬度客製",
        },
        "use_cases": [
            ("住宅大樓", "社區公共樓梯間、中庭天井防護"),
            ("辦公商業大樓", "辦公樓中央採光井、共用空間"),
            ("醫院長照機構", "病患安全考量的天井防護"),
        ],
        "keywords": "大樓天井防墜網,天井安全網,樓梯間防墜,社區安全網,中庭防墜網,大樓防墜",
    },
    "s3": {
        "brand": "safety", "slug": "sports-court-net",
        "name": "球場運動攔截網", "tag": "可訂製", "icon": "shield",
        "category": "sports", "category_name": "運動球場",
        "summary": "棒球、網球、羽球場專用，活動式可收納設計。網目尺寸依運動類型客製，附設專用滑軌系統，使用後可快速收起。",
        "description": "運動場攔截網是各類球場的必備設施，可防止球體飛出造成路人或鄰近設施損傷。安隆依不同運動項目調整網目大小：棒球用網較粗、網目較大；羽球與網球用網則需密目細線。",
        "features": [
            "依運動類型客製網目（棒球/網球/羽球/籃球）",
            "可選固定式或活動式（含滑軌系統）",
            "高張力特多龍，可承受球體高速衝擊",
            "戶外特殊塗層，抗 UV 不褪色",
            "高度可達 12 公尺以上（依場地）",
            "活動式可快速收納，比賽結束自動歸位",
            "支援自動電動收網系統（選配）",
        ],
        "specs": {
            "線徑": "3–6mm 依運動類型",
            "網目": "棒球 10cm、網球 4cm、羽球 2cm",
            "高度": "可達 12m 以上",
            "材質": "高耐候特多龍",
            "尺寸": "依球場規格客製",
        },
        "use_cases": [
            ("學校運動場", "棒球場、網球場、籃球場防球飛出"),
            ("社區球場", "屋頂、地下停車場改建球場"),
            ("專業訓練場", "棒球打擊練習場、網球練習場"),
        ],
        "keywords": "球場攔截網,棒球場用網,網球場用網,運動場安全網,球場防護網,風雨球場攔截網",
    },
    "s4": {
        "brand": "safety", "slug": "outdoor-court-net",
        "name": "風雨球場防護網", "tag": "戶外耐候", "icon": "shield",
        "category": "sports", "category_name": "運動球場",
        "summary": "高耐候特多龍材質，抗 UV 防潑水。可承受 12 級強風，適合台灣海島型氣候。戶外保固一年，校園與公園專用。",
        "description": "風雨球場通常為校園、社區共用空間，承受日曬雨淋與颱風考驗。安隆風雨球場專用網採用特殊塗層處理，UV 穩定劑添加，可承受台灣常見的鹽害、紫外線、強風環境。",
        "features": [
            "12 級強風抗風測試認證",
            "UV 穩定劑添加，戶外 5+ 年不脆化",
            "防潑水塗層，颱風後快乾",
            "鹽害測試合格，海濱地區可用",
            "顏色 5+ 年不明顯褪色",
            "可選防鳥網目（4cm 以下）",
            "戶外安裝保固 1 年",
        ],
        "specs": {
            "線徑": "4–6mm（戶外加強）",
            "網目": "依用途選擇 2–10cm",
            "材質": "抗 UV 特多龍 + 防潑水塗層",
            "風阻等級": "可承受 12 級強風",
            "保固": "戶外 1 年",
        },
        "use_cases": [
            ("學校風雨球場", "棒球、籃球、足球場多功能用網"),
            ("公園戶外球場", "社區公園、公共體育場"),
            ("沿海運動場館", "鹽害地區可長期使用"),
        ],
        "keywords": "風雨球場防護網,戶外球場網,抗UV球場網,風雨操場攔截網,戶外運動安全網",
    },
    "s5": {
        "brand": "safety", "slug": "solar-panel-net",
        "name": "太陽能板防護網", "tag": "防鳥防墜", "icon": "shield",
        "category": "industrial", "category_name": "工業廠房",
        "summary": "防止鳥類築巢、異物掉落，保護光電系統。不影響光電效能，可大幅延長太陽能板壽命，光電廠與住宅光電皆適用。",
        "description": "太陽能板下方常成為鳥類築巢地點，鳥糞、巢材會降低發電效率甚至引發短路。安隆太陽能防護網從板下、板側包覆，阻絕鳥類但不擋光，是光電場、屋頂型光電系統的必備配件。",
        "features": [
            "完全不影響光電發電效率",
            "阻絕麻雀、鴿子、白鷺等常見鳥類",
            "可承受異物掉落衝擊（樹葉、樹枝）",
            "不鏽鋼夾具，不破壞光電結構",
            "10+ 年戶外使用壽命",
            "鳥類友善（不傷害鳥類本身）",
            "可拆卸式設計，方便板下維護",
        ],
        "specs": {
            "線徑": "2–3mm（細線不影響採光）",
            "網目": "2.5cm（防鳥標準）",
            "材質": "PE 抗 UV 黑色（適配光電板色系）",
            "固定方式": "不鏽鋼夾具，免鑽孔",
            "尺寸": "依光電板陣列客製",
        },
        "use_cases": [
            ("地面型光電場", "永安、永興等大型光電廠"),
            ("屋頂光電系統", "住宅、廠房屋頂太陽能"),
            ("水面型光電", "埤塘、滯洪池上方光電系統"),
        ],
        "keywords": "太陽能板防護網,光電廠防鳥網,太陽能防鳥網,光電板防護,太陽能異物攔截網",
    },
    "s6": {
        "brand": "safety", "slug": "factory-safety-net",
        "name": "公司廠區安全網", "tag": "工業級", "icon": "shield",
        "category": "industrial", "category_name": "工業廠房",
        "summary": "物架安全網、倉儲防護網，工業級線徑訂製。可依倉儲規範裝設防墜層、防落物層，符合 ISO 工安要求。",
        "description": "現代工廠倉儲多採用高架儲位，物品墜落是嚴重的工安事故來源。安隆廠區安全網針對倉儲走道、貨架背面、輸送帶上方等高風險區設計，線徑加粗、網目縮小，可承受工業級重物衝擊。",
        "features": [
            "工業級高張力編織，承重 ≥ 150kg/m²",
            "防止托盤、紙箱、零件墜落",
            "符合 ISO 45001 工安認證要求",
            "可裝設多層（防墜 + 防落物）",
            "難燃處理選項（B1 級）",
            "防靜電版本（電子廠專用）",
            "可結合貨架既有結構安裝",
        ],
        "specs": {
            "線徑": "6mm（工業加強）",
            "網目": "5×5 cm（細密防小物件）",
            "材質": "高張力特多龍 / 可選難燃版",
            "承重": "≥ 150 kg/m²",
            "尺寸": "依貨架規格客製",
        },
        "use_cases": [
            ("半導體廠 / 電子廠", "無塵室外圍倉儲防護"),
            ("傳統製造業廠房", "鋼鐵、機械零件倉儲"),
            ("物流倉儲中心", "高架儲位、輸送帶上方"),
        ],
        "keywords": "廠區安全網,工業安全網,倉儲防護網,物架安全網,工廠防墜網,工業防護網",
    },
    "s7": {
        "brand": "safety", "slug": "bird-prevention-net",
        "name": "農業防鳥網", "tag": "農用", "icon": "shield",
        "category": "agriculture", "category_name": "農業用網",
        "summary": "果園、雞舍、農場專用，多種網目尺寸選擇。可阻擋麻雀、白鷺鷥等常見害鳥，不傷害鳥類本身，環境友善。",
        "description": "農作物受鳥害是農民長期困擾，傳統毒餌、彈弓既不人道也不持久。安隆防鳥網以物理隔絕方式根本解決鳥害，網目尺寸依目標鳥種設計，從麻雀（1.5cm）到白鷺鷥（5cm）皆有對應規格。",
        "features": [
            "物理阻絕，不傷害鳥類",
            "依鳥種選擇網目（1.5–5cm）",
            "可承受採收期重量",
            "輕量化設計，一人可操作",
            "可選顏色：透明（果園）/ 黑色（雞舍）",
            "抗 UV 處理，戶外 3–5 年使用壽命",
            "支援溫室、隧道棚架設",
        ],
        "specs": {
            "線徑": "0.5–1.5mm（細線不影響採光）",
            "網目": "1.5cm / 2.5cm / 4cm / 5cm",
            "材質": "PE / HDPE 抗 UV",
            "顏色": "透明、黑、白、綠",
            "尺寸": "卷材 4×30m 起，可裁切",
        },
        "use_cases": [
            ("果園", "葡萄、芭樂、棗子、釋迦防鳥"),
            ("雞舍鴨舍", "防止野鳥傳染禽流感"),
            ("水稻田", "麻雀群害防治"),
        ],
        "keywords": "防鳥網,農業用網,果園防鳥網,雞舍防鳥網,水稻防鳥網,農場防鳥",
    },
    "s8": {
        "brand": "safety", "slug": "shade-net",
        "name": "遮光網", "tag": "降溫節能", "icon": "shield",
        "category": "agriculture", "category_name": "農業用網",
        "summary": "針織 50–80%、平織 50–95% 遮光率，多種規格。安裝後室內可降溫約 2 度，節能省電，可選固定式或活動式。",
        "description": "夏季高溫不僅讓人不適也讓冷氣費飆升。安隆遮光網依使用場景提供針織與平織兩種材質：針織耐用度高但遮光率較低；平織遮光率可達 95% 但壽命較短。圓扁紗針織版本則融合兩者優點。",
        "features": [
            "針織版：遮光 50–80%，5+ 年耐用",
            "平織版：遮光 50–95%，遮陽效果強",
            "圓扁紗針織：耐用與遮光兼顧",
            "活動式可拉動，依日照調整",
            "固定式可長期使用",
            "可降低室內溫度約 2 度",
            "農作育苗、頂樓加蓋皆適用",
        ],
        "specs": {
            "材質": "針織 PE / 平織 PE / 圓扁紗",
            "遮光率": "50% / 60% / 70% / 80% / 95%",
            "顏色": "黑、銀、白、墨綠",
            "規格": "卷材 4×30m 起",
            "施工": "固定式或活動式可選",
        },
        "use_cases": [
            ("住宅頂樓", "降低室內溫度、節省冷氣費"),
            ("農作育苗區", "高溫期保護幼苗"),
            ("停車場 / 庭院", "車輛防曬、室外活動區"),
        ],
        "keywords": "遮光網,遮陽網,頂樓遮陽,農用遮光網,降溫網,節能遮陽網",
    },
    "s9": {
        "brand": "safety", "slug": "playground-net",
        "name": "兒童遊戲場防護網", "tag": "兒童安全", "icon": "shield",
        "category": "public", "category_name": "公共設施",
        "summary": "幼兒園、公園遊樂設施專用，符合兒童安全標準。色彩鮮豔、邊角圓滑、無毒材質，讓孩子玩得安全也玩得開心。",
        "description": "兒童遊戲場是事故率較高的場域，地面、攀爬設施、滑梯邊緣都需要妥善防護。安隆兒童遊戲場專用網採用無毒 PE 材質、軟性編織、邊角圓滑處理，並提供繽紛色彩讓孩子在愉悅環境中遊玩。",
        "features": [
            "通過 SGS 無毒材質檢驗",
            "邊角圓滑處理，不刮傷孩童",
            "軟性編織，碰撞緩衝效果好",
            "11 種繽紛色彩可選",
            "符合 CNS 兒童遊戲場設備標準",
            "防紫外線、戶外不脆化",
            "支援大型攀爬網結構（人類攀爬網）",
        ],
        "specs": {
            "線徑": "3–4mm 軟性編織",
            "網目": "5×5 cm 或 7×7 cm",
            "材質": "無毒 PE / 特多龍",
            "顏色": "11 色繽紛可選",
            "認證": "CNS 兒童遊戲場標準",
        },
        "use_cases": [
            ("公私立幼兒園", "教室外遊戲場、攀爬區防護"),
            ("社區親子公園", "公共遊樂設施防護"),
            ("商場親子樂園", "室內遊樂場、爬爬區"),
        ],
        "keywords": "兒童遊戲場安全網,幼兒園防護網,遊樂設施安全網,兒童攀爬網,親子公園防護網",
    },
    "s10": {
        "brand": "safety", "slug": "barrier-net",
        "name": "隔離阻擋用安全網", "tag": "分區隔離", "icon": "shield",
        "category": "public", "category_name": "公共設施",
        "summary": "人車分流、區域隔離、活動分區用網。可快速架設、收納，活動式設計適合短期工程與大型活動。",
        "description": "大型活動、臨時工區、車輛動線管制等場合，需要快速架設可移動的隔離網。安隆隔離阻擋網採用模組化設計，可單片組合、依場地調整，活動結束後可快速收納再利用。",
        "features": [
            "模組化單片設計，自由組合長度",
            "快速架設，2 人 30 分鐘完成 100m",
            "可收納重複使用，環保耐用",
            "鮮明警示色，遠距可見",
            "可附 logo 印刷（活動專用）",
            "可選透視款（網目大）或遮蔽款（網目密 + 遮陽布）",
            "防傾倒底座，戶外風大也穩固",
        ],
        "specs": {
            "高度": "1.2m / 1.8m / 2.4m 可選",
            "單片長度": "2m / 3m",
            "材質": "PE / 特多龍",
            "顏色": "橘 / 黃 / 紅警示色",
            "配件": "可選底座、警示燈、logo 印刷",
        },
        "use_cases": [
            ("大型戶外活動", "演唱會、市集、運動會分區"),
            ("臨時工區", "短期工程的人車隔離"),
            ("展場 / 賣場", "貨架區、活動區分隔"),
        ],
        "keywords": "隔離網,阻擋網,分區網,活動安全網,警示網,人車分流網",
    },
    "s11": {
        "brand": "safety", "slug": "climbing-net",
        "name": "人類攀爬網", "tag": "遊樂設施", "icon": "shield",
        "category": "public", "category_name": "公共設施",
        "summary": "兒童遊樂場攀爬網，正方形網目設計。承載多人同時攀爬，繩結結構安全經過認證，是體能訓練的最佳選擇。",
        "description": "攀爬網是兒童體能發展的優秀器材，可訓練平衡感、肌肉協調、勇氣與決斷力。安隆人類攀爬網依規範採用正方形網目設計（不同於菱形的防墜網），繩結處特別加固，可承載多名孩童同時攀爬。",
        "features": [
            "正方形網目（符合人類攀爬網規範）",
            "繩結雙重加固，可承載多人同時攀爬",
            "粗繩設計，手部抓握舒適",
            "8mm 以上線徑，承重 500kg+",
            "可設計 3D 立體攀爬塔",
            "戶外抗 UV 處理",
            "適合幼兒園、體能教室、戶外公園",
        ],
        "specs": {
            "線徑": "8–14mm（粗繩）",
            "網目": "20×20 cm 或 30×30 cm 正方形",
            "材質": "高張力特多龍粗繩",
            "承重": "500 kg+",
            "形式": "平面、傾斜、立體塔狀皆可訂製",
        },
        "use_cases": [
            ("體能教室", "幼兒園、體能補習班"),
            ("公園地景設施", "都會公園的攀爬塔"),
            ("學校體育設施", "國小操場體能挑戰區"),
        ],
        "keywords": "攀爬網,兒童攀爬網,體能訓練網,遊樂場攀爬網,粗繩攀爬網",
    },
    "s12": {
        "brand": "safety", "slug": "tile-protection-net",
        "name": "防磁磚掉落網", "tag": "外牆防護", "icon": "shield",
        "category": "construction", "category_name": "工程營建",
        "summary": "老舊大樓外牆磁磚防護，保護行人安全。透明或細網目設計，不影響大樓外觀，是都市更新前的必備防護。",
        "description": "台灣老舊大樓常因熱脹冷縮、地震、漏水導致外牆磁磚剝落，砸傷行人事件頻傳。安隆防磁磚網從外牆懸掛，可承接掉落磁磚，避免砸傷人車。網目細密但採用透明或細線設計，盡量降低對建築外觀的影響。",
        "features": [
            "承接磁磚、混凝土小塊墜落",
            "細線設計，不影響大樓外觀",
            "透明 / 半透明選項",
            "高張力編織，可承受塊狀衝擊",
            "可整棟包覆或局部安裝",
            "符合都市更新前的暫時防護需求",
            "鋼索 + 不鏽鋼支架固定，10+ 年壽命",
        ],
        "specs": {
            "線徑": "2–3mm（細線）",
            "網目": "2×2 cm（防止小塊磁磚通過）",
            "材質": "高張力 PE / 特多龍",
            "顏色": "透明 / 黑 / 灰（融入建築）",
            "固定": "鋼索 + 不鏽鋼支架",
        },
        "use_cases": [
            ("30 年以上老舊大樓", "公寓、商辦、社區大樓"),
            ("都市更新等待期", "拆除前的暫時防護"),
            ("特殊建材外牆", "石材、預鑄板的二次防護"),
        ],
        "keywords": "防磁磚掉落網,外牆防墜網,磁磚剝落防護,老舊大樓外牆網,磁磚墜落防護網",
    },
    # ============== 安隆居家 ==============
    "h1": {
        "brand": "home", "slug": "stairs-safety-net",
        "name": "樓梯防墜安全網", "tag": "熱銷款", "icon": "home",
        "category": "stairs", "category_name": "樓梯防護",
        "summary": "透天樓梯標配，5mm 線徑 10×10cm 網目，符合國家標準。可選擇 11 種顏色搭配居家風格，安裝快速、整潔美觀。",
        "description": "透天厝、樓中樓的開放式樓梯是兒童、長輩、寵物的重大安全隱患。安隆樓梯防墜網採用政府標準規格（5mm 線徑、10×10cm 菱形網目），完整包覆樓梯間中央天井，從根本防止墜落事故，是有孩童或長輩家庭的必備設施。",
        "features": [
            "政府標準規格：5mm 線徑 10×10cm 菱形網目",
            "11 種顏色可選，依居家風格搭配",
            "包覆樓梯中央天井，無死角防護",
            "邊繩穿線、四角打結加固",
            "安裝過程不破壞牆面、扶手結構",
            "可承受成人意外重量",
            "室內保固 2 年（非人為因素損壞）",
        ],
        "specs": {
            "線徑": "5mm（國家標準）",
            "網目": "10×10 cm 菱形",
            "材質": "尼龍（室內專用）",
            "顏色": "白為基本款，10 種彩色可選（彩色加價）",
            "尺寸": "依樓梯天井客製測量",
        },
        "use_cases": [
            ("透天厝家庭", "2–4 層樓開放式樓梯防護"),
            ("樓中樓住宅", "夾層樓梯天井防墜"),
            ("有孩童 / 長輩 / 寵物家庭", "全家安心的基本配備"),
        ],
        "keywords": "樓梯防墜網,樓梯安全網,透天樓梯防墜,居家防墜網,室內樓梯防護,高雄樓梯安全網",
    },
    "h2": {
        "brand": "home", "slug": "l-shape-stairs-net",
        "name": "L 型樓梯安全網", "tag": "客製化", "icon": "home",
        "category": "stairs", "category_name": "樓梯防護",
        "summary": "依樓梯形狀客製，多色可選，安裝整潔美觀。轉角處特殊處理，線條俐落不雜亂，是 L 型樓梯天井的完美解決方案。",
        "description": "L 型樓梯是常見的設計，但其轉角處難以用標準矩形網涵蓋。安隆 L 型專用網透過現場精確測量，依實際樓梯轉角角度製作，無多餘繩索、無鬆垮現象，安裝後線條俐落如同建築結構一部分。",
        "features": [
            "依現場測量精準訂製",
            "轉角處特殊縫合處理",
            "無多餘繩索、無鬆垮",
            "可選 11 種顏色搭配",
            "保留樓梯採光與通透感",
            "現場安裝 1 天完成",
            "適合別墅、樓中樓 L 型樓梯",
        ],
        "specs": {
            "線徑": "5mm",
            "網目": "10×10 cm 菱形",
            "形狀": "L 型轉角特製",
            "材質": "尼龍（室內）",
            "尺寸": "現場測量訂製",
        },
        "use_cases": [
            ("L 型透天厝", "2–4 層 L 型開放式樓梯"),
            ("別墅樓梯", "高級住宅的設計感樓梯"),
            ("樓中樓夾層", "現代設計感樓梯天井"),
        ],
        "keywords": "L型樓梯安全網,L型樓梯防墜網,客製樓梯網,別墅樓梯防墜",
    },
    "h3": {
        "brand": "home", "slug": "square-stairs-net",
        "name": "口字型樓梯安全網", "tag": "全周防護", "icon": "home",
        "category": "stairs", "category_name": "樓梯防護",
        "summary": "中央天井包覆式設計，全周防護無死角。適合中庭式透天厝、別墅、樓中樓挑高空間。",
        "description": "口字型樓梯的中央天井往往挑高 2–3 層樓，是兒童最容易發生意外的位置之一。安隆口字型專用網從天井四面完整包覆，形成一個完整的「網箱」，孩童、寵物、物品掉落時皆能承接。",
        "features": [
            "四面完整包覆，全周防護無死角",
            "可承受成人意外墜落衝擊",
            "天井挑高可達 3+ 層樓",
            "中央可保留採光（網體仍有透光）",
            "11 種顏色搭配，可與牆面同色融入",
            "邊繩鋼索加強選項（高樓層必選）",
            "施工不破壞天井結構",
        ],
        "specs": {
            "線徑": "5mm（標準）／7mm（高樓層加強）",
            "網目": "10×10 cm 菱形",
            "形狀": "口字型四面包覆",
            "材質": "尼龍 / 特多龍可選",
            "尺寸": "依天井寬深客製",
        },
        "use_cases": [
            ("中庭式透天厝", "傳統閩南建築風格透天"),
            ("挑高別墅", "現代建築的中央採光井"),
            ("企業會所", "辦公空間的天井防護"),
        ],
        "keywords": "口字型樓梯安全網,中庭天井防墜網,全周樓梯防護,挑高樓梯防墜網",
    },
    "h4": {
        "brand": "home", "slug": "triangle-stairs-net",
        "name": "三角型樓梯安全網", "tag": "訂製款", "icon": "home",
        "category": "stairs", "category_name": "樓梯防護",
        "summary": "特殊樓梯結構訂製，精準貼合不留縫隙。提供現場測量服務，誤差 ≤ 1cm，是不規則樓梯的唯一解。",
        "description": "三角型樓梯常出現在角間透天、舊式建築、特殊設計住宅。標準矩形網無法妥善覆蓋三角區域，孩童容易從縫隙鑽過。安隆三角型專用網依現場 3 點測量精準訂製，貼合三角結構不留任何縫隙。",
        "features": [
            "現場 3 點精準測量（誤差 ≤ 1cm）",
            "三角結構完整貼合",
            "無縫隙、無鬆垮",
            "適合角間透天、特殊建築",
            "11 種顏色可選",
            "可結合 L 型網組合複雜樓梯",
            "施工 7 日內可到場",
        ],
        "specs": {
            "線徑": "5mm",
            "網目": "10×10 cm 菱形",
            "形狀": "依三角角度訂製",
            "材質": "尼龍（室內）",
            "尺寸": "現場測量訂製",
        },
        "use_cases": [
            ("角間透天厝", "三角窗、轉角戶型"),
            ("舊式公寓", "不規則格局的老屋樓梯"),
            ("特殊設計住宅", "建築師設計的非標準樓梯"),
        ],
        "keywords": "三角型樓梯安全網,三角樓梯防墜,角間樓梯防護,特殊樓梯安全網",
    },
    "h5": {
        "brand": "home", "slug": "invisible-grilles",
        "name": "隱形鐵窗", "tag": "不影響採光", "icon": "home",
        "category": "window", "category_name": "窗戶鐵窗",
        "summary": "2mm 白鐵鋼索包 PVC，防鳥 2.5cm／防人 5cm 間隔。不影響採光、視野與外觀，社區規約友善，是現代家庭的最佳選擇。",
        "description": "傳統鐵窗醜陋且阻擋逃生路線，但無防護又有兒童墜落風險。安隆隱形鐵窗以細鋼索取代傳統鐵條，遠看幾乎不可見，近看也只是細線條，完整保留窗戶採光與視野，同時防止兒童墜落、貓咪外逃、宵小入侵。",
        "features": [
            "2mm 不鏽鋼索（內芯）+ PVC 包覆（外層）",
            "防鳥版：2.5cm 間隔（防麻雀以上）",
            "防人版：5cm 間隔（防兒童墜落 / 寵物外逃）",
            "遠看幾乎不可見，保留窗景",
            "完整保留採光（不影響通風）",
            "符合社區管委會無外觀變動規約",
            "可選顏色：白、黑、灰（配合窗框）",
        ],
        "specs": {
            "鋼索": "2mm 白鐵不鏽鋼",
            "外層": "PVC 包覆（防鏽、防割手）",
            "間隔": "防鳥 2.5cm / 防人 5cm",
            "固定": "鋁合金支架（單點承重 50kg+）",
            "保固": "室外 1 年",
        },
        "use_cases": [
            ("高樓層住宅", "10 樓以上窗戶的墜落防護"),
            ("有兒童 / 貓咪家庭", "防止兒童攀爬、貓咪外逃"),
            ("社區管委會限制戶", "規約禁止裝鐵窗的大樓"),
        ],
        "keywords": "隱形鐵窗,隱形鐵窗推薦,高雄隱形鐵窗,台中隱形鐵窗,雙北隱形鐵窗,鋼索隱形窗,貓咪窗,防墜窗",
    },
    "h6": {
        "brand": "home", "slug": "window-safety-net",
        "name": "窗戶防墜網", "tag": "兒童防墜", "icon": "home",
        "category": "window", "category_name": "窗戶鐵窗",
        "summary": "兒童墜落防護，安裝快速不破壞窗框。可拆卸式設計，搬家時可帶走，是租屋族與小資家庭的好選擇。",
        "description": "兒童墜樓事件多發生於窗戶、陽台等家中常被忽略的位置。安隆窗戶防墜網以軟性網體形式裝設於窗戶內側，可承受兒童意外重量。與隱形鐵窗相比，安裝更快速、價格更實惠，且可拆卸帶走。",
        "features": [
            "5mm 線徑、10×10cm 網目（國家標準）",
            "張掛式安裝，不破壞窗框",
            "可拆卸式設計，搬家可帶走",
            "可承受兒童 30kg 衝擊",
            "11 種顏色搭配窗簾色系",
            "適合租屋族（房東不允許裝鐵窗）",
            "1 小時內完成安裝",
        ],
        "specs": {
            "線徑": "5mm",
            "網目": "10×10 cm 菱形",
            "材質": "尼龍（室內）",
            "固定": "張掛式（不鏽鋼勾 + 不破壞牆面）",
            "保固": "室內 2 年",
        },
        "use_cases": [
            ("有幼兒家庭", "預防兒童攀爬窗戶墜落"),
            ("租屋族", "可拆卸帶走，房東無異議"),
            ("過渡期住宅", "等都更、等搬家的暫時防護"),
        ],
        "keywords": "窗戶防墜網,兒童防墜網,窗戶安全網,租屋防墜,兒童窗戶防護網",
    },
    "h7": {
        "brand": "home", "slug": "balcony-safety-net",
        "name": "頂樓陽台防墜網", "tag": "貓奴必備", "icon": "home",
        "category": "balcony", "category_name": "陽台頂樓",
        "summary": "陽台、頂樓加強防護，貓咪友善不外逃。專為毛孩家庭設計，網目密度防止頭部卡住，11 色可選不影響景觀。",
        "description": "貓咪好奇心強，陽台、頂樓是最容易發生「飛貓」事件的場所。安隆陽台頂樓防墜網特別考量寵物安全：網目密度避免貓咪頭部卡住，材質柔軟不傷爪，顏色多樣可融入環境，讓毛孩自由活動同時保障安全。",
        "features": [
            "貓咪友善設計：網目防止頭部卡住",
            "柔軟材質不傷爪",
            "5×5 cm 細網目（防小型寵物外逃）",
            "可包覆陽台欄杆 + 上方天空（防鳥同步）",
            "11 色可選，可選擇與外牆同色融入",
            "頂樓全包覆設計（含天頂遮鳥網）",
            "材質抗 UV，戶外 5+ 年",
        ],
        "specs": {
            "線徑": "3–4mm",
            "網目": "5×5 cm 或 7×7 cm",
            "材質": "特多龍（戶外）",
            "顏色": "11 色可選",
            "保固": "戶外 1 年",
        },
        "use_cases": [
            ("養貓家庭", "防止貓咪攀爬陽台外逃"),
            ("頂樓加蓋住宅", "頂樓全包覆防墜 + 防鳥"),
            ("有幼兒陽台", "兒童陽台安全防護"),
        ],
        "keywords": "陽台防墜網,頂樓防墜網,貓咪防逃網,寵物陽台安全網,陽台貓網,頂樓加蓋防墜",
    },
    "h8": {
        "brand": "home", "slug": "colorful-safety-net",
        "name": "創意彩色安全網", "tag": "繽紛時尚", "icon": "home",
        "category": "creative", "category_name": "創意客製",
        "summary": "白／黑／藍／紫／咖／綠／紅／橘／黃多色搭配。可拼接漸層、條紋等創意圖案，把防護變成居家裝飾的一部分。",
        "description": "誰說安全網一定要醜醜的白色？安隆創意彩色安全網提供 11 種顏色任意搭配，可以做成漸層、條紋、棋盤格、漸變色等圖案，讓安全防護變成兒童房的趣味裝飾、咖啡店的吸睛元素、設計師宅的點綴。",
        "features": [
            "11 種顏色任意搭配",
            "可訂製漸層、條紋、棋盤格圖案",
            "色彩 UV 穩定，5+ 年不明顯褪色",
            "適合兒童房、咖啡店、設計感空間",
            "可與品牌色系搭配（商業空間）",
            "提供色彩搭配建議",
            "顏色越多價格越高，但仍符合居家預算",
        ],
        "specs": {
            "線徑": "5mm",
            "網目": "10×10 cm 菱形",
            "材質": "尼龍（室內）",
            "顏色": "11 色全可選",
            "圖案": "漸層、條紋、棋盤、自訂圖案",
        },
        "use_cases": [
            ("兒童房 / 親子空間", "繽紛色彩刺激孩童視覺發展"),
            ("咖啡店 / 商店裝飾", "吸睛裝置、品牌色融入"),
            ("設計師宅", "建築師事務所、自宅亮點"),
        ],
        "keywords": "創意安全網,彩色安全網,設計感樓梯網,兒童房安全網,客製彩色防墜網",
    },
    "h9": {
        "brand": "home", "slug": "handrail-net",
        "name": "手扶梯欄桿網", "tag": "社區規範", "icon": "home",
        "category": "stairs", "category_name": "樓梯防護",
        "summary": "4mm 線徑 7×7cm 網目，符合大樓最新管理規定。每支欄桿上下打結，單線斷不全散，是社區大樓必裝項目。",
        "description": "大樓樓梯間欄桿間距常大於 10 公分，孩童容易鑽過導致墜樓。最新大樓管理條例要求欄桿縫隙必須補小於 10cm，安隆手扶梯欄桿網以細網包覆現有欄桿，符合法規同時不破壞原始結構。",
        "features": [
            "符合大樓管理條例（縫隙 < 10cm）",
            "每支欄桿上下打結（單線斷不全散）",
            "7×7 cm 小網目（兒童頭部無法穿過）",
            "細線徑不影響欄桿美觀",
            "11 色可選，可配合扶手色系",
            "施工不破壞欄桿原結構",
            "適用所有透天 / 大樓樓梯",
        ],
        "specs": {
            "線徑": "4mm（無重力負荷無需粗線）",
            "網目": "7×7 cm",
            "材質": "尼龍（室內）",
            "顏色": "11 色可選",
            "綁紮": "每支欄桿獨立打結",
        },
        "use_cases": [
            ("社區大樓樓梯間", "符合管委會新規定的補網"),
            ("學校 / 公部門樓梯", "公共空間欄桿補強"),
            ("透天厝樓梯", "現有欄桿補小縫隙"),
        ],
        "keywords": "手扶梯欄桿網,樓梯欄桿補網,大樓樓梯縫隙網,欄桿安全網,樓梯欄桿防護",
    },
    "h10": {
        "brand": "home", "slug": "escalator-net",
        "name": "電扶梯安全網", "tag": "公共空間", "icon": "home",
        "category": "stairs", "category_name": "樓梯防護",
        "summary": "商場、車站電扶梯側邊防護。專用安裝結構，不干擾電扶梯運作，符合公共安全法規。",
        "description": "電扶梯上方的開放空間是兒童意外發生熱點，孩童的腳部、衣物可能從欄桿縫隙掉下。安隆電扶梯安全網針對電扶梯結構特殊設計，從欄桿外側懸掛，完整封閉縫隙又不干擾電扶梯本身運作。",
        "features": [
            "符合電扶梯側邊安全規範",
            "不干擾電扶梯機械運作",
            "可承受兒童墜落衝擊",
            "適用電扶梯與手扶梯",
            "現場精準測量，貼合電扶梯曲線",
            "可選防火等級網體（B1）",
            "公共空間專業安裝",
        ],
        "specs": {
            "線徑": "4mm",
            "網目": "7×7 cm",
            "材質": "尼龍 / 可選難燃版",
            "固定": "電扶梯欄桿不破壞式固定",
            "適用": "商場、車站、機場、醫院",
        },
        "use_cases": [
            ("百貨商場", "電扶梯上下交叉處的側邊防護"),
            ("車站機場", "高人流公共空間的兒童保護"),
            ("醫院 / 公部門", "公共電扶梯的兒童意外預防"),
        ],
        "keywords": "電扶梯安全網,手扶梯安全網,商場電扶梯防護,公共空間電扶梯網",
    },
    "h11": {
        "brand": "home", "slug": "pool-safety-net",
        "name": "水池安全防護網", "tag": "水池防護", "icon": "home",
        "category": "balcony", "category_name": "陽台頂樓",
        "summary": "景觀池、魚池防墜，兒童寵物雙重保障。可承重式設計，承載成人重量，是有水景住宅的必備設施。",
        "description": "庭院景觀池、魚池雖然美觀，但對幼兒、寵物來說是溺水風險。安隆水池防護網以可承重結構懸於水面上方或包覆水池四周，意外發生時可承接落水者，提供關鍵的緊急救援時間。",
        "features": [
            "承重型設計（承載成人 70kg+）",
            "細網目防止兒童頭部進水",
            "可選透明色（不影響水景觀賞）",
            "鋼索 + 不鏽鋼支架固定",
            "可拆卸式（換水、清潔時可移除）",
            "防滑、防鏽處理",
            "戶外 UV 抗化 5+ 年壽命",
        ],
        "specs": {
            "線徑": "5mm（承重設計）",
            "網目": "10×10 cm 或 5×5 cm",
            "材質": "高張力特多龍",
            "固定": "不鏽鋼支架 + 鋼索",
            "尺寸": "依水池大小客製",
        },
        "use_cases": [
            ("住宅景觀池", "庭院魚池、噴水池防墜"),
            ("親子餐廳 / 民宿", "公共水景區域的兒童防護"),
            ("社區游泳池", "非營業時段的兒童預防"),
        ],
        "keywords": "水池防護網,魚池防墜網,景觀池安全網,水池兒童防護,泳池防墜網",
    },
    "h12": {
        "brand": "home", "slug": "bumper-strip",
        "name": "防撞條", "tag": "居家防護", "icon": "home",
        "category": "creative", "category_name": "創意客製",
        "summary": "牆角、柱子防撞，居家安全細節。多種顏色、軟硬度可選，自黏式安裝，是有幼兒或長輩家庭的貼心防護。",
        "description": "家中尖銳牆角、柱子角是幼兒學步、長輩跌倒的常見傷害源。安隆防撞條提供多種軟硬度與顏色選擇，自黏式安裝免工具，可包覆任何尖角結構，是低成本高效益的居家安全升級項目。",
        "features": [
            "自黏式安裝，無需工具",
            "多種軟硬度（軟質給幼兒、半硬給長輩）",
            "多種顏色搭配室內裝潢",
            "可裁切，貼合各種角度",
            "EVA / NBR 環保材質",
            "拆除不殘膠",
            "幼兒、長輩、寵物家庭三贏",
        ],
        "specs": {
            "材質": "EVA 軟質 / NBR 半硬",
            "厚度": "1cm / 2cm / 3cm 可選",
            "顏色": "透明、白、米、咖、黑",
            "規格": "每條 2m 起，可裁切",
            "黏著": "3M 自黏，不殘膠",
        },
        "use_cases": [
            ("有幼兒家庭", "茶几、牆角、桌角防撞"),
            ("長輩照護", "走道牆角、樓梯轉角防撞"),
            ("寵物友善宅", "貓咪柱子、牆角防撞防抓"),
        ],
        "keywords": "防撞條,牆角防撞,幼兒防撞條,居家防撞,長輩防撞,寵物防撞",
    },
}


# ============================================
# HTML 模板
# ============================================

def slugify_path(brand, slug):
    return f"products/{brand}/{slug}.html"


def render_features(features):
    return "\n".join(f"          <li>{f}</li>" for f in features)


def render_specs(specs):
    rows = []
    for k, v in specs.items():
        rows.append(f"          <tr><th>{k}</th><td>{v}</td></tr>")
    common = []
    for k, v in COMMON_SPECS.items():
        common.append(f"          <tr><th>{k}</th><td>{v}</td></tr>")
    return "\n".join(rows + common)


def render_use_cases(cases):
    items = []
    for i, (title, desc) in enumerate(cases, 1):
        items.append(f"""        <article class="usecase-card">
          <div class="usecase-card-num">{i:02d}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </article>""")
    return "\n".join(items)


def render_related_products(current_id, brand, category):
    """找同分類、不同 id 的其他產品，最多 3 個"""
    related = []
    for pid, p in PRODUCTS.items():
        if pid == current_id:
            continue
        if p["brand"] != brand:
            continue
        if p["category"] != category:
            continue
        related.append((pid, p))
        if len(related) >= 3:
            break
    # 如果同類產品不夠，從同品牌補
    if len(related) < 3:
        for pid, p in PRODUCTS.items():
            if pid == current_id:
                continue
            if p["brand"] != brand:
                continue
            if (pid, p) in related:
                continue
            related.append((pid, p))
            if len(related) >= 3:
                break

    items = []
    for pid, p in related:
        url = slugify_path(p["brand"], p["slug"])
        items.append(f"""        <a href="../../{url}" class="product-card" data-category="{p['category']}">
          <div class="product-visual">
            <div class="product-icon" data-icon="{p['icon']}"></div>
            <span class="product-tag">{p['tag']}</span>
          </div>
          <div class="product-body">
            <h3>{p['name']}</h3>
            <p>{p['summary'][:60]}...</p>
            <span class="product-link">查看詳情 →</span>
          </div>
        </a>""")
    return "\n".join(items)


def render_breadcrumb_jsonld(product):
    brand = product["brand"]
    brand_name = BRAND_NAMES[brand]
    name = product["name"]
    slug = product["slug"]
    return f"""    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "首頁",
          "item": "{SITE_URL}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "產品型錄",
          "item": "{SITE_URL}/#products"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{brand_name}",
          "item": "{SITE_URL}/#products"
        }},
        {{
          "@type": "ListItem",
          "position": 4,
          "name": "{name}",
          "item": "{SITE_URL}/products/{brand}/{slug}.html"
        }}
      ]
    }}"""


def render_product_jsonld(product):
    brand = product["brand"]
    return f"""    {{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "{product['name']}",
      "description": "{product['summary']}",
      "category": "{product['category_name']}",
      "brand": {{
        "@type": "Brand",
        "name": "{BRAND_NAMES[brand]}",
        "alternateName": "{BRAND_NAMES_EN[brand]}"
      }},
      "manufacturer": {{
        "@type": "Organization",
        "name": "安隆安全網有限公司",
        "url": "{SITE_URL}/"
      }},
      "offers": {{
        "@type": "Offer",
        "url": "{SITE_URL}/products/{brand}/{product['slug']}.html",
        "availability": "https://schema.org/InStock",
        "priceCurrency": "TWD",
        "priceSpecification": {{
          "@type": "PriceSpecification",
          "valueAddedTaxIncluded": true
        }}
      }}
    }}"""


def render_page(pid, product):
    brand = product["brand"]
    brand_name = BRAND_NAMES[brand]
    brand_en = BRAND_NAMES_EN[brand]
    slug = product["slug"]
    name = product["name"]
    summary = product["summary"]
    description = product["description"]
    tag = product["tag"]
    icon = product["icon"]
    category_name = product["category_name"]
    keywords = product["keywords"]

    features_html = render_features(product["features"])
    specs_html = render_specs(product["specs"])
    use_cases_html = render_use_cases(product["use_cases"])
    related_html = render_related_products(pid, brand, product["category"])
    breadcrumb_jsonld = render_breadcrumb_jsonld(product)
    product_jsonld = render_product_jsonld(product)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- SEO -->
  <title>{name}｜{brand_name} {tag} - 安隆安全網有限公司</title>
  <meta name="description" content="{summary}" />
  <meta name="keywords" content="{keywords},{brand_name},安隆安全網,免費估價" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{SITE_URL}/products/{brand}/{slug}.html" />

  <!-- Open Graph -->
  <meta property="og:type" content="product" />
  <meta property="og:locale" content="zh_TW" />
  <meta property="og:url" content="{SITE_URL}/products/{brand}/{slug}.html" />
  <meta property="og:title" content="{name}｜{brand_name} - 安隆安全網" />
  <meta property="og:description" content="{summary}" />
  <meta property="og:site_name" content="安隆安全網有限公司" />

  <!-- Google Search Console -->
  <meta name="google-site-verification" content="n2u56H6tGekvNenjobW76FdALH_lMMqFdFpkvfZbAXA" />

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

  <!-- Stylesheets -->
  <link rel="stylesheet" href="../../styles.css" />

  <!-- JSON-LD: Product -->
  <script type="application/ld+json">
{product_jsonld}
  </script>

  <!-- JSON-LD: Breadcrumb -->
  <script type="application/ld+json">
{breadcrumb_jsonld}
  </script>
</head>

<body data-brand="{brand}">
  <!-- ========== HEADER ========== -->
  <header class="header">
    <div class="container header-inner">
      <a href="../../index.html" class="logo">
        <span class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </span>
        <span class="logo-text">
          <span class="logo-name">安隆</span>
          <span class="logo-en">ANLONG SAFETY</span>
        </span>
      </a>

      <nav class="nav-desktop">
        <a href="../../index.html">首頁</a>
        <a href="../../products.html">產品型錄</a>
        <a href="../../cases.html">施工案例</a>
        <a href="../../about.html">關於安隆</a>
        <a href="../../faq.html">常見問題</a>
        <a href="../../contact.html">聯絡我們</a>
      </nav>

      <a href="tel:07-7828005" class="header-cta">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
        </svg>
        07-7828005
      </a>

      <button class="mobile-toggle" id="mobileToggle" aria-label="開啟選單">
        <svg class="icon-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <nav class="nav-mobile" id="navMobile">
      <a href="../../index.html">首頁</a>
      <a href="../../products.html">產品型錄</a>
      <a href="../../cases.html">施工案例</a>
      <a href="../../about.html">關於安隆</a>
      <a href="../../faq.html">常見問題</a>
      <a href="../../contact.html">聯絡我們</a>
      <a href="tel:07-7828005" class="mobile-cta">立即來電 07-7828005</a>
    </nav>
  </header>

  <main>
    <!-- ========== Breadcrumb ========== -->
    <nav class="breadcrumb" aria-label="麵包屑">
      <div class="container">
        <a href="../../index.html">首頁</a>
        <span class="separator">›</span>
        <a href="../../products.html">產品型錄</a>
        <span class="separator">›</span>
        <a href="../../products.html">{brand_name}</a>
        <span class="separator">›</span>
        <span class="current">{name}</span>
      </div>
    </nav>

    <!-- ========== 產品主視覺 ========== -->
    <section class="product-page-hero">
      <div class="container">
        <div class="product-page-hero-inner">
          <div class="product-page-visual">
            <div class="product-page-icon" data-icon="{icon}"></div>
          </div>
          <div class="product-page-info">
            <span class="product-tag">{tag}</span>
            <h1 class="product-page-title">{name}</h1>
            <p class="product-page-summary">{description}</p>
            <div class="product-page-cta">
              <a href="tel:07-7828005" class="btn btn-accent">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                立即來電詢價
              </a>
              <a href="../../contact.html" class="btn btn-outline">免費現場估價</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========== 產品特色 ========== -->
    <section class="product-section">
      <div class="container">
        <h2>產品特色</h2>
        <ul class="feature-list">
{features_html}
        </ul>
      </div>
    </section>

    <!-- ========== 產品規格 ========== -->
    <section class="product-section product-section-alt">
      <div class="container">
        <h2>產品規格</h2>
        <table class="specs-table">
          <tbody>
{specs_html}
          </tbody>
        </table>
      </div>
    </section>

    <!-- ========== 應用場景 ========== -->
    <section class="product-section">
      <div class="container">
        <h2>應用場景</h2>
        <div class="usecase-list">
{use_cases_html}
        </div>
      </div>
    </section>

    <!-- ========== 相關產品 ========== -->
    <section class="product-section product-section-alt">
      <div class="container">
        <h2>相關產品</h2>
        <div class="products-grid related-grid">
{related_html}
        </div>
      </div>
    </section>

    <!-- ========== CTA ========== -->
    <section class="product-cta-section">
      <div class="hero-bg-pattern"></div>
      <div class="container">
        <h2>免費現場估價</h2>
        <p>{name}依現場環境客製，價格與五金材料、安裝位置、網子數量相關。歡迎來電或加 LINE 諮詢，我們會盡快回覆。</p>
        <div class="cta-buttons">
          <a href="tel:07-7828005" class="btn btn-accent">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            07-7828005
          </a>
          <a href="https://line.me/R/ti/p/@643qzkfp" class="btn btn-outline" target="_blank" rel="noopener noreferrer">LINE 諮詢</a>
        </div>
      </div>
    </section>
  </main>

  <!-- ========== Footer ========== -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="logo footer-logo">
            <span class="logo-icon">
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
          <h4>產品分類</h4>
          <ul>
            <li><a href="../../products.html">安隆安全 · 工程級</a></li>
            <li><a href="../../products.html">安隆居家 · 住宅用</a></li>
            <li><a href="../../cases.html">施工案例</a></li>
            <li><a href="../../faq.html">常見問題</a></li>
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

  <!-- LINE 浮動按鈕 -->
  <a href="https://line.me/R/ti/p/@643qzkfp" class="line-float" target="_blank" rel="noopener noreferrer">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    <span>LINE 諮詢</span>
  </a>

  <script src="../../script.js" defer></script>
</body>
</html>
"""


def _ensure_svg_dimensions(html_text):
    """為沒有 width 屬性的 <svg> 加上 width/height（CSS 失效時的保險）"""
    import re
    return re.sub(r'<svg(?![^>]*\swidth=)', '<svg width="20" height="20"', html_text)


# ============================================
# 生成所有產品頁面
# ============================================
def main():
    # 建立 products/safety/ 和 products/home/
    (PRODUCTS_DIR / "safety").mkdir(parents=True, exist_ok=True)
    (PRODUCTS_DIR / "home").mkdir(parents=True, exist_ok=True)

    count = 0
    for pid, product in PRODUCTS.items():
        brand = product["brand"]
        slug = product["slug"]
        out_path = PRODUCTS_DIR / brand / f"{slug}.html"
        html = _ensure_svg_dimensions(render_page(pid, product))
        out_path.write_text(html, encoding="utf-8")
        count += 1
        print(f"  ✓ {brand}/{slug}.html  ({product['name']})")

    print(f"\n✅ 成功生成 {count} 個產品頁面")

    # 同時生成 sitemap.xml
    generate_sitemap()


def generate_sitemap():
    from datetime import date
    today = date.today().isoformat()

    urls = [
        (f"{SITE_URL}/", "1.0", "weekly"),
        (f"{SITE_URL}/products.html", "0.9", "weekly"),
        (f"{SITE_URL}/cases.html", "0.7", "monthly"),
        (f"{SITE_URL}/about.html", "0.6", "monthly"),
        (f"{SITE_URL}/faq.html", "0.6", "monthly"),
        (f"{SITE_URL}/contact.html", "0.7", "monthly"),
    ]
    # 加入所有產品頁
    for pid, p in PRODUCTS.items():
        urls.append((f"{SITE_URL}/products/{p['brand']}/{p['slug']}.html", "0.8", "monthly"))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, priority, changefreq in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{url}</loc>")
        xml.append(f"    <lastmod>{today}</lastmod>")
        xml.append(f"    <changefreq>{changefreq}</changefreq>")
        xml.append(f"    <priority>{priority}</priority>")
        xml.append("  </url>")
    xml.append("</urlset>")

    (OUTPUT_DIR / "sitemap.xml").write_text("\n".join(xml), encoding="utf-8")
    print(f"✅ sitemap.xml 已生成（{len(urls)} 筆 URL）")


if __name__ == "__main__":
    main()
