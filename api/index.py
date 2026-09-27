import os
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

def call_gemini(prompt, api_key):
    # NEW 2026 MODELS - 100% working
    models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-2.5-flash"]
    last_err = ""
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            data = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                res = json.loads(r.read().decode())
                return res['candidates'][0]['content']['parts'][0]['text']
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode()
            except:
                body = str(e)
            last_err = f"{e.code} {e.reason} - {body[:400]}"
            continue
        except Exception as e:
            last_err = str(e)[:400]
            continue
    raise Exception(last_err)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode())
            text = body.get('text','')[:4000]
            api_key = os.environ.get('GEMINI_API_KEY','').strip()
            if not api_key:
                raise Exception("GEMINI_API_KEY not found in Vercel - Redeploy pannala!")

            prompt = f"""You are Chennai Tanglish legal explainer. Explain this rental agreement in super casual Chennai Tanglish like talking to a friend (mama, da, machi). Make it short, funny but clear about risks. Keep numbers like 15000, 75000, 5th, 2 months, 15 days. Document: {text}"""

            summary = call_gemini(prompt, api_key)

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"summary": summary}).encode())
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"summary": f"Dei mama error da: {str(e)[:500]}"}).encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
