"""
Supabase client for AI Newsletter Dashboard
Handles all database operations for articles and saved items
"""

import os
from typing import List, Dict, Optional
from datetime import datetime

# Supabase credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://yrsphamotsgcngtzolwt.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlyc3BoYW1vdHNnY25ndHpvbHd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3NzUxNjYsImV4cCI6MjA4NjM1MTE2Nn0.MGll6bTRgpZW9ek2mPFFF1X6BtxdWXCWfkRd1J-Afog")


class SupabaseClient:
    """Client for interacting with Supabase database"""
    
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_ANON_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def insert_articles(self, articles: List[Dict]) -> Dict:
        """
        Insert articles into Supabase
        Uses upsert to avoid duplicates
        
        Args:
            articles: List of article dictionaries from scraper
            
        Returns:
            Result dictionary with success status and count
        """
        import requests
        
        # Transform articles to match database schema
        db_articles = []
        for article in articles:
            db_article = {
                "article_id": article.get("id"),
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "scraped_at": article.get("scrapedAt", datetime.utcnow().isoformat() + "Z"),
                "image_url": article.get("imageUrl"),
                "category": article.get("category"),
                "source": article.get("source")
            }
            db_articles.append(db_article)
        
        try:
            # Use upsert to avoid duplicates (on conflict with url)
            response = requests.post(
                f"{self.url}/rest/v1/articles",
                headers=self.headers,
                json=db_articles,
                params={"on_conflict": "url"}
            )
            
            if response.status_code in [200, 201]:
                inserted = response.json()
                return {
                    "success": True,
                    "count": len(inserted),
                    "articles": inserted
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "count": 0
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "count": 0
            }
    
    def get_articles(self, source: Optional[str] = None, limit: int = 100) -> Dict:
        """
        Fetch articles from Supabase
        
        Args:
            source: Filter by source ('bens_bites' or 'ai_rundown')
            limit: Maximum number of articles to return
            
        Returns:
            Dictionary with articles list
        """
        import requests
        
        try:
            params = {
                "select": "*",
                "order": "scraped_at.desc",
                "limit": limit
            }
            
            if source:
                params["source"] = f"eq.{source}"
            
            response = requests.get(
                f"{self.url}/rest/v1/articles",
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                articles = response.json()
                return {
                    "success": True,
                    "articles": articles,
                    "count": len(articles)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "articles": [],
                    "count": 0
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "articles": [],
                "count": 0
            }
    
    def save_article(self, article_id: str, user_id: Optional[str] = None, notes: Optional[str] = None) -> Dict:
        """
        Save/bookmark an article
        
        Args:
            article_id: UUID of the article
            user_id: Optional user ID (for future auth)
            notes: Optional user notes
            
        Returns:
            Result dictionary
        """
        import requests
        
        try:
            data = {
                "article_id": article_id,
                "user_id": user_id,
                "notes": notes
            }
            
            response = requests.post(
                f"{self.url}/rest/v1/saved_articles",
                headers=self.headers,
                json=data
            )
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "saved": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_saved_articles(self, user_id: Optional[str] = None) -> Dict:
        """
        Get all saved/bookmarked articles
        
        Args:
            user_id: Optional user ID filter
            
        Returns:
            Dictionary with saved articles
        """
        import requests
        
        try:
            params = {
                "select": "*, articles(*)",
                "order": "saved_at.desc"
            }
            
            if user_id:
                params["user_id"] = f"eq.{user_id}"
            
            response = requests.get(
                f"{self.url}/rest/v1/saved_articles",
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                saved = response.json()
                return {
                    "success": True,
                    "saved_articles": saved,
                    "count": len(saved)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "saved_articles": [],
                    "count": 0
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "saved_articles": [],
                "count": 0
            }


# Example usage
if __name__ == "__main__":
    client = SupabaseClient()
    
    # Test connection
    result = client.get_articles(limit=5)
    
    if result["success"]:
        print(f"✅ Connected to Supabase!")
        print(f"📊 Found {result['count']} articles")
    else:
        print(f"❌ Error: {result['error']}")
