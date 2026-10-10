import http.server
import socketserver
import os
import sys
import json
import urllib.parse
import webbrowser

# Ensure stdout and stderr exist for background/headless run
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')

import db

PORT = 8080
FALLBACK_FILE = os.path.join(os.path.dirname(__file__), 'local_bookings.json')

def save_to_fallback(data):
    records = []
    if os.path.exists(FALLBACK_FILE):
        try:
            with open(FALLBACK_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
        except Exception:
            records = []
    data['created_at_fallback'] = data.get('created_at') or 'now'
    data['booking_id'] = len(records) + 1001
    records.insert(0, data)
    with open(FALLBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
    return data['booking_id']

class TailorHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        try:
            super().log_message(format, *args)
        except Exception:
            pass

    def end_headers(self):
        # Enable caching-free headers for lively development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def send_json(self, status_code, payload):
        body = json.dumps(payload).encode('utf-8')
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

        if path == '/api/db-test':
            res = db.test_connection()
            return self.send_json(200 if res['success'] else 500, res)

        elif path == '/api/track':
            query_params = urllib.parse.parse_qs(parsed.query)
            q = query_params.get('q', [''])[0].strip()
            if not q:
                return self.send_json(400, {"success": False, "error": "Query parameter 'q' is required"})

            try:
                results = db.get_bookings(q)
                return self.send_json(200, {"success": True, "source": "mysql", "bookings": results})
            except Exception as e:
                # Search fallback if DB is not reachable
                fallback_results = []
                if os.path.exists(FALLBACK_FILE):
                    try:
                        with open(FALLBACK_FILE, 'r', encoding='utf-8') as f:
                            all_fb = json.load(f)
                            for item in all_fb:
                                if q in str(item.get('mobile', '')) or q == str(item.get('booking_id', '')) or q.lower() in str(item.get('name', '')).lower():
                                    fallback_results.append(item)
                    except Exception:
                        pass
                return self.send_json(200, {
                    "success": True, 
                    "source": "fallback", 
                    "warning": f"MySQL offline: {str(e)}", 
                    "bookings": fallback_results
                })

        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/register':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            try:
                data = json.loads(raw_body.decode('utf-8'))
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
                status_code = 200 if (res.get('success') or res.get('already_exists')) else 400
                return self.send_json(status_code, res)
            except Exception as e:
                print(f"[Register Notice] DB error ({e}), saving to local fallback.")
                fb_id = save_to_fallback({
                    "name": name,
                    "mobile": mobile,
                    "locality": locality,
                    "username": username,
                    "pref_date": pref_date,
                    "pref_time": pref_time,
                    "garments": garments
                })
                return self.send_json(200, {
                    "success": True,
                    "saved_locally": True,
                    "booking_id": fb_id,
                    "user": {"name": name, "mobile": mobile, "username": username, "locality": locality},
                    "message": "Account registered (local queue). Configure MySQL password in db_config.json."
                })

        elif self.path == '/api/login':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            try:
                data = json.loads(raw_body.decode('utf-8'))
            except Exception as e:
                return self.send_json(400, {"success": False, "error": f"Invalid JSON: {e}"})

            username = data.get('username', '')
            password = data.get('password', '')

            try:
                res = db.login_user(username, password)
                status_code = 200 if res.get('success') else 401
                return self.send_json(status_code, res)
            except Exception as e:
                return self.send_json(500, {
                    "success": False,
                    "error": f"Database login error: {e}. Please ensure password in db_config.json is set."
                })

        elif self.path == '/api/reset-password':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            try:
                data = json.loads(raw_body.decode('utf-8'))
            except Exception as e:
                return self.send_json(400, {"success": False, "error": f"Invalid JSON: {e}"})

            identifier = data.get('identifier') or data.get('username') or data.get('mobile', '')
            new_password = data.get('new_password') or data.get('password', '')

            try:
                res = db.reset_password(identifier, new_password)
                status_code = 200 if res.get('success') else 400
                return self.send_json(status_code, res)
            except Exception as e:
                return self.send_json(500, {
                    "success": False,
                    "error": f"Password reset error: {e}"
                })

        elif self.path == '/api/bookings':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            try:
                data = json.loads(raw_body.decode('utf-8'))
            except Exception as e:
                return self.send_json(400, {"success": False, "error": f"Invalid JSON: {e}"})

            name = data.get('name', 'Valued Customer')
            mobile = data.get('mobile', '')
            locality = data.get('locality', 'Governorpet, Vijayawada')
            pref_date = data.get('pref_date', '')
            pref_time = data.get('pref_time', '')
            garnments = data.get('garnments') or data.get('garments') or 'Bespoke Garments'
            shirt_size = data.get('shirt_size')
            pant_size = data.get('pant_size')

            if not mobile:
                return self.send_json(400, {"success": False, "error": "Mobile number is required"})

            try:
                # Try saving directly to MySQL customers database
                res = db.save_booking(
                    name=name,
                    mobile=mobile,
                    locality=locality,
                    pref_date=pref_date,
                    pref_time=pref_time,
                    garnments=garnments,
                    garments=garnments,
                    shirt_size=shirt_size,
                    pant_size=pant_size
                )
                print(f"[MySQL Success] Saved booking #{res['booking_id']} for user #{res['user_id']} ({name})")
                return self.send_json(200, res)
            except Exception as e:
                # Fallback storage so no customer order is ever dropped
                print(f"[MySQL Notice] Could not save directly to MySQL ({e}). Saving to local cache.")
                fb_id = save_to_fallback({
                    "name": name,
                    "mobile": mobile,
                    "locality": locality,
                    "pref_date": pref_date,
                    "pref_time": pref_time,
                    "garments": garnments,
                    "shirt_size": shirt_size,
                    "pant_size": pant_size
                })
                return self.send_json(200, {
                    "success": True,
                    "saved_locally": True,
                    "booking_id": fb_id,
                    "warning": f"Saved in local queue. Please configure password in db_config.json: {e}"
                })

        return self.send_json(404, {"error": "Not Found"})

if __name__ == '__main__':
    reconfigure_stdout = getattr(sys.stdout, 'reconfigure', None)
    if callable(reconfigure_stdout):
        reconfigure_stdout(encoding='utf-8', errors='replace')

    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    # Check DB status on startup
    db_test = db.test_connection()
    if db_test['success']:
        print(" Connected to MySQL database 'customers' successfully!")
        try:
            db.init_db()
            print(" Verified MySQL tables: user, bookings, measurements.")
        except Exception as e:
            print(f" Notice checking tables: {e}")
    else:
        print(f" MySQL Notice: {db_test.get('error')}")
        print("  Edit 'db_config.json' with your MySQL password to link live.")

    httpd = None
    for port_attempt in [8080, 8081, 8082, 3000, 5000, 8088]:
        try:
            httpd = socketserver.TCPServer(("", port_attempt), TailorHandler)
            PORT = port_attempt
            break
        except OSError:
            continue
            
    if not httpd:
        print("Could not bind to any port.")
        sys.exit(1)

    url = f"http://localhost:{PORT}"
    print("==================================================================")
    print(" S. V. T. TAILORS - FULL STACK ATELIER SERVER IS LIVE!")
    print(f" Database Integration: MySQL 'customers' (user, bookings, measurements)")
    print(f" API Endpoints: POST /api/bookings | GET /api/track | GET /api/db-test")
    print(f" Open in your browser: {url}")
    print(f" WhatsApp & Phone Helpline: +91 98481 33417")
    print(f" Google Maps: https://maps.app.goo.gl/tUgrhQhHEAkgGBXQ7")
    print("==================================================================")
    
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
