#!/usr/bin/env python3
"""
24-Hour Filter
Filters articles to only those published in the last 24 hours
"""

from datetime import datetime, timedelta
import json


def filter_24h(articles):
    """
    Filter articles to only those within the last 24 hours
    
    Args:
        articles (list): List of article dictionaries
        
    Returns:
        list: Filtered articles
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=24)
    
    filtered = []
    
    for article in articles:
        published_at = article.get('publishedAt')
        scraped_at = article.get('scrapedAt')
        
        # Use publishedAt if available, otherwise scrapedAt as fallback
        timestamp_str = published_at or scraped_at
        
        if not timestamp_str:
            # If no timestamp, include it (assume recent)
            filtered.append(article)
            continue
        
        try:
            # Parse ISO 8601 timestamp
            # Remove 'Z' suffix and parse
            timestamp_str = timestamp_str.replace('Z', '+00:00')
            timestamp = datetime.fromisoformat(timestamp_str.replace('+00:00', ''))
            
            # Check if within 24 hours
            if timestamp >= cutoff:
                filtered.append(article)
        except ValueError:
            # If parsing fails, include the article (benefit of doubt)
            filtered.append(article)
    
    return filtered


if __name__ == "__main__":
    # Test with sample data
    test_articles = [
        {
            "title": "Recent article",
            "publishedAt": datetime.utcnow().isoformat() + "Z",
            "url": "https://example.com/1"
        },
        {
            "title": "Old article",
            "publishedAt": (datetime.utcnow() - timedelta(hours=48)).isoformat() + "Z",
            "url": "https://example.com/2"
        },
        {
            "title": "No timestamp",
            "publishedAt": None,
            "url": "https://example.com/3"
        }
    ]
    
    result = filter_24h(test_articles)
    print(f"Filtered {len(result)} articles from {len(test_articles)}")
    print(json.dumps(result, indent=2))
