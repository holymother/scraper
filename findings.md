# 🔍 Findings & Research Log

**Project**: AI Newsletter Dashboard  
**Created**: 2026-02-08

---

## Research Sessions

### Session 1: Project Initialization (2026-02-08)

#### User Requirements Gathered
- **Primary Sources**: Ben's Bites, The AI Rundown (Reddit later)
- **Time Window**: Last 24 hours of articles
- **Update Frequency**: Every 24 hours
- **Persistence**: Saved articles must survive page refresh
- **Future Integration**: Supabase for database
- **Phase 1 Scope**: Web scraping only (no API integrations yet)

#### Technical Constraints
- No external API keys required for Phase 1 (web scraping)
- LocalStorage will be used initially for saved articles
- Supabase integration deferred to Phase 2

#### Design Requirements
- "Gorgeous, interactive, beautiful" aesthetic
- Modern web design principles
- Smooth animations and transitions

---

## Discoveries

### Newsletter Sources

#### **Ben's Bites** ✓
- **Platform**: Hosted on Substack (bensbites.com)
- **URL Structure**: 
  - Homepage: https://www.bensbites.com
  - Archive: https://www.bensbites.com/archive (organized by month/year)
  - Individual posts: https://www.bensbites.com/p/{slug}
- **Article Format**: 
  - Organized chronologically by month (e.g., "January 2026", "December 2025")
  - Each article has a title and subtitle
  - No public API available (Substack limitation)
- **Scraping Approach**: 
  - **Method**: HTML scraping of archive page
  - **Note**: Ben's Bites created their own searchable archive using web scraping (open-source on GitHub: transitive-bullshit/bens-bites-ai-search)
  - Articles are in standard Substack HTML structure
- **Constraints**:
  - No RSS feed or API
  - Must parse HTML directly
  - Archive page shows recent articles with chronological organization

#### **The AI Rundown** ✓
- **Platform**: Custom website (therundown.ai)
- **URL Structure**:
  - Homepage: https://www.therundown.ai
  - Latest Articles section: Built into homepage
  - Individual posts: https://www.therundown.ai/p/{slug}
- **Article Format**:
  - "Latest Articles" section has 8+ recent articles
  - Each article shows:
    - Title (H3 heading)
    - Subtitle/description
    - Author attribution (e.g., "Zach Mink, +4")
    - Link to full article
  - Clean, structured HTML
- **Scraping Approach**:
  - **Method**: HTML scraping of homepage or Latest Articles section
  - Articles clearly marked with H3 headers
  - Consistent structure for easy parsing
- **Publishing Pattern**: Daily newsletter format

---

## Technical Constraints & Edge Cases

### Confirmed Constraints
- **No Public APIs**: Neither source has a public API; web scraping is required
- **Platform Differences**: 
  - Ben's Bites: Substack-based (generic CMS)
  - The AI Rundown: Custom website (potentially easier to scrape)
- **Update Schedule**: Both appear to be daily newsletters
- **Timestamp Extraction**: May need to parse publication dates from HTML or use scrape time as fallback
- **Image Handling**: Articles may have featured images; need to extract image URLs

### Edge Cases to Handle
1. **Missing Timestamps**: Some articles may not have explicit publication dates
2. **Pagination**: Archive pages may paginate older content
3. **Rate Limiting**: Must implement delays between requests (2+ seconds)
4. **Broken Links**: Some article URLs may be inaccessible
5. **HTML Structure Changes**: Websites may update their HTML, breaking scrapers
6. **Duplicate Detection**: Same article may appear in multiple scrapes (use URL as unique ID)

---

## Libraries & Tools Recommended

### Backend (Scraping)
- **BeautifulSoup4** + **Requests**: For static HTML scraping (both sources appear to be server-rendered)
- **Alternative**: Playwright (if JavaScript rendering is needed, but likely overkill)
- **dateutil/python-dateutil**: For parsing publication dates
- **uuid**: For generating unique article IDs

### Frontend (Dashboard)
- **Recommended**: **Vanilla HTML/CSS/JavaScript** for maximum control and beautiful custom designs
- **Alternative**: Vite + Vanilla JS (for better dev experience with hot reload)
- **Note**: User emphasized "gorgeous, interactive, beautiful" - custom styling is better than framework defaults

### Styling
- **Custom CSS**: Required for premium aesthetics (glassmorphism, gradients, animations)
- **Google Fonts**: Inter, Outfit, or similar modern typefaces
- **CSS Variables**: For theming and consistent design tokens

### Storage
- **Phase 1**: LocalStorage (for saved articles, simple and immediate)
- **Phase 2**: Supabase (for persistence across devices, planned for future)

---

## Questions for User
*List any clarifying questions identified during research*

---

## Next Research Tasks
1. Investigate Ben's Bites website structure
2. Investigate The AI Rundown website structure
3. Determine best scraping method (static HTML vs dynamic JS)
4. Research frontend framework requirements
