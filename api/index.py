from http.server import BaseHTTPRequestHandler
import json, os, urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"status":"Live da","endpoints":["/api/summarize","/api/chat"]}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body) if body else {}
        
        path = self.path
        text = data.get('text','')
        
        # Simple response for now - Gemini key add panna original AI varum
        if 'summarize' in path:
            result = f"Simplified: {text[:200]}... This is a legal document explained in simple words."
        else:
            result = f"AI Answer for: {text}"

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
