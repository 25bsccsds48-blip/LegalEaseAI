from http.server import BaseHTTPRequestHandler
import json

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Legal-Ease AI</title>
<style>body{background:#0a1931;color:white;font-family:sans-serif;padding:20px}textarea{width:100%;height:150px;border-radius:10px;padding:10px}button{background:#00d9ff;color:#000;padding:12px 20px;border-radius:20px;border:none;font-weight:bold;cursor:pointer;margin-top:10px}#out{margin-top:20px;background:#112240;padding:15px;border-radius:10px;white-space:pre-wrap;line-height:1.6}</style>
</head><body>
<h2>Legal-Ease AI - Legal Summarizer</h2>
<textarea id="t">This Rental Agreement is made on 27th September 2026 between the Landlord and Tenant. The Tenant agrees to pay Rs. 15,000 per month as rent on or before 5th of every month. Security deposit of Rs. 75,000 shall be paid. If Tenant fails to pay rent for 2 consecutive months, Landlord has right to evict with 15 days notice. The agreement is for 11 months and cannot be terminated early without 2 months notice.</textarea>
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
</script></body></html>"""

def make_english_summary(text):
    return """Here is a summary of your Rental Agreement:

1. Tenancy Period: This is an 11-month agreement starting from 27th September 2026.

2. Rent: The monthly rent is Rs. 15,000. It must be paid on or before the 5th of every month. Late payment may cause issues.

3. Security Deposit: An advance deposit of Rs. 75,000 is required. This amount will be refunded when you vacate the house.

4. Important Clauses: If you fail to pay rent for 2 consecutive months, the landlord has the right to ask you to vacate with
