#!/usr/bin/env python3
"""
Upload scraped articles to Supabase
Reads from .tmp/articles.json and uploads to Supabase database
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from supabase_client import SupabaseClient


def upload_articles():
    """Upload articles from local JSON to Supabase"""
    
    # Read articles from local file
    articles_file = Path(__file__).parent / ".tmp" / "articles.json"
    
    if not articles_file.exists():
        print("❌ Error: articles.json not found")
        print("💡 Run 'python3 scrape_all.py' first to generate articles")
        return False
    
    print("📖 Reading articles from .tmp/articles.json...")
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"   ✓ Found {len(articles)} articles")
    
    # Upload to Supabase
    print("\n☁️  Uploading to Supabase...")
    client = SupabaseClient()
    result = client.insert_articles(articles)
    
    if result["success"]:
        print(f"   ✅ Successfully uploaded {result['count']} articles to Supabase!")
        return True
    else:
        print(f"   ❌ Error: {result['error']}")
        return False


if __name__ == "__main__":
    print("🚀 Supabase Article Uploader\n")
    
    success = upload_articles()
    
    if success:
        print("\n✅ Upload complete!")
        print("💡 Your articles are now in the cloud and accessible from anywhere!")
    else:
        print("\n❌ Upload failed. Please check the error above.")
        sys.exit(1)
