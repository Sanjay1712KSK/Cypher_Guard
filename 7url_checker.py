from fastapi import FastAPI
from pydantic import BaseModel
import requests
import ssl
import socket
from urllib.parse import urlparse
app = FastAPI(title="Payment URL Safety Checker")
VIRUSTOTAL_API_KEY = "40b1b795ed5ea8c5a7b3328a31d1241f7c9f5a14c91b85241a6b0165aa3ec78d"
class URLRequest(BaseModel):
    url: str
def simple_domain_check(url):
    result = {"https": False, "suspicious_domain": False}
    parsed = urlparse(url)
    if parsed.scheme.startswith("https"):
        result["https"] = True
    if "-" in parsed.netloc or len(parsed.netloc.split(".")) > 3:
        result["suspicious_domain"] = True
    return result
def check_ssl(url):
    hostname = urlparse(url).hostname
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
        return True
    except Exception:
        return False
def virustotal_check(url):
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url},
            timeout=10
        )
        if response.status_code != 200:
            return None  
        url_id = response.json()["data"]["id"]
        analysis_resp = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{url_id}",
            headers=headers,
            timeout=10
        )
        if analysis_resp.status_code != 200:
            return None
        analysis_data = analysis_resp.json()["data"]["attributes"]["stats"]
        if analysis_data["malicious"] > 0 or analysis_data["suspicious"] > 0:
            return True
        else:
            return False
    except Exception:
        return None
@app.post("/check-url")
def check_url(request: URLRequest):
    url = request.url
    domain_result = simple_domain_check(url)
    ssl_result = check_ssl(url)
    vt_result = virustotal_check(url)
    if vt_result is True or not domain_result["https"] or domain_result["suspicious_domain"] or ssl_result is False:
        verdict = "⚠️ Unsafe / Suspicious"
    elif vt_result is None:
        verdict = "❔ Unknown (VirusTotal check failed)"
    else:
        verdict = "✅ Safe"
    return {
        "url": url,
        "https": domain_result["https"],
        "suspicious_domain": domain_result["suspicious_domain"],
        "ssl_valid": ssl_result,
        "virustotal_flag": vt_result,
        "verdict": verdict
    }
