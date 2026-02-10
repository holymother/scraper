#!/usr/bin/env python3
"""
Ben's Bites Scraper
Scrapes latest articles from Ben's Bites archive page
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json


def scrape():
    """
    Scrape Ben's Bites archive for latest articles
    
    Returns:
        dict: Scraper output matching schema
    """
    output = {
        "source": "bens_bites",
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
        
        # Fetch archive page
        url = "https://www.bensbites.com/archive"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article links
        # Ben's Bites structure: Links to /p/ are articles
        article_links = soup.find_all('a', href=lambda x: x and '/p/' in x)
        
        seen_urls = set()  # Dedup within source
        
        for link in article_links:
            article_url = link.get('href', '')
            
            # Skip if already seen or not a valid article URL
            if not article_url or article_url in seen_urls:
                continue
                
            # Make absolute URL if relative
            if article_url.startswith('/'):
                article_url = 'https://www.bensbites.com' + article_url
            
            # Skip non-https URLs
            if not article_url.startswith('https://'):
                continue
            
            seen_urls.add(article_url)
            
            # Extract title (link text)
            title = link.get_text(strip=True)
            
            # Skip if no title
            if not title or len(title) < 3:
                continue
            
            # Try to extract description from next sibling
            description = None
            next_elem = link.find_next_sibling()
            if next_elem and next_elem.name in ['p', 'div']:
                desc_text = next_elem.get_text(strip=True)
                if desc_text and desc_text != title:
                    description = desc_text
            
            # Estimate publish date - for now use scrapeAt
            # (Ben's Bites doesn't have explicit dates on archive page)
            publishedAt = None
            
            # Look for image
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
                "publishedAt": publishedAt,
                "imageUrl": imageUrl,
                "category": None
            }
            
            output["articles"].append(article)
        
        output["articlesFound"] = len(output["articles"])
        
        # Rate limiting - wait 2 seconds if we need to make another request
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
