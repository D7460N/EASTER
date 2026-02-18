# EASTER Knowledge Base - D7460N Architecture

This application follows the D7460N Architecture principles:

- **CSS-first**: All UI logic, state management, and styling handled by CSS
- **Zero-dependency**: No frameworks, no libraries
- **JAMstack**: Static files served, API data injected
- **Semantic HTML**: Structure equals meaning
- **Browser-native**: Modern CSS and vanilla JavaScript only

## File Structure

```
/
├── index.html              # Root HTML file with semantic empty tags
├── manifest.json           # PWA manifest
├── assets/
│   ├── css/
│   │   └── layout.css     # All layout and UI styling (Holy Grail grid)
│   ├── js/
│   │   └── app.js         # Data transport only - CRUD operations
│   └── data/
│       ├── introduction.json
│       ├── roles.json
│       ├── basics.json
│       ├── rehearsal.json
│       ├── production.json
│       ├── ministry.json
│       └── glossary.json
└── data/                  # Original markdown source data
```

## Architecture Principles

### HTML
- Semantic elements only (`<app-container>`, `<app-logo>`, etc.)
- No classes, IDs, or `data-*` attributes (except for functional needs like `data-id`)
- No inline styles or scripts
- Custom elements act as semantic containers

### CSS
- All UI logic lives in CSS
- `:has()`, `:checked`, `:empty`, `:valid` for state management
- Hidden checkboxes/radio inputs act as CSS state machines
- CSS Grid for all layout (no Flexbox)
- Holy Grail layout pattern via `<app-container>`

### JavaScript
- **CRUD operations and data transport ONLY**
- `fetch()` to load JSON data
- Inject content into empty semantic tags
- `oninput` event handler (not `onclick` or event listeners)
- Idempotent and stateless functions
- No DOM styling, UI logic, or global state

## How It Works

1. **Page Load**: `index.html` loads with empty semantic tags
2. **Navigation**: Radio buttons (hidden) trigger category loading via `oninput`
3. **Data Fetch**: JavaScript fetches JSON from `/assets/data/`
4. **Data Injection**: JavaScript injects data into empty tags
5. **UI State**: CSS manages all visual state using `:checked`, `:has()`, etc.
6. **Document Detail**: Click on list item shows detail in `<aside>`

## Key Patterns

### Navigation State
```html
<label>
  Introduction
  <input type="radio" name="nav" value="introduction" checked>
</label>
```
- Hidden radio button (`aria-hidden="true"`)
- CSS uses `:checked` to style active nav
- JavaScript uses `oninput` to load data

### Document List
```html
<app-document-list>
  <ol></ol>
</app-document-list>
```
- JavaScript injects `<li>` elements with document data
- Each `<li>` has semantic child elements (`<document-title>`, etc.)
- CSS styles based on structure, not classes

### Document Detail
```html
<aside>
  <app-document-detail>
    <app-document-title></app-document-title>
    <app-document-content></app-document-content>
  </app-document-detail>
</aside>
```
- Aside hidden by default (`display: none`)
- CSS shows when title is not empty: `aside:has(app-document-title:not(:empty))`
- JavaScript injects HTML content from JSON

## JSON Data Format

Each category JSON file contains:

```json
{
  "id": "category-id",
  "name": "Category Name",
  "description": "Category description",
  "icon": "🎯",
  "document_count": 3,
  "documents": [
    {
      "id": "doc-id",
      "title": "Document Title",
      "category": "Category",
      "summary": "Brief summary",
      "tags": ["tag1", "tag2"],
      "audience": ["audience1"],
      "content": "<h1>HTML Content</h1><p>...</p>"
    }
  ]
}
```

## Development

To run locally:

```bash
# Start a simple HTTP server
python3 -m http.server 8000

# Or use any other static file server
npx serve
```

Navigate to `http://localhost:8000`

## Why This Architecture?

1. **Performance**: CSS is 100-1000× faster than JavaScript for UI
2. **Security**: Minimal JavaScript attack surface
3. **Accessibility**: Semantic HTML with proper ARIA
4. **Maintainability**: Clear separation of concerns
5. **Progressive Enhancement**: Works without JavaScript for basic content
6. **No Build Step**: Direct deployment, no transpilation needed

## References

- [D7460N Starter Repository](https://github.com/D7460N/starter)
- D7460N Architecture documentation in starter repo
