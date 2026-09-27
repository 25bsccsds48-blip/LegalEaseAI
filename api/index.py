import os, json, urllib.request
from http.server import BaseHTTPRequestHandler

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Legal Ease AI</title>
<style>body{background:#0f172a;color:#fff;font-family:sans-serif;padding:20px}textarea{width:100%;height:140px;padding:10px;border-radius:10px}button{background:#38bdf8;color:#000;padding:12px 20px;border:none;border-radius:20px;font-weight:bold;cursor:pointer;margin-top:10px}#out{background:#1e293b;padding:15px;border-radius:10px;margin-top:15px;white-space:pre-wrap}</style>
</head><body><h2>Legal-Ease AI - Tanglish Helper</h2>
<textarea id="t" placeholder="Rental agreement ah inga paste pannu da..."></textarea><br>
<button onclick="summ()">Summarize pannu da!</button><div id="out"></div>
<script>async function summ(){let txt=document.getElementById('t').value;document.getElementById('out').innerText='AI yosikuthu da...';let r=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:txt})});let j=await r.json();document.getElementById('out').innerText=j.summary}</script></body></html>"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers()
        self.wfile.write(HTML.encode())
    def do_POST(self):
        length=int(self.headers.get('Content-Length',0))
        data=json.loads(self.rfile.read(length))
        text=data.get('text','')
        api_key=os.environ.get('GEMINI_API_KEY','').strip()
        result=""; last_err=""
        MODELS = ["gemini-2.5-flash","gemini-2.0-flash","gemini-1.5-flash","gemini-pro"]
        VERSIONS = ["v1","v1beta"]
        if not api_key:
            result="Dei mama GEMINI_API_KEY Vercel la illa da!"
        else:
            for ver in VERSIONS:
                for model in MODELS:
                    try:
                        url=f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={api_key}"
                        payload={"contents":[{"parts":[{"text":f"Summarize in Tanglish simple points: {text[:2500]}"}]}]}
                        req=urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
                        with urllib.request.urlopen(req, timeout=20) as resp:
                            res=json.loads(resp.read().decode())
                            result=res['candidates'][0]['content']['parts'][0]['text']
                            break
                    except Exception as e:
                        last_err=str(e)[:500]
                        continue
                if result: break
        if not result:
            result=f"Dei mama full fail da: {last_err} - aistudio.google.com la puthu UNRESTRICTED key eduthu Vercel la podu da!"

        self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers()
        self.wfile.write(json.dumps({"summary":result}).encode())
    def do_OPTIONS(self):
        self.send_response(200); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.end_headers()
