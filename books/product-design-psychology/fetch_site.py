#!/usr/bin/env python3
"""productdesignpsychology.com → manuscript/*.md + assets/ 다운로더.

개인 학습용 편집본 생성 스크립트. 원문 저작권은 Wouter de Bres에게 있음.
재실행 시 변경된 챕터만 다시 쓴다(내용 비교).
"""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

from lxml import html as lhtml

BASE = "https://productdesignpsychology.com"
BOOK = Path(__file__).resolve().parent
MANUSCRIPT = BOOK / "manuscript-en"
ASSETS = BOOK / "assets"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) KLIC-BOOK personal-archive"}
SKIP_TAGS = ("svg", "path", "script", "style")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()


def chapter_urls() -> list[str]:
    """홈페이지에서 /NN-slug/ 링크를 추출해 정렬 목록 반환."""
    root = lhtml.fromstring(fetch(BASE + "/"))
    slugs = set()
    for href in root.xpath("//a/@href"):
        m = re.match(r"^/(\d{2}-[a-z0-9-]+)/?$", href)
        if m:
            slugs.add(m.group(1))
    return sorted(slugs)


def strip_md(elem) -> str:
    """태그 제거한 순수 텍스트."""
    return re.sub(r"\s+", " ", elem.text_content() or "").strip()


def md_inline(elem) -> str:
    """요소 내부를 markdown 인라인으로 직렬화(strong/em/a/br)."""
    out: list[str] = []

    def emit(text: str) -> None:
        out.append(re.sub(r"\s+", " ", text) if text else "")

    def walk(node) -> None:
        emit(node.text)
        for child in node:
            tag = child.tag if isinstance(child.tag, str) else ""
            if tag == "strong":
                out.append(f"**{strip_md(child)}**")
            elif tag == "em":
                out.append(f"*{strip_md(child)}*")
            elif tag == "a":
                href = child.get("href") or ""
                seg = strip_md(child)
                out.append(f"[{seg}]({href})" if href else seg)
            elif tag == "br":
                out.append("\n")
            elif tag not in SKIP_TAGS:
                walk(child)
            emit(child.tail)

    walk(elem)
    text = "".join(out)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def download_asset(src: str) -> str:
    name = src.rsplit("/", 1)[-1]
    dst = ASSETS / name
    if not dst.exists():
        dst.write_bytes(fetch(BASE + src))
    return f"../assets/{name}"


def convert_page(slug: str) -> str:
    root = lhtml.fromstring(fetch(f"{BASE}/{slug}/"))
    h1 = root.xpath("//header/h1")
    title = strip_md(h1[0]) if h1 else slug
    label_el = root.xpath("//header//div[contains(@class,'chapter-label')]")
    label = strip_md(label_el[0]) if label_el else ""
    if label and label.lower() != title.lower():
        title = f"{label} · {title}"
    subtitle_el = root.xpath("//header//p[contains(@class,'chapter-subtitle')]")
    subtitle = strip_md(subtitle_el[0]) if subtitle_el else ""

    content = root.xpath("//div[contains(@class,'chapter-content')]")[0]
    lines: list[str] = [f"## {title}", ""]
    if subtitle:
        lines += [f"*{subtitle}*", ""]

    for el in content:
        tag = el.tag if isinstance(el.tag, str) else ""
        cls = el.get("class") or ""
        if tag == "figure":
            for img in el.xpath(".//img"):
                src = img.get("src") or ""
                if src:
                    lines += [f"![]({download_asset(src)})", ""]
        elif tag in ("h2", "h3"):
            level = "###" if tag == "h2" else "####"
            lines += [f"{level} {strip_md(el)}", ""]
        elif tag == "p":
            if "chapter-subtitle" in cls:
                continue
            seg = md_inline(el)
            if seg:
                lines += [seg, ""]
        elif tag == "blockquote":
            for p in el.xpath("./p"):
                seg = md_inline(p)
                if seg:
                    lines.append("> " + seg)
            lines.append("")
        elif tag in ("ul", "ol"):
            for li in el.xpath("./li"):
                lines.append(f"- {md_inline(li).replace(chr(10), ' ')}")
            lines.append("")

    # references 는 .chapter-content 밖 article 형제 노드에 있다.
    refs = root.xpath("//details[contains(@class,'references')]//ul/li")
    if refs:
        lines += ["### References & Sources", ""]
        for li in refs:
            lines.append(f"- {md_inline(li).replace(chr(10), ' ')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    MANUSCRIPT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    slugs = chapter_urls()
    print(f"{len(slugs)} chapters")
    for slug in slugs:
        out = MANUSCRIPT / f"{slug}.md"
        md = convert_page(slug)
        marker = "=" if (out.exists() and out.read_text(encoding="utf-8") == md) else "+"
        out.write_text(md, encoding="utf-8")
        print(f"  {marker} {out.name} ({len(md)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
