from http.server import BaseHTTPRequestHandler
import json, os, urllib.request

def call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "API Key set pannala da! Vercel la add pannu!"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode())
            return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error da: {str(e)}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"status":"LegalEaseAI Full AI Live da! 🚀"}).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        data = json.loads(body) if body else {}
        text = data.get('text','')

        if 'summarize' in self.path:
            prompt = f"You are LegalEaseAI. Explain this legal text in simple Tamil + English: {text}"
        else:
            prompt = f"You are LegalEaseAI assistant. Answer: {text}"

        ai_result = call_gemini(prompt)

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"result": ai_result}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
