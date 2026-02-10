#!/usr/bin/env python3
"""
Main Scraping Orchestration Script
Runs all scrapers, combines sources, filters to 24h, and outputs to JSON
"""

import sys
import os
import json
from datetime import datetime

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

import scrape_bensbites
import scrape_airundown
from filter_24h import filter_24h
from combine_sources import combine_sources


def main():
    """
    Main orchestration function
    """
    print("🚀 Starting AI Newsletter Scraper...")
    print(f"⏰ Timestamp: {datetime.utcnow().isoformat()}Z\n")
    
    # Step 1: Scrape Ben's Bites
    print("📰 Scraping Ben's Bites...")
    bensbites_output = scrape_bensbites.scrape()
    print(f"   ✓ Found {bensbites_output['articlesFound']} articles")
    if bensbites_output['errors']:
        print(f"   ⚠️  Errors: {bensbites_output['errors']}")
    
    # Step 2: Scrape The AI Rundown
    print("\n📰 Scraping The AI Rundown...")
    airundown_output = scrape_airundown.scrape()
    print(f"   ✓ Found {airundown_output['articlesFound']} articles")
    if airundown_output['errors']:
        print(f"   ⚠️  Errors: {airundown_output['errors']}")
    
    # Step 3: Combine sources
    print("\n🔗 Combining sources...")
    all_scraper_outputs = [bensbites_output, airundown_output]
    combined_articles = combine_sources(all_scraper_outputs)
    print(f"   ✓ Combined into {len(combined_articles)} unique articles")
    
    # Step 4: Filter to 24 hours
    print("\n⏳ Filtering to last 24 hours...")
    filtered_articles = filter_24h(combined_articles)
    print(f"   ✓ Filtered to {len(filtered_articles)} recent articles")
    
    # Step 5: Save to .tmp/articles.json
    output_path = os.path.join('.tmp', 'articles.json')
    os.makedirs('.tmp', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {output_path}")
    
    # Step 6: Create log file
    log_dir = os.path.join('.tmp', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_filename = f"scrape_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sources": {
            "bens_bites": {
                "found": bensbites_output['articlesFound'],
                "errors": bensbites_output['errors']
            },
            "ai_rundown": {
                "found": airundown_output['articlesFound'],
                "errors": airundown_output['errors']
            }
        },
        "total_combined": len(combined_articles),
        "total_filtered": len(filtered_articles),
        "output_path": output_path
    }
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)
    
    print(f"📝 Log saved to: {log_path}")
    
    print("\n✅ Scraping complete!")
    return filtered_articles


if __name__ == "__main__":
    try:
        articles = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
