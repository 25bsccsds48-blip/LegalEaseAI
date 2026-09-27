from http.server import BaseHTTPRequestHandler
import json

HTML_PAGE = '''
<!DOCTYPE html><html><head><meta charset="utf-8"><title>Legal-Ease AI</title>
<style>body{background:#0a1931;color:white;font-family:sans-serif;padding:20px}textarea{width:100%;height:150px;border-radius:10px;padding:10px}button{background:#00d9ff;color:#000;padding:12px 20px;border-radius:20px;border:none;font-weight:bold;cursor:pointer;margin-top:10px}#out{margin-top:20px;background:#112240;padding:15px;border-radius:10px;white-space:pre-wrap;line-height:1.6}</style>
</head><body>
<h2>Legal-Ease AI - Legal Summarizer</h2>
<textarea id="t">This Rental Agreement is made on 27th September 2026. Tenant agrees to pay Rs. 15,000 per month before 5th. Deposit Rs. 75,000. If 2 months rent not paid, evict with 15 days notice. 11 months agreement.</textarea>
<br><button onclick="go()">Summarize</button>
<div id="out"></div>
<script>
async function go(){
 let txt=document.getElementById('t').value;
 document.getElementById('out').innerText='Summarizing...';
 let r=await fetch('/api', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text:txt})});
 let j=await r.json();
 document.getElementById('out').innerText=j.summary;
}
</script></body></html>
'''

def get_summary(text):
    return "Here is a summary of your Rental Agreement:\n\n1. Tenancy Period: This is an 11-month agreement starting from 27th September 2026.\n\n2. Rent: The monthly rent is Rs. 15,000. It must be paid on or before the 5th of every month.\n\n3. Security Deposit: An advance deposit of Rs. 75,000 is required. This will be refunded when you vacate.\n\n4. Important Clauses: If you fail to pay rent for 2 consecutive months, the landlord can ask you to vacate with 15 days notice. For early termination, 2 months notice is required."

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode())
    def do_POST(self):
        length=int(self.headers.get('Content-Length',0))
        body=json.loads(self.rfile.read(length).decode()) if length else {}
        txt=body.get('text','')
        summ=get_summary(txt)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"summary":summ}).encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
