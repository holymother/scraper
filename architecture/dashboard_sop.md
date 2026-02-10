# Dashboard SOP - AI Newsletter Dashboard
**Layer 1: Architecture**  
**Created**: 2026-02-08  
**Purpose**: Define UI/UX specifications, design system, and component structure

---

## 🎨 Design System

### Color Palette
```css
:root {
  --color-primary: #FAF2E8;      /* Warm beige background */
  --color-accent: #FF9C94;       /* Coral/pink for interactive elements */
  --color-text-primary: #242424; /* Dark charcoal text */
  --color-text-secondary: #5A5A5A; /* Lighter gray for metadata */
  --color-card-bg: rgba(250, 242, 232, 0.6); /* Semi-transparent for glassmorphism */
  --color-card-border: rgba(255, 156, 148, 0.2); /* Subtle accent border */
}
```

### Typography
- **Font**: Figtree (Google Fonts)
- **Sizes**:
  - `h1`: 173.867px (hero/logo text)
  - `h2`: 16px (section headers)
  - `body`: 23.4667px (article text)

```css
:root {
  --font-primary: 'Figtree', sans-serif;
  --size-h1: 173.867px;
  --size-h2: 16px;
  --size-body: 23.4667px;
  --size-small: 18px; /* For metadata */
}
```

### Spacing System
```css
:root {
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 48px;
  --space-xl: 96px;
}
```

---

## 🧩 Component Specifications

### 1. Article Card (.article-card)

**Visual Design**:
- Glassmorphism effect: `backdrop-filter: blur(10px)`
- Background: Semi-transparent warm beige
- Border: 1px solid accent with low opacity
- Border radius: 16px
- Padding: 24px
- Box shadow: Subtle elevation on hover

**Structure**:
```html
<div class="article-card" data-article-id="{uuid}">
  <div class="article-image">
    <img src="{imageUrl}" alt="{title}">
  </div>
  <div class="article-content">
    <span class="source-badge">{source}</span>
    <h3 class="article-title">{title}</h3>
    <p class="article-description">{description}</p>
    <div class="article-meta">
      <span class="publish-time">{timeAgo}</span>
      <button class="save-btn" aria-label="Save article">
        <svg class="heart-icon">{heart SVG}</svg>
      </button>
    </div>
  </div>
</div>
```

**Interactions**:
- Hover: Lift effect (translateY(-4px)) with increased shadow
- Click card: Open article URL in new tab
- Click save button: Toggle saved state with animation

### 2. Source Badge (.source-badge)

**Ben's Bites Badge**:
- Background: `#FF9C94` with 0.2 opacity
- Text color: `#242424`
- Text: "Ben's Bites"

**The AI Rundown Badge**:
- Background: `#FF9C94` with 0.4 opacity
- Text color: `#242424`
- Text: "The AI Rundown"

**Style**:
- Border radius: 8px
- Padding: 4px 12px
- Font size: 14px
- Display: inline-block

### 3. Save Button (.save-btn)

**States**:
- **Unsaved**: Heart outline (stroke only)
- **Saved**: Filled heart with accent color
- **Hover**: Scale up slightly (1.1x)
- **Click**: Pulse animation

**SVG Heart Icon**:
```html
<!-- Unsaved -->
<svg class="heart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
</svg>

<!-- Saved -->
<svg class="heart-icon filled" viewBox="0 0 24 24" fill="#FF9C94" stroke="none">
  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
</svg>
```

### 4. Filter Bar (.filter-bar)

**Layout**:
- Sticky header (position: sticky, top: 0)
- Background: Primary color with slight blur
- Z-index: 100
- Padding: 16px 24px

**Filter Buttons**:
- All / Ben's Bites / The AI Rundown
- Active state: Accent background, white text
- Inactive state: Transparent background, text color
- Border radius: 8px
- Transition: 0.3s ease

**Saved Only Toggle**:
- Checkbox styled as toggle switch
- Accent color when active
- Label: "Saved Only"

---

## 🎭 Animations & Interactions

### Card Entrance Animation
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.article-card {
  animation: fadeInUp 0.5s ease-out;
  animation-fill-mode: both;
}

/* Stagger animation for multiple cards */
.article-card:nth-child(1) { animation-delay: 0.05s; }
.article-card:nth-child(2) { animation-delay: 0.1s; }
.article-card:nth-child(3) { animation-delay: 0.15s; }
```

### Save Button Animation
```css
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.save-btn.saving {
  animation: pulse 0.3s ease-out;
}
```

### Hover Effects
- Cards: `transform: translateY(-4px)` with shadow increase
- Buttons: `transform: scale(1.05)`
- Links: Color transition to accent

---

## 📱 Responsive Design

### Breakpoints
```css
--breakpoint-mobile: 0px - 640px
--breakpoint-tablet: 641px - 1024px
--breakpoint-desktop: 1025px+
```

### Grid Layout
- **Mobile**: 1 column
- **Tablet**: 2 columns
- **Desktop**: 3 columns

```css
.articles-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: 1fr; /* Mobile */
}

@media (min-width: 641px) {
  .articles-grid {
    grid-template-columns: repeat(2, 1fr); /* Tablet */
  }
}

@media (min-width: 1025px) {
  .articles-grid {
    grid-template-columns: repeat(3, 1fr); /* Desktop */
  }
}
```

---

## ♿ Accessibility Requirements

### ARIA Labels
- All interactive elements must have `aria-label`
- Save button: `aria-label="Save article: {article title}"`
- Filter buttons: `aria-label="Filter by {source}"`
- Article cards: `aria-label="Read article: {title}"`

### Keyboard Navigation
- Tab order: Filter bar → Article cards → Save buttons
- Enter/Space on article card: Open article
- Enter/Space on save button: Toggle save state
- Focus visible: Accent color outline

### Screen Reader Support
- Image alt text: Descriptive article titles
- Time elements: `<time datetime="{ISO 8601}">{human readable}</time>`
- Loading states: `aria-live="polite"` announcements

---

## 📊 Dashboard Layout Structure

```
┌─────────────────────────────────────────────┐
│  Header (h1 logo + last updated)           │
├─────────────────────────────────────────────┤
│  Filter Bar (sticky)                        │
│  [All] [Ben's Bites] [The AI Rundown]       │
│  [Saved Only: ○]                            │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐               │
│  │Card 1│ │Card 2│ │Card 3│               │
│  └──────┘ └──────┘ └──────┘               │
│                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐               │
│  │Card 4│ │Card 5│ │Card 6│               │
│  └──────┘ └──────┘ └──────┘               │
│                                             │
└─────────────────────────────────────────────┘
```

---

## ✅ Quality Checklist

Before deployment:
- [ ] All colors match user-provided design system
- [ ] Figtree font loaded from Google Fonts
- [ ] Typography sizes exactly match spec (h1: 173.867px, etc.)
- [ ] Glassmorphism effects visible on cards
- [ ] Smooth animations on all interactions
- [ ] Responsive on mobile, tablet, desktop
- [ ] Save functionality persists across refresh
- [ ] Filters work correctly
- [ ] Accessibility: keyboard nav, ARIA labels, screen reader tested
- [ ] Performance: No layout shift, smooth 60fps animations
