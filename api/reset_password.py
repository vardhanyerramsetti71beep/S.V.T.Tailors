import http.server
import json
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
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)
        try:
            data = json.loads(raw_body.decode('utf-8')) if raw_body else {}
        except Exception as e:
            return self.send_json(400, {"success": False, "error": f"Invalid JSON: {e}"})

        identifier = data.get('identifier') or data.get('username') or data.get('mobile', '')
        new_password = data.get('new_password') or data.get('password', '')

        if not identifier or not new_password:
            return self.send_json(400, {"success": False, "error": "Identifier and new password are required"})

        try:
            res = db.reset_password(identifier, new_password)
            status_code = 200 if res.get('success') else 400
            return self.send_json(status_code, res)
        except Exception as e:
            return self.send_json(500, {"success": False, "error": str(e)})
