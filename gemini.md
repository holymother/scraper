# 📜 Project Constitution: AI Newsletter Dashboard

**Last Updated**: 2026-02-08  
**Project Type**: Web Dashboard + Data Scraping Automation  
**Architecture**: B.L.A.S.T. Protocol with A.N.T. 3-Layer System

---

## 🎯 North Star (Mission Statement)
Display the latest AI newsletter articles (last 24 hours) from multiple sources in a beautiful, interactive dashboard with save functionality and automatic daily updates.

---

## 📊 Data Schemas

### Article Schema (Primary Entity)
```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string | null",
  "url": "string (URL)",
  "source": "string (enum: 'bens_bites', 'ai_rundown', 'reddit')",
  "publishedAt": "string (ISO 8601 timestamp)",
  "scrapedAt": "string (ISO 8601 timestamp)",
  "imageUrl": "string (URL) | null",
  "category": "string | null",
  "saved": "boolean (default: false)",
  "savedAt": "string (ISO 8601 timestamp) | null"
}
```

### Scraper Output Schema
```json
{
  "source": "string",
  "scrapedAt": "string (ISO 8601)",
  "articlesFound": "number",
  "articles": [
    {
      "title": "string",
      "description": "string | null",
      "url": "string",
      "publishedAt": "string",
      "imageUrl": "string | null",
      "category": "string | null"
    }
  ],
  "errors": ["string"] | null
}
```

### Dashboard State Schema
```json
{
  "lastUpdated": "string (ISO 8601)",
  "articles": ["Article[]"],
  "savedArticles": ["Article[]"],
  "filters": {
    "source": "string | 'all'",
    "showSavedOnly": "boolean",
    "timeRange": "string (enum: '24h', '7d', '30d')"
  }
}
```

---

## 🔧 Integrations

### Phase 1 (Current - Web Scraping)
- **Ben's Bites Newsletter** (https://www.bensbites.com)
- **The AI Rundown** (https://www.therundown.ai)
- Storage: LocalStorage (browser) for saved articles

### Phase 2 (Future - Database)
- **Supabase**: PostgreSQL database for persistence
  - Tables: `articles`, `saved_articles`, `scrape_logs`
  - Real-time subscriptions for live updates

### Phase 3 (Future - Advanced)
- **Reddit API**: r/artificial, r/MachineLearning
- **Cron Job/Cloud Functions**: Automated 24-hour scraping
- **Email Notifications**: Optional digest delivery

---

## 🎨 Behavioral Rules

### Design Principles
1. **Visual Excellence**: Premium, modern aesthetic with glassmorphism, gradients, and smooth animations
2. **Responsiveness**: Micro-interactions on hover, save actions, and scroll
3. **Performance**: Lazy loading for images, virtualized lists for large datasets
4. **Accessibility**: WCAG AA compliance, keyboard navigation, ARIA labels

### Design System (User-Provided)

#### Color Palette
- **Primary**: `#FAF2E8` (warm beige background)
- **Accent**: `#FF9C94` (coral/pink for links and interactive elements)
- **Background**: `#FAF2E8`
- **Text Primary**: `#242424` (dark charcoal)
- **Link Color**: `#FF9C94`

#### Typography
- **Font Family**: Figtree (for body and headings)
- **Font Sizes**:
  - `h1`: 173.867px (hero text)
  - `h2`: 16px
  - `body`: 23.4667px

**Note**: These exact values will be implemented in `styles.css` using CSS custom properties for consistency.

### Data Handling Rules
1. **24-Hour Window**: Filter articles where `publishedAt` is within last 24 hours
2. **Deduplication**: Use article URL as unique identifier to prevent duplicates
3. **Saved Persistence**: Saved articles persist across page refreshes via LocalStorage (Phase 1) or Supabase (Phase 2)
4. **Error Tolerance**: If a source fails to scrape, display other sources normally

### Scraping Ethics
1. **Rate Limiting**: Maximum 1 request per 2 seconds per source
2. **User-Agent**: Identify as legitimate research bot
3. **Respect robots.txt**: Check and honor crawl directives
4. **Caching**: Store scraped data to minimize repeat requests

---

## 🏗️ Architecture Invariants

### 3-Layer Structure
```
Layer 1: Architecture (architecture/)
  ├── scraper_sop.md          # Scraping methodology and rules
  ├── dashboard_sop.md         # UI/UX specifications
  └── deployment_sop.md        # Automation and cloud deployment

Layer 2: Navigation (This AI Agent)
  └── Routes data between SOPs and Tools based on user intent

Layer 3: Tools (tools/)
  ├── scrape_bensbites.py      # Ben's Bites scraper
  ├── scrape_airundown.py      # AI Rundown scraper
  ├── filter_24h.py            # Time-based filtering
  └── deduplicate.py           # Remove duplicate articles
```

### File System Rules
- **Temporary Data**: All scraped raw data goes to `.tmp/`
- **Secrets**: API keys and credentials in `.env` (never committed)
- **Deliverables**: Final dashboard in main project directory
- **Logs**: Scraping logs stored in `.tmp/logs/` for debugging

---

## 🔄 Update Log

### 2026-02-08 19:52 - Initial Constitution
- Defined Article, Scraper Output, and Dashboard State schemas
- Established 3-layer architecture structure
- Documented Phase 1-3 integration roadmap
- Set behavioral rules for design, data, and scraping

---

## 📋 Next Schema Updates Required
- [ ] Refine schema after researching actual newsletter structure
- [ ] Add error handling schema for failed scrapes
- [ ] Define webhook payload schema for automation triggers
