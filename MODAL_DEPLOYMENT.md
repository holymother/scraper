# Modal Scraper Deployment Guide

## Overview
This project uses Modal to run automated scraping every 24 hours.

## Prerequisites
1. Modal account (sign up at https://modal.com)
2. Modal CLI installed: `pip install modal`
3. Modal authentication: `python3 -m modal setup`

## Files
- `modal_scraper.py` - Main Modal app with scheduled scraping
- `tools/` - Scraping modules (Ben's Bites, AI Rundown, etc.)

## Deployment

### 1. Deploy the Scheduled Scraper
```bash
modal deploy modal_scraper.py
```

This will:
- Create a Modal app called "ai-newsletter-scraper"
- Set up a daily cron job (midnight UTC)
- Create a persistent volume for storing articles
- Deploy your scraping functions to the cloud

### 2. Test the Scraper Manually
```bash
modal run modal_scraper.py
```

This runs a one-time scrape to verify everything works.

### 3. View Logs
```bash
modal app logs ai-newsletter-scraper
```

## Schedule
- **Frequency**: Every 24 hours
- **Time**: 00:00 UTC (midnight UTC)
- **Cron Expression**: `0 0 * * *`

## Data Storage
Articles are saved to a Modal Volume called `ai-newsletter-data`:
- Path: `/data/articles.json`
- Persistent across function runs
- Automatically committed after each scrape

## Retrieving Articles
To get the latest articles from your Modal volume:

```python
import modal

app = modal.App.lookup("ai-newsletter-scraper")
get_latest = modal.Function.lookup("ai-newsletter-scraper", "get_latest_articles")

with app.run():
    result = get_latest.remote()
    articles = result["articles"]
    print(f"Found {result['count']} articles")
```

## Monitoring
- View runs in Modal dashboard: https://modal.com/apps
- Check logs for each execution
- Set up alerts for failures (Modal dashboard)

## Cost
Modal free tier includes:
- $30/month free credits
- Should be sufficient for daily scraping

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate if needed
python3 -m modal setup
```

### View Active Apps
```bash
modal app list
```

### Stop Scheduled Function
```bash
modal app stop ai-newsletter-scraper
```

### Update Schedule
Edit the `schedule` parameter in `modal_scraper.py`:
```python
schedule=modal.Cron("0 */12 * * *"),  # Every 12 hours
# or
schedule=modal.Cron("0 6 * * *"),  # 6 AM UTC daily
```

Then redeploy:
```bash
modal deploy modal_scraper.py
```
