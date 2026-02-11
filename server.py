#!/usr/bin/env python3
"""
Simple HTTP server for the AI Newsletter Dashboard
Serves the dashboard and allows proper loading of .tmp/articles.json
"""

import http.server
import socketserver
import sys

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    Handler = MyHTTPRequestHandler
    
    print(f"🚀 Starting AI Newsletter Dashboard Server...")
    print(f"📡 Server running at: http://localhost:{PORT}")
    print(f"🌐 Open your browser to: http://localhost:{PORT}")
    print(f"\n💡 Tip: Make sure you've run 'python3 scrape_all.py' to load articles")
    print(f"⛔ Press Ctrl+C to stop the server\n")
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
