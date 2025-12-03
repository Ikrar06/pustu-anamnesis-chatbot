#!/usr/bin/env python3
"""
Simple HTTP server untuk serve index.html
Run: python serve.py
"""

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server berjalan di http://localhost:{PORT}")
    print(f"Buka browser dan akses: http://localhost:{PORT}/index.html")
    print("Tekan CTRL+C untuk stop server")
    httpd.serve_forever()
