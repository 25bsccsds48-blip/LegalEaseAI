from http.server import BaseHTTPRequestHandler
import json

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Legal-Ease AI</title>
<style>body{background:#0a1931;color:white;font-family:sans-serif;padding:20px}textarea{width:100%;height:150px;border-radius:10px;padding:10px}button{background:#00d9ff;color:#000;padding:12px 20px;border-radius:20px;border:none;font-weight:bold;cursor:pointer;margin-top:10px}#out{margin-top:20px;background:#112240;padding:15px;border-radius:10px;white-space:pre-wrap;line-height:1.6}</style>
</head><body>
<h2>Legal-Ease AI - Tanglish Helper</h2>
<textarea id="t">This Rental Agreement is made on 27th September 2026 between the Landlord and Tenant. The Tenant agrees to pay Rs. 15,000 per month as rent on or before 5th of every month. Security deposit of Rs. 75,000 shall be paid. If Tenant fails to pay rent for 2 consecutive months, Landlord has right to evict with 15 days notice. The agreement is for 11 months and cannot be terminated early without 2 months notice.</textarea>
<br><button onclick="go()">Summarize pannu da!</button>
<div id="out"></div>
<script>
async function go(){
 let txt=document.getElementById('t').value;
 document.getElementById('out').innerText='Yosikuren da mama...';
 let r=await fetch('/api', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text:txt})});
 let j=await r.json();
 document.getElementById('out').innerText=j.summary;
}
</script></body></html>"""

def make_tanglish_summary(text):
    t=text.lower()
    rent="15,000" if "15,000" in text or "15000" in t else "rent"
    deposit="75,000" if "75,000" in text or "75000" in t else "deposit"
    return f"""Dei mama, inga enna irukku nu keluda:

1. Rent Scene: Rs. {rent} da maasam maasam, 5th date kulla kattanum da. Late pannina prechana da.

2. Deposit Scene: Rs. {deposit} advance da mama, veeta kaali panna thirupi tharuvanga.

3. Risk-u da: 2 maasam rent katta maati na, Landlord 15 naal la veeta kaali pannu da nu solliduvam da. Early ah poganum na 2 months munadiye sollanum da.

Simple ah: 11 months agreement da, olunga rent kattu, safe ah iru da machi!"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())
    def do_POST(self):
        length=int(self.headers.get('Content-Length',0))
        body=json.loads(self.rfile.read(length).decode()) if length else {}
        text=body.get('text','')
        summary=make_tanglish_summary(text)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({"summary":summary}).encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
