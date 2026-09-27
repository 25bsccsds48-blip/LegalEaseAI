import os, json, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler

HTML = """
<!DOCTYPE html><html><head><title>Legal-Ease AI</title>
<style>body{background:#0a1931;color:white;font-family:sans-serif;padding:20px}textarea{width:100%;height:150px;border-radius:10px;padding:10px}button{background:#00d9ff;color:#000;padding:12px 20px;border-radius:20px;border:none;font-weight:bold;cursor:pointer;margin-top:10px}#out{margin-top:20px;background:#112240;padding:15px;border-radius:10px;white-space:pre-wrap}</style>
</head><body>
<h2>Legal-Ease AI - Tanglish Helper</h2>
<textarea id="t">This Rental Agreement is made on 27th September 2026 between the Landlord and Tenant. The Tenant agrees to pay Rs. 15,000 per month as rent on or before 5th of every month. Security deposit of Rs. 75,000 shall be paid. If Tenant fails to pay rent for 2 consecutive months, Landlord has right to evict with 15 days notice. The agreement is for 11 months and cannot be terminated early without 2 months notice.</textarea>
<br><button onclick="go()">Summarize pannu da!</button>
<div id="out"></div>
<script>
async function go(){
 let txt=document.getElementById('t').value;
 document.getElementById('out').innerText='Loading da mama...';
 let r=await fetch('/api', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text:txt})});
 let j=await r.json();
 document.getElementById('out').innerText=j.summary;
}
</script></body></html>
"""

def call_gemini(prompt, api_key):
    for model in ["gemini-2.0-flash","gemini-2.0-flash-lite","gemini-1.5-flash","gemini-2.5-flash"]:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            data=json.dumps({"contents":[{"parts":[{"text":prompt}]}]}).encode()
            req=urllib.request.Request(url,data=data,headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=20) as r:
                res=json.loads(r.read().decode())
                return res['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            continue
    raise Exception("Gemini call fail - check API key restriction")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        try:
            length=int(self.headers.get('Content-Length',0))
            body=json.loads(self.rfile.read(length).decode())
            text=body.get('text','')[:4000]
            api_key=os.environ.get('GEMINI_API_KEY','').strip()
            if not api_key: raise Exception("GEMINI_API_KEY illa da")
            prompt=f"You are Chennai Tanglish legal explainer. Explain in casual Tanglish with mama, da, machi. Short, funny but clear risks. Doc: {text}"
            summary=call_gemini(prompt,api_key)
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"summary":summary}).encode())
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"summary":f"Error da: {str(e)[:500]}"}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
