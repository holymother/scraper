#!/usr/bin/env python3
"""
The AI Rundown Scraper
Scrapes latest articles from The AI Rundown homepage
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json


def scrape():
    """
    Scrape The AI Rundown homepage for latest articles
    
    Returns:
        dict: Scraper output matching schema
    """
    output = {
        "source": "ai_rundown",
        "scrapedAt": datetime.utcnow().isoformat() + "Z",
        "articlesFound": 0,
        "articles": [],
        "errors": []
    }
    
    try:
        # Set user agent
        headers = {
            'User-Agent': 'AI-Newsletter-Dashboard/1.0 (Educational Project)'
        }
        
        # Fetch homepage
        url = "https://www.therundown.ai"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article links (therundown.ai uses /p/ for posts)
        article_links = soup.find_all('a', href=lambda x: x and '/p/' in x)
        
        seen_urls = set()  # Dedup within source
        
        for link in article_links:
            article_url = link.get('href', '')
            
            # Skip if already seen
            if not article_url or article_url in seen_urls:
                continue
            
            # Make absolute URL if relative
            if article_url.startswith('/'):
                article_url = 'https://www.therundown.ai' + article_url
            
            # Skip non-https URLs
            if not article_url.startswith('https://'):
                continue
            
            seen_urls.add(article_url)
            
            # Extract title from link text or h3 parent
            title = link.get_text(strip=True)
            
            # Try to find h3 parent for better title extraction
            h3_parent = link.find_parent('h3')
            if h3_parent:
                title = h3_parent.get_text(strip=True)
            
            # Skip if no valid title
            if not title or len(title) < 3:
                continue
            
            # Try to extract description from following paragraph
            description = None
            
            # Look for description after link or in parent's next sibling
            container = link.find_parent(['div', 'article'])
            if container:
                # Find next paragraph after the title
                next_p = container.find('p')
                if next_p:
                    desc_text = next_p.get_text(strip=True)
                    # Only use if it's substantial and not the title
                    if desc_text and desc_text != title and len(desc_text) > 20:
                        description = desc_text
            
            # Extract publish date if available
            publishedAt = None
            time_elem = container.find('time') if container else None
            if time_elem and time_elem.get('datetime'):
                publishedAt = time_elem['datetime']
            
            # Look for image
            imageUrl = None
            if container:
                img = container.find('img')
                if img and img.get('src'):
                    imageUrl = img['src']
            
            article = {
                "title": title,
                "description": description,
                "url": article_url,
                "publishedAt": publishedAt,
                "imageUrl": imageUrl,
                "category": None
            }
            
            output["articles"].append(article)
        
        output["articlesFound"] = len(output["articles"])
        
        # Rate limiting - wait 2 seconds
        time.sleep(2)
        
    except requests.exceptions.RequestException as e:
        output["errors"].append(f"Network error: {str(e)}")
    except Exception as e:
        output["errors"].append(f"Unexpected error: {str(e)}")
    
    return output


if __name__ == "__main__":
    # Test the scraper
    result = scrape()
    print(json.dumps(result, indent=2))
