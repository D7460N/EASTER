# 🎭 Church Stage Performance Knowledge MCP
<!-- NAV:START -->
| Section | Description | Key Links |
|----------|--------------|-----------|
| 🎯 **Introduction** | introduction | [01_introduction](./docs/01_introduction/) → [vision.md](./docs/01_introduction/vision.md) |
| 👥 **Roles & Teams** | 02 roles | [02_roles](./docs/02_roles/) → [director.md / producer.md](./docs/02_roles/director.md / producer.md) |
| 🎬 **Stage Basics** | 03 basics | [03_basics](./docs/03_basics/) |
| 🕓 **Rehearsals** | 04 rehearsal | [04_rehearsal](./docs/04_rehearsal/) → [mock-schedule.md](./docs/04_rehearsal/mock-schedule.md) |
| 💡 **Production** | 05 production | [05_production](./docs/05_production/) |
| 🙏 **Ministry & Leadership** | 06 ministry | [06_ministry](./docs/06_ministry/) → [purpose.md](./docs/06_ministry/purpose.md) |
| 🧾 **Reference & Glossary** | 07 glossary | [07_glossary](./docs/07_glossary/) |
<!-- NAV:END -->

_A structured, ministry-aligned documentation and knowledge system for church productions and pageants._

---

## 📚 Quick Navigation

| Section                      | Description                                                                 | Key Links                                                                                                              |
| ---------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 🎯 **Introduction**          | Vision, mission, and leadership guidance for the pageant ministry.          | [01_introduction](./docs/01_introduction/) → [vision.md](./docs/01_introduction/vision.md)                             |
| 👥 **Roles & Teams**         | Responsibilities and expectations for all cast and crew members.            | [02_roles](./docs/02_roles/) → [director.md](./docs/02_roles/director.md) / [producer.md](./docs/02_roles/producer.md) |
| 🎬 **Stage Basics**          | Core skills and principles: blocking, projection, choreography, expression. | [03_basics](./docs/03_basics/)                                                                                         |
| 🕓 **Rehearsals**            | Etiquette, communication, devotionals, preparation, and scheduling.         | [04_rehearsal](./docs/04_rehearsal/) → [mock-schedule.md](./docs/04_rehearsal/mock-schedule.md)                        |
| 💡 **Production**            | Technical and backstage operations: lighting, cues, sound, and props.       | [05_production](./docs/05_production/)                                                                                 |
| 🙏 **Ministry & Leadership** | Theology of art, servant leadership, sustainability, and church alignment.  | [06_ministry](./docs/06_ministry/) → [purpose.md](./docs/06_ministry/purpose.md)                                       |
| 🧾 **Reference & Glossary**  | Checklists, templates, feedback forms, and version history.                 | [07_glossary](./docs/07_glossary/)                                                                                     |
| ⚙️ **System Files**          | MCP configuration and schema definitions.                                   | [manifest.json](./manifest.json) / [schema.yaml](./schema.yaml)                                                        |

---

## ✨ Purpose

This repository provides a complete, organized documentation framework for directing, training, and sustaining church stage productions — especially large seasonal pageants such as Easter or Christmas.
It unites artistic best practices, technical operations, and spiritual formation under one clear standard.

**Primary Goals**

- Empower volunteers and leaders with clear expectations and language.
- Preserve ministry knowledge for future productions.
- Support AI/automation (via the Model Context Protocol, or MCP) for quick reference and training.
- Keep all creative work centered on **Christ, community, and excellence**.

> “Let all things be done decently and in order.”
> — _1 Corinthians 14:40_

---

## 🧱 Repository Structure

Each folder represents a domain of ministry, production, or training.

```
/docs
├── 01_introduction/ → Vision, mission, leadership briefs
├── 02_roles/ → Volunteer and staff role guides
├── 03_basics/ → Acting, singing, expression, movement
├── 04_rehearsal/ → Scheduling, etiquette, devotionals
├── 05_production/ → Technical and backstage operations
├── 06_ministry/ → Theology, servant leadership, sustainability
└── 07_glossary/ → Checklists, templates, feedback, change logs
```

**Core Configuration Files**
| File | Purpose |
|------|----------|
| `schema.yaml` | Defines metadata and validation rules for all documentation. |
| `manifest.json` | MCP manifest that connects resources and schemas for server integration. |

---

## ⚙️ Quick Start for Ministry Leaders

### 1. Read the Vision

Start in `/docs/01_introduction/vision.md` — it explains the theological and creative mission behind this documentation.

### 2. Assign Roles

Use `/docs/02_roles/` to define expectations and responsibilities for every team:
Director, Producer, Choral Director, Tech Team, Props Team, etc.

### 3. Plan Rehearsals

Consult `/docs/04_rehearsal/schedule.md` and `/docs/04_rehearsal/mock-schedule.md` for planning timelines from kickoff through Easter week.

### 4. Prepare Production Teams

Review `/docs/05_production/` for cues, lighting, props, and backstage coordination.

### 5. Lead Spiritually

Teach and model the heart of service through `/docs/06_ministry/servant-leadership.md` and `/docs/06_ministry/purpose.md`.

### 6. Use Tools and Checklists

Simplify operations with `/docs/07_glossary/checklists.md`, `/docs/07_glossary/templates.md`, and `/docs/07_glossary/feedback.md`.

---

## 🧩 MCP Integration (Optional Advanced Use)

This repository is **MCP-ready**, meaning it can be connected to AI assistants or custom servers for dynamic access and querying.

To register:

```bash
npx mcp-server serve --manifest ./manifest.json
```