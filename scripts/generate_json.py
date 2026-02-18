#!/usr/bin/env python3
"""
Generate static JSON files from markdown documentation.
Extracts YAML front matter and converts markdown content to HTML.
Creates structured JSON files organized by category for easy UI consumption.
"""

import os
import json
import yaml
import re
from pathlib import Path
from datetime import datetime
from markdown_it import MarkdownIt

# Base paths
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_DIR = BASE_DIR / "data"

# Category mappings from folder names to readable names
CATEGORY_MAP = {
    "01_introduction": {
        "id": "introduction",
        "name": "Introduction",
        "description": "Vision, mission, and leadership guidance for the pageant ministry",
        "icon": "🎯"
    },
    "02_roles": {
        "id": "roles",
        "name": "Roles & Teams",
        "description": "Responsibilities and expectations for all cast and crew members",
        "icon": "👥"
    },
    "03_basics": {
        "id": "basics",
        "name": "Stage Basics",
        "description": "Core skills and principles: blocking, projection, choreography, expression",
        "icon": "🎬"
    },
    "04_rehearsal": {
        "id": "rehearsal",
        "name": "Rehearsals",
        "description": "Etiquette, communication, devotionals, preparation, and scheduling",
        "icon": "🕓"
    },
    "05_production": {
        "id": "production",
        "name": "Production",
        "description": "Technical and backstage operations: lighting, cues, sound, and props",
        "icon": "💡"
    },
    "06_ministry": {
        "id": "ministry",
        "name": "Ministry & Leadership",
        "description": "Theology of art, servant leadership, sustainability, and church alignment",
        "icon": "🙏"
    },
    "07_glossary": {
        "id": "glossary",
        "name": "Reference & Glossary",
        "description": "Checklists, templates, feedback forms, and version history",
        "icon": "🧾"
    }
}

# Initialize markdown renderer with table support
md = MarkdownIt().enable('table')


def extract_frontmatter_and_content(file_path):
    """Extract YAML front matter and markdown content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML front matter
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            markdown_content = match.group(2).strip()
            return frontmatter, markdown_content
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return {}, content
    
    # No front matter found
    return {}, content


def extract_scripture_quote(content):
    """Extract the first scripture quote from content if present."""
    # Look for pattern: > "text" — *reference*
    pattern = r'>\s*"([^"]+)"\s*[-—]\s*[*_]([^*_]+)[*_]'
    match = re.search(pattern, content)
    if match:
        return {
            "text": match.group(1),
            "reference": match.group(2)
        }
    return None


def process_markdown_file(file_path, category_info):
    """Process a single markdown file and return structured data."""
    frontmatter, content = extract_frontmatter_and_content(file_path)
    
    # Extract filename without extension
    filename = file_path.stem
    
    # Skip index files (they're navigation only)
    if filename == "index":
        return None
    
    # Convert markdown content to HTML and remove newlines
    html_content = md.render(content).replace('\n', '')
    
    # Build the document object
    doc = {
        "filename": filename,
        "id": frontmatter.get("id", f"{category_info['id']}/{filename}"),
        "title": filename.replace("-", " ").title(),
        "category": frontmatter.get("category", category_info["name"]),
        "summary": frontmatter.get("summary", ""),
        "tags": frontmatter.get("tags", []),
        "audience": frontmatter.get("audience", []),
        "content": html_content,
        "metadata": {}
    }
    
    # Add optional fields
    if "scriptural_reference" in frontmatter:
        doc["scriptural_reference"] = frontmatter["scriptural_reference"]
    
    if "related" in frontmatter:
        doc["related"] = frontmatter["related"]
    
    # Extract scripture quote from content if present
    scripture_quote = extract_scripture_quote(content)
    if scripture_quote:
        doc["scripture_quote"] = scripture_quote
    
    # Add metadata
    if "last_updated" in frontmatter:
        doc["metadata"]["last_updated"] = str(frontmatter["last_updated"])
    
    if "author" in frontmatter:
        doc["metadata"]["author"] = frontmatter["author"]
    
    return doc


def process_category(category_folder, category_info):
    """Process all markdown files in a category folder."""
    folder_path = DOCS_DIR / category_folder
    
    if not folder_path.exists():
        print(f"Warning: Category folder {category_folder} not found")
        return None
    
    documents = []
    
    # Create output subdirectory mirroring docs structure
    category_output_dir = OUTPUT_DIR / category_folder
    category_output_dir.mkdir(exist_ok=True)
    
    # Process all .md files
    for md_file in sorted(folder_path.glob("*.md")):
        doc = process_markdown_file(md_file, category_info)
        if doc:  # Skip None results (e.g., index files)
            documents.append(doc)
            
            # Write individual JSON file
            individual_file = category_output_dir / f"{md_file.stem}.json"
            with open(individual_file, 'w', encoding='utf-8') as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
    
    # Build category JSON structure
    category_data = {
        "id": category_info["id"],
        "name": category_info["name"],
        "description": category_info["description"],
        "icon": category_info["icon"],
        "document_count": len(documents),
        "documents": documents
    }
    
    return category_data


def generate_master_index(categories_data):
    """Generate a master index with navigation structure."""
    index = {
        "metadata": {
            "title": "EASTER - Church Stage Performance Knowledge",
            "description": "A structured, ministry-aligned documentation system for church productions and pageants",
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "repository": "https://github.com/D7460N/EASTER"
        },
        "categories": [],
        "statistics": {
            "total_categories": 0,
            "total_documents": 0,
            "total_tags": set()
        }
    }
    
    for cat_data in categories_data:
        if cat_data:
            # Add to categories list
            index["categories"].append({
                "id": cat_data["id"],
                "name": cat_data["name"],
                "description": cat_data["description"],
                "icon": cat_data["icon"],
                "document_count": cat_data["document_count"],
                "data_file": f"{cat_data['id']}.json"
            })
            
            # Update statistics
            index["statistics"]["total_categories"] += 1
            index["statistics"]["total_documents"] += cat_data["document_count"]
            
            # Collect all tags
            for doc in cat_data["documents"]:
                index["statistics"]["total_tags"].update(doc.get("tags", []))
    
    # Convert set to sorted list
    index["statistics"]["total_tags"] = sorted(list(index["statistics"]["total_tags"]))
    
    return index


def main():
    """Main execution function."""
    print("🎭 EASTER Documentation → JSON Generator")
    print("=" * 50)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")
    
    categories_data = []
    
    # Process each category
    total_individual_files = 0
    for folder_name, category_info in CATEGORY_MAP.items():
        print(f"\n📁 Processing: {category_info['name']}...")
        category_data = process_category(folder_name, category_info)
        
        if category_data:
            categories_data.append(category_data)
            
            # Write category JSON file
            output_file = OUTPUT_DIR / f"{category_info['id']}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(category_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✓ Generated category file: {output_file.name}")
            print(f"   ✓ Generated individual files: {category_data['document_count']}")
            print(f"   ✓ Location: {OUTPUT_DIR / folder_name}/")
            total_individual_files += category_data['document_count']
    
    # Generate master index
    print(f"\n📋 Generating master index...")
    master_index = generate_master_index(categories_data)
    
    index_file = OUTPUT_DIR / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(master_index, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Generated: {index_file.name}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("✨ Generation Complete!")
    print(f"   Categories: {master_index['statistics']['total_categories']}")
    print(f"   Documents: {master_index['statistics']['total_documents']}")
    print(f"   Category JSON files: {master_index['statistics']['total_categories']}")
    print(f"   Individual JSON files: {total_individual_files}")
    print(f"   Tags: {len(master_index['statistics']['total_tags'])}")
    print(f"\n📂 JSON files available in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
