"""Build the lightweight client-side search index used by every page."""

from __future__ import annotations

import html
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
OUTPUT = ROOT / "search-data.js"


def strip_markup(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def read_meta(text: str, name: str) -> str:
    match = re.search(
        rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', text, re.I
    )
    return html.unescape(match.group(1)).strip() if match else ""


def read_title(text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    return strip_markup(match.group(1)).split("｜", 1)[0] if match else ""


def add_page(entries: list[dict], path: str, kind: str, extra: str = "") -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    entries.append(
        {
            "title": read_title(text),
            "url": path,
            "type": kind,
            "summary": read_meta(text, "description"),
            "keywords": f'{read_meta(text, "keywords")} {extra}'.strip(),
        }
    )


def build() -> list[dict]:
    entries: list[dict] = []

    main_pages = [
        ("index.html", "主要頁面", "首頁 安隆工程 安隆居家 安全網"),
        ("products.html", "產品總覽", "產品 型錄 工程 居家"),
        ("cases.html", "案例總覽", "施工 實績 工程 案場"),
        ("cases-gallery.html", "案例圖庫", "照片 相簿 學校 社區 工廠 政府"),
        ("blog.html", "文章總覽", "安全知識 指南 規範 價格"),
        ("about.html", "主要頁面", "公司 介紹 認證 保固 駐點"),
        ("contact.html", "主要頁面", "聯絡 電話 LINE 免費估價 高雄 台中 新竹 桃園 台北 新北"),
        ("service-areas/index.html", "地區服務", "服務地區 台北 新北 高雄 新竹 竹北 桃園 安全網 工程實績"),
        ("service-areas/taipei-safety-net.html", "地區服務", "台北 臺北 新北 安全網 防護網 防墜網 樓梯 工地 學校 公共工程 免費估價"),
        ("service-areas/kaohsiung-safety-net.html", "地區服務", "高雄 大寮 大社 燕巢 鳥松 安全網 工地 廠房 樓梯 防鳥 校園"),
        ("service-areas/hsinchu-zhubei-safety-net.html", "地區服務", "新竹 竹北 湖口 安全網 天井 樓梯 學校 商場 工地"),
        ("service-areas/taoyuan-safety-net.html", "地區服務", "桃園 蘆竹 安全網 外牆 防磁磚 樓梯 工地 體育場 幼兒園"),
    ]
    for path, kind, extra in main_pages:
        add_page(entries, path, kind, extra)

    for path in sorted((ROOT / "products").rglob("*.html")):
        add_page(entries, path.relative_to(ROOT).as_posix(), "產品")

    for path in sorted((ROOT / "blog").glob("*.html")):
        if path.name != "_template.html":
            add_page(entries, path.relative_to(ROOT).as_posix(), "文章")

    for path in sorted((ROOT / "cases").glob("*.html")):
        add_page(entries, path.relative_to(ROOT).as_posix(), "精選案例")

    faq_text = (ROOT / "faq.html").read_text(encoding="utf-8")
    faq_blocks = re.findall(
        r'<details class="faq-item" id="([^"]+)">\s*<summary>(.*?)</summary>\s*<div[^>]*>(.*?)</div>\s*</details>',
        faq_text,
        re.I | re.S,
    )
    for anchor, question, answer in faq_blocks:
        entries.append(
            {
                "title": strip_markup(question),
                "url": f"faq.html#{anchor}",
                "type": "常見問題",
                "summary": strip_markup(answer),
                "keywords": "FAQ 問題 解答 安全網",
            }
        )

    gallery_text = (ROOT / "cases-gallery.html").read_text(encoding="utf-8")
    gallery_match = re.search(r"const GALLERY = (\[.*?\]);", gallery_text, re.S)
    if gallery_match:
        categories = {
            "edu": "學校 教育 幼兒園 國小 國中 高中 大學",
            "community": "社區 住宅 大樓",
            "factory": "工廠 廠房 工業",
            "gov": "政府 公共工程 機關",
            "commercial": "商業 休閒 球場 飯店",
            "other": "其他工程",
        }
        for index, case in enumerate(json.loads(gallery_match.group(1))):
            category = categories.get(case.get("cat", ""), "施工案例")
            entries.append(
                {
                    "title": case["name"],
                    "url": f"cases-gallery.html?case={index}",
                    "type": "案例圖庫",
                    "summary": f'{category}，共 {len(case.get("photos", []))} 張施工照片。',
                    "keywords": f"{category} 安全網 施工 實績 案例",
                }
            )

    return entries


def main() -> None:
    entries = build()
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    content = (
        "(function(){\n"
        '  "use strict";\n'
        "  var source=document.currentScript;\n"
        "  window.ANLONG_SEARCH_ROOT=new URL('.',source.src).href;\n"
        f"  window.ANLONG_SEARCH_INDEX={payload};\n"
        "})();\n"
    )
    OUTPUT.write_text(content, encoding="utf-8", newline="\n")
    print(f"search-data.js generated ({len(entries)} entries, {len(content.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
