# AI Newsletter Dashboard 🤖📰

A beautiful, interactive dashboard that displays the latest AI newsletter articles from Ben's Bites and The AI Rundown with automated scraping and a stunning Bento Grid layout.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎨 Beautiful Bento Grid Layout
- **Dynamic card sizes**: 2x2, 1x1, 1x2, and 2x1 grid patterns
- **Interactive CTA buttons**: "Read Article" button slides up from bottom on hover
- **Glassmorphism effects**: Modern frosted glass aesthetic
- **Smooth animations**: Card entrance, hover effects, and transitions
- **Responsive design**: Perfect on mobile, tablet, and desktop

### 🔍 Automated Scraping
- **Ben's Bites**: Scrapes latest articles from archive
- **The AI Rundown**: Extracts articles from homepage
- **24-hour filtering**: Shows only articles from the last 24 hours
- **Automatic deduplication**: Removes duplicate articles by URL
- **Error resilience**: Handles network failures gracefully

### 💾 User Features
- **Save articles**: Click heart icon to save favorite articles
- **Persistent storage**: Saved articles persist across page refresh (LocalStorage)
- **Source filtering**: Filter by "All", "Ben's Bites", or "The AI Rundown"
- **Saved-only view**: Toggle to show only saved articles

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/holymother/scraper.git
   cd scraper
   ```

2. **Install Python dependencies**:
   ```bash
   pip install requests beautifulsoup4
   ```

3. **Run the scraper**:
   ```bash
   python3 scrape_all.py
   ```
   This will create `.tmp/articles.json` with the latest articles.

4. **Start the local server**:
   ```bash
   python3 server.py
   ```
   
5. **Open the dashboard**:
   - The server will start on `http://localhost:8080`
   - Open your browser and navigate to: **http://localhost:8080**
   - You should see the beautiful Bento Grid dashboard with articles!

> **Note**: You must use the local server (`server.py`) instead of opening `index.html` directly. Opening the HTML file directly will cause CORS errors when loading articles.

### Quick Commands

```bash
# Scrape latest articles
python3 scrape_all.py

# Start dashboard server
python3 server.py

# Then open http://localhost:8080 in your browser
```

## 📂 Project Structure

```
scraper/
├── index.html              # Dashboard HTML
├── styles.css              # Bento Grid styles and design system
├── app.js                  # Dashboard JavaScript
├── scrape_all.py           # Main scraper orchestration
├── server.py               # Local HTTP server (port 8080)
├── .gitignore              # Git ignore rules
├── .env                    # Environment variables (create your own)
│
├── tools/                  # Layer 3: Python scraping tools
│   ├── scrape_bensbites.py
│   ├── scrape_airundown.py
│   ├── filter_24h.py
│   └── combine_sources.py
│
├── architecture/           # Layer 1: SOPs & documentation
│   ├── scraper_sop.md
│   └── dashboard_sop.md
│
├── .tmp/                   # Temporary data (gitignored)
│   ├── articles.json       # Scraped article data
│   └── logs/               # Scraping logs
│
├── gemini.md               # Project constitution
├── findings.md             # Research notes
├── progress.md             # Progress log
└── task_plan.md            # Project roadmap
```

## 🎨 Design System

### Colors
- **Primary**: `#FAF2E8` (Warm beige)
- **Accent**: `#FF9C94` (Coral/pink)
- **Text**: `#242424` (Dark charcoal)

### Typography
- **Font Family**: Figtree (Google Fonts)
- **Sizes**:
  - H1 (Logo): 173.867px
  - H2 (Filters): 16px
  - Body (Articles): 23.4667px

### Effects
- **Glassmorphism**: `backdrop-filter: blur(10px)`
- **Smooth transitions**: 0.3s ease
- **Card hover**: Lift 4px with accent border

## 🔧 How It Works

### Scraping Pipeline

1. **Scrape Ben's Bites** (`scrape_bensbites.py`)
   - Fetches archive page
   - Extracts titles, URLs, descriptions, images
   - Returns JSON with 12 articles

2. **Scrape The AI Rundown** (`scrape_airundown.py`)
   - Fetches homepage
   - Finds "Latest Articles" section
   - Returns JSON with 16 articles

3. **Combine Sources** (`combine_sources.py`)
   - Merges all articles
   - Deduplicates by URL
   - Generates unique UUIDs
   - Sorts by publish date

4. **Filter 24 Hours** (`filter_24h.py`)
   - Keeps articles from last 24 hours
   - Uses `publishedAt` or `scrapedAt` as fallback

5. **Save to JSON**
   - Outputs to `.tmp/articles.json`
   - Creates timestamped log in `.tmp/logs/`

### Dashboard Flow

1. **Load Articles**: Fetch `.tmp/articles.json`
2. **Render Grid**: Create Bento Grid with varying card sizes
3. **Handle Interactions**:
   - Filter by source
   - Toggle saved-only view
   - Save/unsave articles (persists to LocalStorage)
4. **Update UI**: Smooth animations and transitions

## 📊 Data Schema

Each article follows this JSON structure:

```json
{
  "id": "uuid-v4",
  "title": "Article Title",
  "description": "Article description or excerpt",
  "url": "https://...",
  "source": "bens_bites" or "ai_rundown",
  "publishedAt": "2026-02-09T12:00:00Z",
  "scrapedAt": "2026-02-09T13:00:00Z",
  "imageUrl": "https://...",
  "category": null,
  "saved": false,
  "savedAt": null
}
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- [ ] **Automated 24-hour cron job** for scraping
- [ ] **Supabase integration** for cross-device persistence
- [ ] **Reddit sources** (r/artificial, r/MachineLearning)
- [ ] **Email digest** notifications
- [ ] **Cloud deployment** (Vercel, Netlify)
- [ ] **Custom grid patterns** configuration
- [ ] **Dark mode** toggle

## 🙏 Acknowledgments

- **Aceternity UI**: Bento Grid component inspiration
- **Ben's Bites**: AI newsletter source
- **The AI Rundown**: AI newsletter source
- **Google Fonts**: Figtree font family

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using the B.L.A.S.T. Protocol**
