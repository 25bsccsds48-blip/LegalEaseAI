import os, json, urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length',0))
        data = json.loads(self.rfile.read(length))
        text = data.get('text','')
        api_key = os.environ.get('GEMINI_API_KEY','').strip()
        result = ""
        try:
            if api_key:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Explain this legal text in simple Tanglish for common man: {text[:2000]}"}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    res = json.loads(resp.read().decode())
                    result = res['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            result = f"Error: {str(e)[:200]}"

        if not result:
            result = "Dei mama, API key error da. Vercel la GEMINI_API_KEY check pannu da!"

        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"summary": result}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
