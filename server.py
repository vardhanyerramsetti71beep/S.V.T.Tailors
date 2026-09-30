import http.server
import socketserver
import os
import sys
import webbrowser

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable caching-free headers for lively local development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    reconfigure_stdout = getattr(sys.stdout, 'reconfigure', None)
    if callable(reconfigure_stdout):
        reconfigure_stdout(encoding='utf-8', errors='replace')

    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    httpd = None
    for port_attempt in [8080, 8081, 8082, 3000, 5000, 8088]:
        try:
            httpd = socketserver.TCPServer(("", port_attempt), Handler)
            PORT = port_attempt
            break
        except OSError:
            continue
            
    if not httpd:
        print("Could not bind to any port.")
        sys.exit(1)

    url = f"http://localhost:{PORT}"
    print("==================================================================")
    print("🧵 S. V. T. TAILORS - OFFICIAL WEBSITE SERVER IS LIVE!")
    print(f"📍 Location: Eluru Road, near Ram Mandiram, Governorpet, Vijayawada")
    print(f"🌐 Open in your browser: {url}")
    print(f"📞 WhatsApp & Phone Helpline: +91 98481 33417")
    print(f"🗺️  Google Maps: https://maps.app.goo.gl/tUgrhQhHEAkgGBXQ7")
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
