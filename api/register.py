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

        name = data.get('name', 'Valued Customer')
        mobile = data.get('mobile', '')
        locality = data.get('locality', 'Governorpet, Vijayawada')
        username = data.get('username', '')
        password = data.get('password', '')
        pref_date = data.get('pref_date', '')
        pref_time = data.get('pref_time', '')
        garments = data.get('garments') or data.get('garnments') or ''
        shirt_size = data.get('shirt_size')
        pant_size = data.get('pant_size')

        try:
            res = db.register_user(
                name=name,
                mobile=mobile,
                locality=locality,
                username=username,
                password=password,
                pref_date=pref_date,
                pref_time=pref_time,
                garments=garments,
                shirt_size=shirt_size,
                pant_size=pant_size
            )
            status_code = 201 if res.get('success') else (200 if res.get('already_exists') else 400)
            return self.send_json(status_code, res)
        except Exception as e:
            return self.send_json(500, {
                "success": False,
                "error": f"MySQL Database error: Could not register user ({str(e)})"
            })
