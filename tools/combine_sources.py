#!/usr/bin/env python3
"""
Combine Sources
Merges articles from multiple scrapers, deduplicates, and generates UUIDs
"""

import json
import uuid
from datetime import datetime


def combine_sources(scraper_outputs):
    """
    Combine multiple scraper outputs into a single unified list
    
    Args:
        scraper_outputs (list): List of scraper output dictionaries
        
    Returns:
        list: Combined and deduplicated articles with UUIDs
    """
    all_articles = []
    seen_urls = set()
    
    for output in scraper_outputs:
        source = output.get('source', 'unknown')
        scraped_at = output.get('scrapedAt', datetime.utcnow().isoformat() + 'Z')
        
        for article in output.get('articles', []):
            url = article.get('url')
            
            # Skip duplicates
            if not url or url in seen_urls:
                continue
            
            seen_urls.add(url)
            
            # Add UUID and metadata
            unified_article = {
                "id": str(uuid.uuid4()),
                "title": article.get('title', 'Untitled'),
                "description": article.get('description'),
                "url": url,
                "source": source,
                "publishedAt": article.get('publishedAt'),
                "scrapedAt": scraped_at,
                "imageUrl": article.get('imageUrl'),
                "category": article.get('category'),
                "saved": False,
                "savedAt": None
            }
            
            all_articles.append(unified_article)
    
    # Sort by publishedAt (newest first), fallback to scrapedAt
    all_articles.sort(key=lambda x: x.get('publishedAt') or x.get('scrapedAt'), reverse=True)
    
    return all_articles


if __name__ == "__main__":
    # Test with sample data
    test_outputs = [
        {
            "source": "bens_bites",
            "scrapedAt": "2026-02-08T20:00:00Z",
            "articles": [
                {"title": "Article 1", "url": "https://example.com/1", "description": "Test"},
                {"title": "Article 2", "url": "https://example.com/2", "description": "Test 2"}
            ]
        },
        {
            "source": "ai_rundown",
            "scrapedAt": "2026-02-08T20:00:00Z",
            "articles": [
                {"title": "Article 3", "url": "https://example.com/3", "description": "Test 3"},
                {"title": "Duplicate", "url": "https://example.com/1", "description": "Dup"}
            ]
        }
    ]
    
    result = combine_sources(test_outputs)
    print(f"Combined into {len(result)} unique articles")
    print(json.dumps(result, indent=2))
