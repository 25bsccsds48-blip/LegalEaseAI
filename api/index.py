from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LegalEaseAI</title><style>body{font-family:sans-serif;background:#0f172a;color:white;max-width:700px;margin:40px auto;padding:20px}
textarea{width:100%;height:140px;padding:12px;border-radius:12px;background:#1e293b;color:white;border:1px solid #444}
button{background:#38bdf8;color:#000;padding:12px 24px;border-radius:10px;border:0;font-weight:bold;margin-top:10px;cursor:pointer}
#out{background:#1e293b;padding:16px;border-radius:10px;margin-top:20px;min-height:60px;white-space:pre-wrap}</style></head><body>
<h1>⚖️ LegalEaseAI</h1><p>Legal text ah simple ah puriya vekkum AI da!</p>
<textarea id="i" placeholder="Legal document ah inga paste pannu da..."></textarea><br>
<button onclick="go()">Summarize pannu da!</button><div id="out">Result inga varum da...</div>
<script>async function go(){let t=document.getElementById('i').value;if(!t){alert('Text podu da');return}
document.getElementById('out').innerText='Yosikuren da...';try{let r=await fetch('/api/index',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});let d=await r.json();document.getElementById('out').innerText=d.result||JSON.stringify(d)}catch(e){document.getElementById('out').innerText='Error: '+e}}</script>
</body></html>"""
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        try:
            import os
            length = int(self.headers.get('Content-Length',0))
            body = self.rfile.read(length)
            data = json.loads(body)
            text = data.get('text','')[:3000]
            
            # Gemini try pannuvom
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
                model = genai.GenerativeModel('gemini-1.5-flash')
                resp = model.generate_content(f'Summarize this legal doc in simple Tanglish: {text}')
                result = resp.text
            except Exception as e:
                result = f"Gemini Error da: {e}. But unga text: {text[:200]}... (API key check pannu da Vercel la)"
        except Exception as e:
            result = f"Error da: {e}"
        
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode())
