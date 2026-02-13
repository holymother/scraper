/**
 * AI Newsletter Dashboard - JavaScript
 * Handles article loading, filtering, and save functionality
 */

// ============ Supabase Client ============
const SUPABASE_URL = 'https://yrsphamotsgcngtzolwt.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlyc3BoYW1vdHNnY25ndHpvbHd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3NzUxNjYsImV4cCI6MjA4NjM1MTE2Nn0.MGll6bTRgpZW9ek2mPFFF1X6BtxdWXCWfkRd1J-Afog';

// Initialize Supabase client (named supabaseClient to avoid shadowing library)
const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Initialization flag to prevent double loading
let isInitialized = false;

// ============ State Management ============
let allArticles = [];
let currentFilter = 'all';
let showSavedOnly = false;

// ============ LocalStorage Keys ============
const STORAGE_KEY = 'ai-newsletter-saved-articles';

// ============ Initialize ============
// Support both early and late script loading
if (document.readyState === 'loading') {
    // Still loading, wait for DOMContentLoaded
    document.addEventListener('DOMContentLoaded', () => {
        if (!isInitialized) {
            isInitialized = true;
            loadArticles();
            setupEventListeners();
        }
    });
} else {
    // DOM already loaded, run immediately
    if (!isInitialized) {
        isInitialized = true;
        loadArticles();
        setupEventListeners();
    }
}

// ============ Event Listeners ============
function setupEventListeners() {
    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            renderArticles();
        });
    });

    // Saved only toggle
    const savedToggle = document.getElementById('savedOnlyToggle');
    savedToggle.addEventListener('change', (e) => {
        showSavedOnly = e.target.checked;
        renderArticles();
    });
}

// ============ Load Articles ============
async function loadArticles() {
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');

    try {
        console.log('🔄 Fetching articles from Supabase...');

        // Fetch from Supabase instead of local JSON
        const { data: articles, error } = await supabaseClient
            .from('articles')
            .select('*')
            .order('scraped_at', { ascending: false })
            .limit(100);

        if (error) {
            throw new Error(`Supabase error: ${error.message}`);
        }

        if (!articles || articles.length === 0) {
            throw new Error('No articles found in database');
        }

        console.log(`✅ Loaded ${articles.length} articles from Supabase`);

        // Transform Supabase data to match our schema
        allArticles = articles.map(article => ({
            id: article.article_id,
            title: article.title,
            description: article.description,
            url: article.url,
            publishedAt: article.published_at,
            scrapedAt: article.scraped_at,
            imageUrl: article.image_url,
            category: article.category,
            source: article.source,
            saved: false  // Will be updated from LocalStorage below
        }));

        // Load saved article IDs from LocalStorage
        const savedArticles = getSavedArticles();

        // Mark articles as saved
        allArticles.forEach(article => {
            if (savedArticles.includes(article.id)) {
                article.saved = true;
            }
        });

        // Hide loading, show articles
        loadingState.style.display = 'none';
        updateLastUpdated();
        renderArticles();

    } catch (error) {
        console.error('Error loading articles:', error);
        loadingState.style.display = 'none';
        errorState.style.display = 'block';

        // Update error message to be more helpful
        const errorText = document.querySelector('#errorState p');
        if (errorText) {
            errorText.textContent = `Unable to load articles from database. ${error.message}`;
        }
    }
}

// ============ Render Articles ============
function renderArticles() {
    const grid = document.getElementById('articlesGrid');
    const emptyState = document.getElementById('emptyState');

    // Filter articles
    let filtered = allArticles;

    // Apply source filter
    if (currentFilter !== 'all') {
        filtered = filtered.filter(article => article.source === currentFilter);
    }

    // Apply saved filter
    if (showSavedOnly) {
        filtered = filtered.filter(article => article.saved);
    }

    // Show empty state if no articles
    if (filtered.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    // Hide empty state
    emptyState.style.display = 'none';
    grid.style.display = 'grid';

    // Clear grid
    grid.innerHTML = '';

    // Render each article
    filtered.forEach((article, index) => {
        const card = createArticleCard(article, index);
        grid.appendChild(card);
    });
}


// ============ Create Article Card ============
function createArticleCard(article, index) {
    const card = document.createElement('div');
    card.className = 'article-card';
    card.dataset.articleId = article.id;
    card.setAttribute('role', 'article');
    card.setAttribute('aria-label', `Read article: ${article.title}`);

    // Handle card click (open article) - but don't interfere with buttons
    card.addEventListener('click', (e) => {
        // Don't open if clicking save button or CTA button
        if (e.target.closest('.save-btn') || e.target.closest('.article-cta-btn')) return;
        window.open(article.url, '_blank', 'noopener,noreferrer');
    });

    // Image
    let imageHTML = '';
    if (article.imageUrl) {
        imageHTML = `
      <div class="article-image">
        <img src="${escapeHtml(article.imageUrl)}" alt="${escapeHtml(article.title)}" loading="lazy">
      </div>
    `;
    }

    // Source badge
    const sourceName = article.source === 'bens_bites' ? "Ben's Bites" : 'The AI Rundown';

    // Time ago
    const timeAgo = getTimeAgo(article.publishedAt || article.scrapedAt);

    // Save button
    const heartClass = article.saved ? 'heart-icon filled' : 'heart-icon';
    const saveLabel = article.saved ? 'Unsave article' : 'Save article';

    card.innerHTML = `
    ${imageHTML}
    <div class="article-inner-content">
      <div class="article-content">
        <span class="source-badge ${article.source}">${sourceName}</span>
        <h3 class="article-title">${escapeHtml(article.title)}</h3>
        ${article.description ? `<p class="article-description">${escapeHtml(article.description)}</p>` : ''}
        <div class="article-meta">
          <time class="publish-time" datetime="${article.publishedAt || article.scrapedAt}">
            ${timeAgo}
          </time>
          <button class="save-btn" aria-label="${saveLabel}: ${escapeHtml(article.title)}" data-article-id="${article.id}">
            <svg class="${heartClass}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
    <div class="article-cta">
      <a href="${escapeHtml(article.url)}" target="_blank" rel="noopener noreferrer" class="article-cta-btn">
        Read Article
        <svg class="arrow-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  `;

    // Add save button listener
    const saveBtn = card.querySelector('.save-btn');
    saveBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSave(article.id);
    });

    return card;
}

// ============ Toggle Save ============
function toggleSave(articleId) {
    const article = allArticles.find(a => a.id === articleId);
    if (!article) return;

    article.saved = !article.saved;

    // Update LocalStorage
    const savedArticles = getSavedArticles();
    if (article.saved) {
        savedArticles.push(articleId);
        article.savedAt = new Date().toISOString();
    } else {
        const index = savedArticles.indexOf(articleId);
        if (index > -1) {
            savedArticles.splice(index, 1);
        }
        article.savedAt = null;
    }

    saveSavedArticles(savedArticles);

    // Re-render (to update UI and handle saved-only filter)
    renderArticles();
}

// ============ LocalStorage Functions ============
function getSavedArticles() {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
}

function saveSavedArticles(articleIds) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(articleIds));
}

// ============ Utility Functions ============
function updateLastUpdated() {
    const lastUpdatedEl = document.getElementById('lastUpdated');
    if (allArticles.length > 0) {
        const mostRecent = allArticles[0].scrapedAt || allArticles[0].publishedAt;
        lastUpdatedEl.textContent = `Last updated: ${getTimeAgo(mostRecent)}`;
    } else {
        lastUpdatedEl.textContent = 'No articles loaded';
    }
}

function getTimeAgo(timestamp) {
    if (!timestamp) return 'Recently';

    const date = new Date(timestamp);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval !== 1 ? 's' : ''} ago`;
        }
    }

    return 'Just now';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
