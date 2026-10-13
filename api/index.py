import http.server
import json
import urllib.parse
import os
import sys

# Ensure parent directory is in python module search path
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.endswith('/api/db-test') or path == '/api/db-test':
            res = db.test_connection()
            return self.send_json(200 if res['success'] else 500, res)

        elif path.endswith('/api/track') or path == '/api/track':
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

        return self.send_json(404, {"error": "API route not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)
        try:
            data = json.loads(raw_body.decode('utf-8')) if raw_body else {}
        except Exception as e:
            return self.send_json(400, {"success": False, "error": f"Invalid JSON: {e}"})

        if path.endswith('/api/register') or path == '/api/register':
            name = data.get('name', 'Valued Customer')
            mobile = data.get('mobile', '')
            locality = data.get('locality', 'Governorpet, Vijayawada')
            username = data.get('username', '')
            password = data.get('password', '')
            pref_date = data.get('pref_date', '')
            pref_time = data.get('pref_time', '')
            garments = data.get('garments', 'Bespoke Fitting')

            if not mobile and not username:
                return self.send_json(400, {"success": False, "error": "Mobile number or username is required"})

            try:
                res = db.register_user(
                    name=name,
                    mobile=mobile,
                    locality=locality,
                    username=username,
                    password=password,
                    pref_date=pref_date,
                    pref_time=pref_time,
                    garments=garments
                )
                status_code = 200 if (res.get('success') or res.get('already_exists')) else 400
                return self.send_json(status_code, res)
            except Exception as e:
                return self.send_json(500, {
                    "success": False,
                    "error": f"MySQL Database error: Could not register user ({str(e)})"
                })

        elif path.endswith('/api/login') or path == '/api/login':
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()

            if not username or not password:
                return self.send_json(400, {"success": False, "error": "Username/mobile and password are required"})

            try:
                res = db.login_user(username, password)
                status_code = 200 if res.get('success') else 401
                return self.send_json(status_code, res)
            except Exception as e:
                return self.send_json(500, {
                    "success": False,
                    "error": f"Database login error: {e}. Please ensure credentials in .env are set."
                })

        elif path.endswith('/api/reset-password') or path == '/api/reset-password':
            identifier = data.get('identifier', '').strip()
            new_password = data.get('new_password', '').strip()

            if not identifier or not new_password:
                return self.send_json(400, {"success": False, "error": "Identifier and new password are required"})

            try:
                res = db.reset_password(identifier, new_password)
                status_code = 200 if res.get('success') else 400
                return self.send_json(status_code, res)
            except Exception as e:
                return self.send_json(500, {"success": False, "error": str(e)})

        elif path.endswith('/api/bookings') or path == '/api/bookings':
            name = data.get('name', 'Bespoke Patron')
            mobile = data.get('mobile', '')
            locality = data.get('locality', 'Governorpet, Vijayawada')
            pref_date = data.get('pref_date', '')
            pref_time = data.get('pref_time', '')
            garments = data.get('garnments') or data.get('garments') or 'Custom Tailoring Order'
            shirt_size = data.get('shirt_size')
            pant_size = data.get('pant_size')

            if not mobile:
                return self.send_json(400, {"success": False, "error": "Mobile number is required"})

            try:
                res = db.save_booking(
                    name=name,
                    mobile=mobile,
                    locality=locality,
                    pref_date=pref_date,
                    pref_time=pref_time,
                    garments=garments,
                    shirt_size=shirt_size,
                    pant_size=pant_size
                )
                return self.send_json(200, res)
            except Exception as e:
                return self.send_json(500, {
                    "success": False,
                    "error": f"MySQL Database error: Could not save booking ({str(e)})"
                })

        return self.send_json(404, {"error": "API route not found"})
