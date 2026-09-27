from http.server import BaseHTTPRequestHandler
import json, os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>LegalEaseAI</title>
<style>body{font-family:system-ui;background:#0f172a;color:white;max-width:700px;margin:40px auto;padding:20px}
textarea{width:100%;height:120px;padding:12px;border-radius:12px;background:#1e293b;color:white;border:1px solid #334155}
button{background:#38bdf8;color:black;padding:12px 24px;border-radius:12px;border:0;font-weight:bold;cursor:pointer;margin-top:10px}
#out{background:#1e293b;padding:16px;border-radius:12px;margin-top:20px;white-space:pre-wrap}</style>
</head><body>
<h1>⚖️ LegalEaseAI</h1><p>Legal text ah simple ah puriya vekkum AI da!</p>
<textarea id="inp" placeholder="Inga unga legal document text ah paste pannunga da..."></textarea><br>
<button onclick="ask()">Summarize pannu da!</button>
<div id="out">Result inga varum da...</div>
<script>
async function ask(){
 let t=document.getElementById('inp').value;
 document.getElementById('out').innerText="Yosikiren da... ⏳";
 let r=await fetch('/api/index',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});
 let d=await r.json();
 document.getElementById('out').innerText=d.result || JSON.stringify(d);
}
</script>
</body></html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        data = json.loads(body)
        text = data.get("text","")
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Summarize this legal text in simple Tamil English mix with da: {text}"
        resp = model.generate_content(prompt)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"result": resp.text}).encode())
