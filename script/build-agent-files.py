#!/usr/bin/env python3
"""Write the agent-readable files for pmintheloop.com.

Reads the Second Brain essays, the workplace fiction, and the chapter files,
then writes llms.txt, llms-full.txt, index.md, and a raw markdown mirror for
every essay that Jekyll would otherwise publish only as HTML.

Run from the repo root after adding or editing an essay:

    python3 script/build-agent-files.py
"""

from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://pmintheloop.com"
AGENT = ROOT / "agent"

SECOND_BRAIN_WRITERS = "Siddharth Saoji and Sriram Iyer"
FICTION_WRITERS = "Manas Sharma, Siddharth Saoji, and Sanskriti Uma"


def split_front_matter(text):
    if not text.startswith("---"):
        return {}, text.lstrip("\n")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text.lstrip("\n")
    meta = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, parts[2].lstrip("\n")


def heading(text):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def mirror_page(permalink, body):
    return (
        "---\n"
        "layout: null\n"
        f"permalink: {permalink}\n"
        "sitemap: false\n"
        "---\n"
        "{% raw %}\n"
        f"{body.rstrip()}\n"
        "{% endraw %}\n"
    )


def main():
    essays = []
    for path in sorted((ROOT / "_second_brain").glob("*.md")):
        meta, body = split_front_matter(path.read_text())
        essays.append(
            {
                "title": meta["title"],
                "dek": meta.get("dek", ""),
                "date": meta.get("date", ""),
                "slug": path.stem,
                "body": body,
                "writers": SECOND_BRAIN_WRITERS,
                "section": "Second Brain",
            }
        )
    essays.sort(key=lambda item: item["date"], reverse=True)

    archive_meta, archive_body = split_front_matter((ROOT / "archive.md").read_text())
    fiction = {
        "title": archive_meta["title"],
        "dek": archive_meta.get("dek", ""),
        "date": archive_meta.get("date", ""),
        "slug": "archive",
        "body": archive_body,
        "writers": FICTION_WRITERS,
        "section": "Workplace Fiction",
    }

    chapters = []
    for path in sorted(ROOT.glob("chapter*.md"), key=lambda p: int(re.search(r"\d+", p.stem).group())):
        text = path.read_text()
        chapters.append({"title": heading(text), "slug": path.stem, "body": text})

    about = (ROOT / "about.md").read_text().strip() + "\n"

    if AGENT.exists():
        shutil.rmtree(AGENT)
    AGENT.mkdir()

    for item in essays + [fiction]:
        (AGENT / f"{item['slug']}.html").write_text(
            mirror_page(f"/{item['slug']}.md", item["body"])
        )

    lines = [
        "# PM in the Loop",
        "",
        "> Musings of becoming and staying an AI product manager.",
        "",
        "Essays are available as clean markdown by replacing `.html` with `.md`. "
        f"The full text of the essays and the workplace fiction is at {SITE}/llms-full.txt.",
        "",
        "## Second Brain",
        "",
        f"A series on the context layer an AI agent needs. Writers: {SECOND_BRAIN_WRITERS}. "
        f"Series page: {SITE}/second-brain/",
        "",
    ]
    for item in essays:
        lines.append(f"- [{item['title']}]({SITE}/{item['slug']}.md): {item['dek']}")
    lines.extend(
        [
            "",
            "## Workplace Fiction",
            "",
            f"A story about product management in the age of AI. Writers: {FICTION_WRITERS}.",
            "",
            f"- [{fiction['title']}]({SITE}/archive.md): {fiction['dek']}",
        ]
    )
    for chapter in chapters:
        lines.append(
            f"- [{chapter['title']}]({SITE}/{chapter['slug']}.md): A chapter of the workplace fiction."
        )
    lines.extend(
        [
            "",
            "## About",
            "",
            f"- [About the Author]({SITE}/about.md): Manas Sharma and Siddharth Saoji.",
            "",
        ]
    )
    (ROOT / "llms.txt").write_text("\n".join(lines))

    full = [
        "# PM in the Loop — Full Content",
        "",
        "> Musings of becoming and staying an AI product manager.",
        "",
        "This file contains the Second Brain essays and the workplace fiction. "
        f"Individual chapters are also at {SITE}/chapter1.md through {SITE}/chapter7.md.",
        "",
        "---",
        "",
    ]
    for item in essays + [fiction]:
        full.extend(
            [
                f"## {item['title']}",
                "",
                f"- URL: {SITE}/{item['slug']}.html",
                f"- Markdown: {SITE}/{item['slug']}.md",
            ]
        )
        if item["date"]:
            full.append(f"- Date: {item['date']}")
        full.extend(
            [
                f"- Writers: {item['writers']}",
                f"- Description: {item['dek']}",
                "",
                item["body"].rstrip(),
                "",
                "---",
                "",
            ]
        )
    full.extend(["## About the Author", "", f"- URL: {SITE}/about.html", f"- Markdown: {SITE}/about.md", "", about])
    (ROOT / "llms-full.txt").write_text("\n".join(full).rstrip() + "\n")

    index = [
        "# PM in the Loop",
        "",
        "Musings of becoming and staying an AI product manager.",
        "",
        f"Agent catalog: {SITE}/llms.txt",
        f"Full text: {SITE}/llms-full.txt",
        "",
        "## Second Brain",
        "",
        f"Writers: {SECOND_BRAIN_WRITERS}. Series page: {SITE}/second-brain/",
        "",
    ]
    for item in essays:
        index.append(f"- [{item['title']}]({SITE}/{item['slug']}.md): {item['dek']}")
    index.extend(
        [
            "",
            "## Workplace Fiction",
            "",
            f"Writers: {FICTION_WRITERS}.",
            "",
            f"- [{fiction['title']}]({SITE}/archive.md): {fiction['dek']}",
            "",
        ]
    )
    (AGENT / "index.html").write_text(mirror_page("/index.md", "\n".join(index).rstrip() + "\n"))
    print(f"wrote llms.txt, llms-full.txt, and {len(list(AGENT.glob('*.html')))} markdown mirrors")


if __name__ == "__main__":
    main()
