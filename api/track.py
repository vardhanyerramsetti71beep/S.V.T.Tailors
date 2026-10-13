import http.server
import json
import urllib.parse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db

class handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def send_json(self, status_code, payload):
        body = json.dumps(payload, default=str).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed.query)
        q = query_params.get('q', [''])[0].strip()
        if not q:
            return self.send_json(400, {"success": False, "error": "Query parameter 'q' is required"})

        try:
            results = db.get_bookings(q)
            return self.send_json(200, {"success": True, "source": "mysql", "bookings": results})
        except Exception as e:
            return self.send_json(500, {
                "success": False, 
                "error": f"MySQL database error: {str(e)}"
            })
