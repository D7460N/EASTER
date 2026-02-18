# 📊 EASTER Knowledge Base - JSON Data Files

This directory contains static JSON files generated from the EASTER repository's markdown documentation. These files provide structured, easily accessible content for building user interfaces, APIs, or other applications.

## 🗂️ File Structure

### Master Index
- **`index.json`** - Central navigation file containing:
  - Metadata about the entire knowledge base
  - List of all categories with descriptions
  - Statistics (total documents, tags, categories)
  - References to individual category JSON files

### Category Files
Each category has its own JSON file with complete content:

| File | Category | Icon | Documents |
|------|----------|------|-----------|
| `introduction.json` | Introduction | 🎯 | Vision, mission, leadership guidance |
| `roles.json` | Roles & Teams | 👥 | All cast and crew responsibilities |
| `basics.json` | Stage Basics | 🎬 | Core skills: blocking, projection, choreography |
| `rehearsal.json` | Rehearsals | 🕓 | Etiquette, communication, scheduling |
| `production.json` | Production | 💡 | Technical operations, lighting, sound, props |
| `ministry.json` | Ministry & Leadership | 🙏 | Theology, servant leadership, sustainability |
| `glossary.json` | Reference & Glossary | 🧾 | Checklists, templates, feedback forms |

### Individual Document Files
Each document also has its own JSON file, organized in subdirectories mirroring the `/docs` structure:

| Directory | Files | Example |
|-----------|-------|---------|
| `01_introduction/` | 3 files | `vision.json`, `leadership-brief.json` |
| `02_roles/` | 9 files | `actors.json`, `director.json` |
| `03_basics/` | 5 files | `blocking.json`, `projection.json` |
| `04_rehearsal/` | 5 files | `etiquette.json`, `schedule.json` |
| `05_production/` | 8 files | `lighting.json`, `sound.json` |
| `06_ministry/` | 5 files | `purpose.json`, `servant-leadership.json` |
| `07_glossary/` | 4 files | `checklists.json`, `templates.json` |

**Total: 39 individual JSON files** - Each contains complete document metadata and content, ready for direct API consumption.

## 📋 JSON Structure

### Master Index (`index.json`)
```json
{
  "metadata": {
    "title": "EASTER - Church Stage Performance Knowledge",
    "description": "...",
    "version": "1.0.0",
    "generated": "2026-02-09T...",
    "repository": "https://github.com/D7460N/EASTER"
  },
  "categories": [
    {
      "id": "introduction",
      "name": "Introduction",
      "description": "...",
      "icon": "🎯",
      "document_count": 3,
      "data_file": "introduction.json"
    }
  ],
  "statistics": {
    "total_categories": 7,
    "total_documents": 39,
    "total_tags": ["acting", "blocking", "communication", ...]
  }
}
```

### Category Files (e.g., `introduction.json`)
```json
{
  "id": "introduction",
  "name": "Introduction",
  "description": "...",
  "icon": "🎯",
  "document_count": 3,
  "documents": [
    {
      "filename": "vision",
      "id": "intro/vision",
      "title": "Vision",
      "category": "Introduction",
      "summary": "Purpose and vision behind church stage productions.",
      "tags": ["purpose", "ministry", "overview"],
      "audience": ["leadership", "volunteers"],
      "content": "<blockquote>\n<p>\"Whatever you do, work heartily...\"</p>\n</blockquote>\n<h1>Vision and Purpose</h1>\n<p>Every performance we create is a ministry...</p>",
      "scriptural_reference": "Colossians 3:23",
      "scripture_quote": {
        "text": "Whatever you do, work heartily...",
        "reference": "Colossians 3:23"
      },
      "related": ["intro/leadership-brief", "ministry/purpose"],
      "metadata": {
        "last_updated": "2025-11-05",
        "author": "..."
      }
    }
  ]
}
```

### Individual Document Files (e.g., `01_introduction/vision.json`)
```json
{
  "filename": "vision",
  "id": "intro/vision",
  "title": "Vision",
  "category": "Introduction",
  "summary": "Purpose and vision behind church stage productions.",
  "tags": ["purpose", "ministry", "overview"],
  "audience": ["leadership", "volunteers"],
  "content": "<blockquote>\n<p>\"Whatever you do, work heartily...\"</p>\n</blockquote>\n<h1>Vision and Purpose</h1>\n<p>Every performance we create is a ministry...</p>",
  "metadata": {}
}
```

## 🔑 Key Fields

### Document Object
- **`filename`** - Original markdown filename (without extension)
- **`id`** - Unique identifier for cross-referencing (e.g., "intro/vision")
- **`title`** - Human-readable title
- **`category`** - Category name
- **`summary`** - One-sentence description
- **`tags`** - Array of keywords for filtering/searching
- **`audience`** - Target audience (director, actor, tech, etc.)
- **`content`** - HTML content converted from markdown
- **`scriptural_reference`** - Bible reference (if applicable)
- **`scripture_quote`** - Extracted opening quote with text and reference
- **`related`** - Array of related document IDs
- **`metadata`** - Additional info (last_updated, author)

## 🚀 Usage Examples

### Loading the Master Index
```javascript
// Fetch the master index
fetch('/data/index.json')
  .then(res => res.json())
  .then(index => {
    console.log(`Total categories: ${index.statistics.total_categories}`);
    console.log(`Total documents: ${index.statistics.total_documents}`);
    
    // Display categories
    index.categories.forEach(cat => {
      console.log(`${cat.icon} ${cat.name}: ${cat.document_count} docs`);
    });
  });
```

### Loading a Category
```javascript
// Fetch a specific category
fetch('/data/introduction.json')
  .then(res => res.json())
  .then(category => {
    console.log(`Category: ${category.name}`);
    console.log(`Documents: ${category.document_count}`);
    
    // Display documents
    category.documents.forEach(doc => {
      console.log(`- ${doc.title}: ${doc.summary}`);
    });
  });
```

### Loading an Individual Document
```javascript
// Fetch a specific document directly
fetch('/data/01_introduction/vision.json')
  .then(res => res.json())
  .then(doc => {
    console.log(`Title: ${doc.title}`);
    console.log(`Summary: ${doc.summary}`);
    console.log(`Content: ${doc.content}`);
    
    // Content is already HTML - just insert it
    document.getElementById('content').innerHTML = doc.content;
  });
```

### Dynamic Document Loading (e.g., via oninput)
```javascript
// Load document based on user selection
function loadDocument(category, filename) {
  fetch(`/data/${category}/${filename}.json`)
    .then(res => res.json())
    .then(doc => {
      // Update UI with document content (already HTML)
      document.getElementById('title').textContent = doc.title;
      document.getElementById('summary').textContent = doc.summary;
      document.getElementById('content').innerHTML = doc.content;
    });
}

// Example: triggered by input event
document.querySelector('select').oninput = (e) => {
  const [category, filename] = e.target.value.split('/');
  loadDocument(category, filename);
};
```

### Searching by Tag
```javascript
// Load all categories and filter by tag
Promise.all([
  fetch('/data/introduction.json').then(r => r.json()),
  fetch('/data/roles.json').then(r => r.json()),
  // ... load other categories
]).then(categories => {
  // Find all documents tagged with "leadership"
  const leadershipDocs = categories.flatMap(cat => 
    cat.documents.filter(doc => doc.tags.includes('leadership'))
  );
  
  console.log(`Found ${leadershipDocs.length} leadership documents`);
});
```

### Filtering by Audience
```javascript
// Find all content for directors
fetch('/data/index.json')
  .then(res => res.json())
  .then(async index => {
    // Load all category files
    const categories = await Promise.all(
      index.categories.map(cat => 
        fetch(`/data/${cat.data_file}`).then(r => r.json())
      )
    );
    
    // Filter documents for directors
    const directorDocs = categories.flatMap(cat =>
      cat.documents.filter(doc => 
        doc.audience.includes('director')
      )
    );
    
    console.log(`Director resources: ${directorDocs.length}`);
  });
```

## 🔄 Regenerating JSON Files

To regenerate the JSON files after updating markdown documentation:

```bash
python3 scripts/generate_json.py
```

This will:
1. Parse all markdown files in `/docs`
2. Extract YAML front matter and content
3. Generate category JSON files
4. Update the master index
5. Output files to `/data` directory

## 📚 Integration Ideas

### Static Site Generator
- Use as data source for Jekyll, Hugo, or Next.js
- Build navigation from `index.json`
- Render content from category files

### API Backend
- Serve JSON files directly via CDN
- No database needed - just static files
- Fast, cacheable, and scalable

### Search Interface
- Build client-side search using tags and summaries
- Filter by category, audience, or scripture reference
- Implement fuzzy search on content

### Mobile App
- Bundle JSON files with app
- Offline-first content access
- Sync updates periodically

### AI/MCP Integration
- Use JSON as structured context for AI agents
- Enable semantic search and Q&A
- Cross-reference related topics automatically

## 📖 Schema Reference

For detailed schema information, see:
- **`/schema.yaml`** - Metadata field definitions
- **`/manifest.json`** - MCP server configuration

## 📜 License

Content is licensed under CC BY-NC-SA 4.0.
See `/LICENSE` for details.

---

**Generated:** Auto-generated from markdown files  
**Maintained by:** EASTER Knowledge Base Team  
**Repository:** https://github.com/D7460N/EASTER
