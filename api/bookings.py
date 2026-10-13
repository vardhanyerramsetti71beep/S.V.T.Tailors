import http.server
import json
import urllib.parse
import os
import sys

# Ensure parent directory is in sys.path so db can be imported
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
        query_params = urllib.parse.parse_qs(parsed.query)
        q = query_params.get('q', [''])[0].strip()
        try:
            results = db.get_bookings(q)
            return self.send_json(200, {"success": True, "source": "mysql", "bookings": results})
        except Exception as e:
            return self.send_json(500, {"success": False, "error": str(e)})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)
        try:
            data = json.loads(raw_body.decode('utf-8')) if raw_body else {}
        except Exception as e:
            return self.send_json(400, {"success": False, "error": f"Invalid JSON: {e}"})

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
            # Return HTTP 201 Created
            return self.send_json(201, res)
        except Exception as e:
            return self.send_json(500, {
                "success": False,
                "error": f"MySQL Database error: Could not save booking ({str(e)})"
            })
