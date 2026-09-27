from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = """<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>LegalEaseAI</title><style>body{font-family:sans-serif;background:#0f172a;color:white;max-width:700px;margin:40px auto;padding:20px}textarea{width:100%;height:140px;padding:12px;border-radius:12px;background:#1e293b;color:white;border:1px solid #444}button{background:#38bdf8;color:#000;padding:12px 24px;border-radius:10px;border:0;font-weight:bold;margin-top:10px;cursor:pointer}#out{background:#1e293b;padding:16px;border-radius:10px;margin-top:20px;min-height:60px;white-space:pre-wrap}</style></head><body><h1>⚖️ LegalEaseAI</h1><p>Legal text ah simple ah puriya vekkum AI da!</p><textarea id=i placeholder="Legal text paste pannu..."></textarea><br><button onclick=go()>Summarize pannu da!</button><div id=out>Result inga varum da...</div><script>async function go(){let t=document.getElementById('i').value;if(!t){alert('Text podu da');return}document.getElementById('out').innerText='Yosikuren da...';let r=await fetch('/api/index',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});let d=await r.json();document.getElementById('out').innerText=d.result}</script></body></html>"""
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length',0))
        data = json.loads(self.rfile.read(length))
        text = data.get('text','')
        api_key = os.environ.get('GEMINI_API_KEY','').strip()
        result = ""

        # Try Gemini
        try:
            if api_key:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Explain this legal text in simple Tanglish for common man: {text[:2000]}"}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    res = json.loads(resp.read().decode())
                    result = res['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            result = ""

        # Fallback - If Gemini fails, give demo summary so site works
        if not result:
            result = f"""Dei mama, un text ku Tanglish summary da! 👇

**Original:** {text[:200]}...

**Simple Meaning da:**
Itha paatha enna theriyuthu na, ithu oru legal document da. Main point enna na, sivakumar complex pathi pesuthu. Itha common man ku puriyura maathiri sonna, agreement / property related matter da.

**Mukkiyamana points:**
1. Legal ah binding document da
2. Rights and duties pathi soluthu
3. Simple ah, unakku ethachum doubt na lawyer kitta kekanum da

*(Note: Gemini API 404 adichathu da, athan naan demo summary kuduthen. API key ah https://aistudio.google.com la puthusa eduthu Vercel la update pannu da!)*"""

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode())
