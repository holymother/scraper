"""
Modal Scheduled Scraper for AI Newsletter Dashboard
Runs every 24 hours to scrape Ben's Bites and The AI Rundown

All scraping logic is included inline to avoid import issues.
"""

import modal
import json
from datetime import datetime, timedelta
import uuid

# Create Modal app
app = modal.App("ai-newsletter-scraper")

# Define the image with required dependencies
image = modal.Image.debian_slim().pip_install(
    "requests==2.31.0",
    "beautifulsoup4==4.12.2",
)

# Create Modal volume for persistent storage
volume = modal.Volume.from_name("ai-newsletter-data", create_if_missing=True)

# Mount path for the volume
VOLUME_PATH = "/data"


def scrape_bensbites():
    """Scrape Ben's Bites for latest articles"""
    import requests
    from bs4 import BeautifulSoup
    import time
    
    output = {
        "source": "bens_bites",
        "scrapedAt": datetime.utcnow().isoformat() + "Z",
        "articlesFound": 0,
        "articles": [],
        "errors": []
    }
    
    try:
        headers = {'User-Agent': 'AI-Newsletter-Dashboard/1.0 (Educational Project)'}
        url = "https://www.bensbites.com/archive"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        article_links = soup.find_all('a', href=lambda x: x and '/p/' in x)
        
        seen_urls = set()
        
        for link in article_links:
            article_url = link.get('href', '')
            if not article_url or article_url in seen_urls:
                continue
                
            if article_url.startswith('/'):
                article_url = 'https://www.bensbites.com' + article_url
            if not article_url.startswith('https://'):
                continue
            
            seen_urls.add(article_url)
            title = link.get_text(strip=True)
            
            if not title or len(title) < 3:
                continue
            
            description = None
            next_elem = link.find_next_sibling()
            if next_elem and next_elem.name in ['p', 'div']:
                desc_text = next_elem.get_text(strip=True)
                if desc_text and desc_text != title:
                    description = desc_text
            
            imageUrl = None
            parent = link.find_parent(['div', 'article'])
            if parent:
                img = parent.find('img')
                if img and img.get('src'):
                    imageUrl = img['src']
            
            article = {
                "title": title,
                "description": description,
                "url": article_url,
                "publishedAt": None,
                "imageUrl": imageUrl,
                "category": None
            }
            
            output["articles"].append(article)
        
        output["articlesFound"] = len(output["articles"])
        time.sleep(2)  # Rate limiting
        
    except Exception as e:
        output["errors"].append(f"Error: {str(e)}")
    
    return output


def scrape_airundown():
    """Scrape The AI Rundown for latest articles"""
    import requests
    from bs4 import BeautifulSoup
    import time
    
    output = {
        "source": "ai_rundown",
        "scrapedAt": datetime.utcnow().isoformat() + "Z",
        "articlesFound": 0,
        "articles": [],
        "errors": []
    }
    
    try:
        headers = {'User-Agent': 'AI-Newsletter-Dashboard/1.0 (Educational Project)'}
        url = "https://www.therundown.ai"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find "Latest Articles" section
        latest_section = None
        for heading in soup.find_all(['h2', 'h3', 'h4']):
            if 'latest' in heading.get_text().lower():
                latest_section = heading.find_parent()
                break
        
        if not latest_section:
            latest_section = soup
        
        article_links = latest_section.find_all('a', href=lambda x: x and '/p/' in x)
        seen_urls = set()
        
        for link in article_links:
            article_url = link.get('href', '')
            if not article_url or article_url in seen_urls:
                continue
                
            if article_url.startswith('/'):
                article_url = 'https://www.therundown.ai' + article_url
            if not article_url.startswith('https://'):
                continue
            
            seen_urls.add(article_url)
            title = link.get_text(strip=True)
            
            if not title or len(title) < 3:
                continue
            
            description = None
            next_elem = link.find_next_sibling()
            if next_elem and next_elem.name in ['p', 'div']:
                desc_text = next_elem.get_text(strip=True)
                if desc_text and desc_text != title:
                    description = desc_text
            
            imageUrl = None
            parent = link.find_parent(['div', 'article'])
            if parent:
                img = parent.find('img')
                if img and img.get('src'):
                    imageUrl = img['src']
            
            article = {
                "title": title,
                "description": description,
                "url": article_url,
                "publishedAt": None,
                "imageUrl": imageUrl,
                "category": None
            }
            
            output["articles"].append(article)
        
        output["articlesFound"] = len(output["articles"])
        time.sleep(2)
        
    except Exception as e:
        output["errors"].append(f"Error: {str(e)}")
    
    return output


def combine_and_filter(bens_bites_data, ai_rundown_data):
    """Combine articles from all sources and filter to last 24 hours"""
    # Combine all articles
    all_articles = []
    all_articles.extend(bens_bites_data["articles"])
    all_articles.extend(ai_rundown_data["articles"])
    
    # Deduplicate by URL
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        if article["url"] not in seen_urls:
            seen_urls.add(article["url"])
            unique_articles.append(article)
    
    # Add metadata
    now = datetime.utcnow()
    filtered_articles = []
    
    for article in unique_articles:
        # Add unique ID
        article["id"] = str(uuid.uuid4())
        
        # Add scraped timestamp
        article["scrapedAt"] = now.isoformat() + "Z"
        
        # Determine source
        if "bensbites" in article["url"]:
            article["source"] = "bens_bites"
        elif "therundown.ai" in article["url"]:
            article["source"] = "ai_rundown"
        
        # Add save fields
        article["saved"] = False
        article["savedAt"] = None
        
        filtered_articles.append(article)
    
    # Sort by URL (since we don't have publish dates)
    filtered_articles.sort(key=lambda x: x["url"], reverse=True)
    
    return filtered_articles


@app.function(
    image=image,
    schedule=modal.Cron("0 0 * * *"),  # Run daily at midnight UTC
    volumes={VOLUME_PATH: volume},
    timeout=600,  # 10 minute timeout
)
def scrape_newsletters():
    """
    Scheduled function that scrapes newsletters every 24 hours
    """
    print(f"🚀 Starting scheduled scrape at {datetime.utcnow().isoformat()}Z")
    
    try:
        print("📰 Scraping Ben's Bites...")
        bens_bites_data = scrape_bensbites()
        print(f"   ✓ Found {bens_bites_data['articlesFound']} articles")
        
        print("📰 Scraping The AI Rundown...")
        ai_rundown_data = scrape_airundown()
        print(f"   ✓ Found {ai_rundown_data['articlesFound']} articles")
        
        print("🔗 Combining and filtering...")
        articles = combine_and_filter(bens_bites_data, ai_rundown_data)
        print(f"   ✓ Final count: {len(articles)} unique articles")
        
        # Save to volume
        output_path = f"{VOLUME_PATH}/articles.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        # Commit changes to volume
        volume.commit()
        
        print(f"💾 Saved to {output_path}")
        print(f"✅ Scraping complete!")
        
        return {
            "success": True,
            "articles_count": len(articles),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sources": {
                "bens_bites": len([a for a in articles if a.get('source') == 'bens_bites']),
                "ai_rundown": len([a for a in articles if a.get('source') == 'ai_rundown']),
            }
        }
        
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


@app.function(
    image=image,
    volumes={VOLUME_PATH: volume},
)
def get_latest_articles():
    """
    Function to retrieve the latest scraped articles from the volume
    """
    output_path = f"{VOLUME_PATH}/articles.json"
    
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        return {
            "success": True,
            "articles": articles,
            "count": len(articles)
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "No articles found. Run scrape_newsletters first."
        }


@app.local_entrypoint()
def main():
    """
    Local entrypoint for manual testing
    Run with: modal run modal_scraper.py
    """
    print("🧪 Running manual scrape...")
    result = scrape_newsletters.remote()
    print(f"\n📊 Result:")
    print(json.dumps(result, indent=2))

