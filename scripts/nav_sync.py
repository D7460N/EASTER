#!/usr/bin/env python3
import re, os, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root
DOCS = ROOT / "docs"

# ---- Helpers ---------------------------------------------------------------

def list_markdown_files(folder: Path):
    return sorted([p for p in folder.glob("*.md") if p.name.lower() != "readme.md"])

def human_title(filename: str) -> str:
    # "stage-directions.md" -> "Stage Directions"
    base = filename.rsplit(".", 1)[0]
    return " ".join([w.capitalize() for w in base.replace("_", "-").split("-")])

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_if_changed(path: Path, new_content: str):
    old = read(path)
    if old != new_content:
        path.write_text(new_content, encoding="utf-8")
        print(f"Updated: {path}")
    else:
        print(f"No change: {path}")

def replace_between_markers(text: str, start_marker: str, end_marker: str, new_block: str):
    pattern = re.compile(
        rf"({re.escape(start_marker)})(.*?){re.escape(end_marker)}",
        re.DOTALL
    )
    if pattern.search(text):
        return pattern.sub(rf"\1\n{new_block}\n{end_marker}", text)
    # If markers missing, append at top under title
    lines = text.splitlines()
    # Insert after first H1 if present
    insert_idx = 0
    for i, line in enumerate(lines[:10]):
        if line.strip().startswith("# "):
            insert_idx = i + 1
            break
    lines.insert(insert_idx, f"{start_marker}\n{new_block}\n{end_marker}")
    return "\n".join(lines)

# ---- Root Quick Navigation -------------------------------------------------

ROOT_START = "<!-- NAV:START -->"
ROOT_END   = "<!-- NAV:END -->"

def build_root_quick_nav():
    # Known sections map: { folder: (emoji, label, key_links) }
    sections = [
        ("01_introduction", "🎯 **Introduction**", "vision.md"),
        ("02_roles",        "👥 **Roles & Teams**", "director.md / producer.md"),
        ("03_basics",       "🎬 **Stage Basics**", ""),
        ("04_rehearsal",    "🕓 **Rehearsals**", "schedule.md"),
        ("05_production",   "💡 **Production**", ""),
        ("06_ministry",     "🙏 **Ministry & Leadership**", "purpose.md"),
        ("07_glossary",     "🧾 **Reference & Glossary**", "")
    ]
    rows = []
    for folder, label, highlight in sections:
        path = f"./docs/{folder}/"
        key = f" → [{highlight}]({path}{highlight})" if highlight else ""
        rows.append(f"| {label} | {folder.replace('_',' ').replace('01','').strip()} | [{folder}]({path}){key} |")
    rows.insert(0, "| Section | Description | Key Links |")
    rows.insert(1, "|----------|--------------|-----------|")
    return "\n".join(rows)

def sync_root_readme():
    readme = ROOT / "README.md"
    if not readme.exists():
        print("ERROR: README.md not found at repo root.")
        sys.exit(1)
    content = read(readme)
    new_table = build_root_quick_nav()
    updated = replace_between_markers(content, ROOT_START, ROOT_END, new_table)
    write_if_changed(readme, updated)

# ---- Section READMEs -------------------------------------------------------

def build_section_table(section_dir: Path):
    files = list_markdown_files(section_dir)
    rows = ["| File | Focus | Description |",
            "|------|--------|-------------|"]
    for f in files:
        title = human_title(f.name)
        # Try to read first H1 or summary from YAML front matter
        focus = title
        desc = ""
        text = read(f)
        if text.startswith("---"):
            # Extract YAML front matter
            try:
                fm_end = text.find("\n---", 3)
                if fm_end != -1:
                    fm = yaml.safe_load(text[3:fm_end])
                    if isinstance(fm, dict):
                        focus = fm.get("summary", focus)
            except Exception:
                pass
        rows.append(f"| [{f.name}](./{f.name}) | {title} | {focus} |")
    return "\n".join(rows)

SECTION_INTROS = {
    "01_introduction": "This section outlines the vision, mission, and theological foundation for the Church Stage Performance Ministry.",
    "02_roles": "This section defines every volunteer and staff role within the stage and production ministry — from direction and design to music, tech, and support.",
    "03_basics": "This section covers the foundational skills of stage ministry — movement, expression, voice, and presence.",
    "04_rehearsal": "Rehearsal is where ministry takes shape — a sacred rhythm of preparation, prayer, and unity.",
    "05_production": "This section manages everything behind the scenes — lighting, sound, props, cues, and backstage operations.",
    "06_ministry": "The heart of all creative work is ministry — service offered in love, grounded in Scripture.",
    "07_glossary": "This section collects tools and references that support smooth ministry operation — checklists, forms, templates, and logs."
}

def ensure_section_readmes():
    for section in sorted(p for p in DOCS.iterdir() if p.is_dir()):
        readme = section / "README.md"
        intro = SECTION_INTROS.get(section.name, "Section overview.")
        table = build_section_table(section)
        body = f"# {section.name.replace('_',' ').replace('0','',1).title()} Overview\n\n{intro}\n\n{table}\n"
        if not readme.exists():
            write_if_changed(readme, body)
        else:
            # Replace table only (after the first blank line); keep custom notes if any
            existing = read(readme)
            if "| File | Focus | Description |" in existing:
                head, _sep, _rest = existing.partition("| File | Focus | Description |")
                new_content = head.rstrip() + "\n\n" + table + "\n"
                write_if_changed(readme, new_content)
            else:
                # Append table if no table is found
                new_content = existing.rstrip() + "\n\n" + table + "\n"
                write_if_changed(readme, new_content)

def main():
    sync_root_readme()
    ensure_section_readmes()

if __name__ == "__main__":
    main()
