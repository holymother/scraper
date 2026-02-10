# Scraper SOP - AI Newsletter Dashboard
**Layer 1: Architecture**  
**Created**: 2026-02-08  
**Purpose**: Define scraping methodology, ethics, error handling, and data validation

---

## 🎯 Scraping Goals

1. Extract latest articles from Ben's Bites and The AI Rundown
2. Return consistent JSON structure matching the `Scraper Output Schema`
3. Handle errors gracefully without crashing the entire system
4. Respect websites and follow ethical scraping practices

---

## 🌐 Target Sources

### Source 1: Ben's Bites
- **URL**: https://www.bensbites.com/archive
- **Platform**: Substack
- **Structure**: 
  - Articles organized by month headers (e.g., "### January 2026")
  - Each article has a title, subtitle, and link
  - Format: `[Title](url)` followed by `[Subtitle](url)`
- **Extraction Strategy**:
  1. Fetch archive page HTML
  2. Parse with BeautifulSoup4
  3. Find all links within chronological sections
  4. Extract title (link text), subtitle (next line text), URL (href)
  5. Estimate publish date from section header (e.g., January 2026)

### Source 2: The AI Rundown
- **URL**: https://www.therundown.ai
- **Platform**: Custom website
- **Structure**:
  - "Latest Articles" section on homepage
  - Articles have H3 titles, descriptions, author info
  - Clean, structured HTML
- **Extraction Strategy**:
  1. Fetch homepage HTML
  2. Parse with BeautifulSoup4
  3. Find "Latest Articles" section
  4. Extract all H3 headers as titles
  5. Extract following paragraph as description
  6. Extract link from H3 anchor tag

---

## 🛠️ Technical Implementation

### Required Libraries
```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
```

### Error Handling Protocol
1. **Network Errors**: Catch `requests.exceptions.RequestException`
   - Return empty scraper output with error logged
   - Never crash the entire system
2. **HTML Parsing Errors**: Catch `AttributeError` when elements not found
   - Skip malformed articles
   - Log warning but continue processing
3. **Timeout Errors**: Set 10-second timeout on all requests
   - Fail gracefully if site is slow/down

### Rate Limiting Rules
- **Delay**: Minimum 2 seconds between requests to same domain
- **User-Agent**: Set custom UA: `"AI-Newsletter-Dashboard/1.0 (Educational Project)"`
- **Respect robots.txt**: Check robots.txt before scraping (manual check for Phase 1)

---

## 📋 Data Validation

### Output Schema Validation
Every scraper must return JSON matching this structure:
```json
{
  "source": "string (enum: 'bens_bites', 'ai_rundown')",
  "scrapedAt": "string (ISO 8601 timestamp)",
  "articlesFound": "number",
  "articles": [
    {
      "title": "string (required)",
      "description": "string | null",
      "url": "string (required, valid URL)",
      "publishedAt": "string (ISO 8601) | null",
      "imageUrl": "string (URL) | null",
      "category": "string | null"
    }
  ],
  "errors": ["string"] | null
}
```

### Validation Rules
1. `title` and `url` are **required** for each article
2. `publishedAt` should be ISO 8601 format or `null`
3. `url` must be a valid absolute URL (starts with https://)
4. If scraping fails completely, return `articles: []` with error message in `errors` array

---

## 🔄 Self-Annealing (Error Recovery)

### When HTML Structure Changes
**Problem**: Website updates HTML, breaking CSS selectors

**Solution**:
1. Log the error with full stack trace to `.tmp/logs/`
2. Return empty results for that source only
3. Update this SOP with new HTML structure after manual inspection
4. Update corresponding Python script in `tools/`

### Common Edge Cases
1. **Missing Timestamp**: Use `scrapedAt` as fallback for `publishedAt`
2. **Missing Description**: Set to `null`, not empty string
3. **Relative URLs**: Convert to absolute URLs using `urljoin()`
4. **Articles > 24h old**: Let filtering happen in later step, scraper returns all

---

## ✅ Testing Checklist

Before deploying a scraper:
- [ ] Test with live website
- [ ] Verify JSON structure matches schema
- [ ] Test error handling (disconnect internet mid-request)
- [ ] Verify rate limiting (check delay between requests)
- [ ] Validate all URLs are absolute and accessible
- [ ] Check for duplicate articles in output

---

## 📝 Maintenance Log

### Ben's Bites Scraper
- **2026-02-08**: Initial implementation based on current archive structure

### The AI Rundown Scraper
- **2026-02-08**: Initial implementation based on homepage "Latest Articles" section

---

## 🚨 Known Gotchas

1. **Substack Paywalls**: Ben's Bites may have paywalled content (skip those articles)
2. **JavaScript Rendering**: Current approach assumes server-side rendering; if sites switch to client-side rendering, we'll need Playwright
3. **Archive Pagination**: Ben's Bites archive may paginate older months (not critical for 24h window)
