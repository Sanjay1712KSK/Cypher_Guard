from fastapi import FastAPI
from pydantic import BaseModel
import requests
import ssl
import socket
import os
import time
from urllib.parse import urlparse
app = FastAPI(title="Payment URL Safety Checker")

# Read VirusTotal API key from environment variable
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
class URLRequest(BaseModel):
    url: str

def normalize_url(url: str) -> str:
    """Add https:// scheme if missing"""
    if not url.startswith(('http://', 'https://')):
        return f"https://{url}"
    return url
def simple_domain_check(url):
    result = {"https": False, "suspicious_domain": False}
    parsed = urlparse(url)
    if parsed.scheme.startswith("https"):
        result["https"] = True
    if "-" in parsed.netloc or len(parsed.netloc.split(".")) > 3:
        result["suspicious_domain"] = True
    return result
def check_ssl(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
        return True
    except Exception:
        return False
def virustotal_check(url):
    if not VIRUSTOTAL_API_KEY:
        return None, None, None  # vt_result, vt_status, vt_stats
    
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        # Submit URL for analysis
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url},
            timeout=10
        )
        if response.status_code != 200:
            return None, None, None
            
        url_id = response.json()["data"]["id"]
        
        # Poll for analysis completion (up to ~10 seconds)
        max_attempts = 10
        for attempt in range(max_attempts):
            analysis_resp = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{url_id}",
                headers=headers,
                timeout=10
            )
            if analysis_resp.status_code != 200:
                return None, None, None
                
            analysis_data = analysis_resp.json()["data"]["attributes"]
            status = analysis_data.get("status")
            
            if status == "completed":
                stats = analysis_data.get("stats", {})
                if stats.get("malicious", 0) > 0 or stats.get("suspicious", 0) > 0:
                    return True, status, stats
                else:
                    return False, status, stats
            elif status in ["queued", "running"]:
                if attempt < max_attempts - 1:  # Don't sleep on last attempt
                    time.sleep(1)
                continue
            else:
                # Unknown status
                return None, status, None
                
        # Timeout reached, analysis still not complete
        return None, "timeout", None
        
    except Exception:
        return None, None, None
@app.post("/check-url")
def check_url(request: URLRequest):
    # Normalize URL to add scheme if missing
    url = normalize_url(request.url)
    
    domain_result = simple_domain_check(url)
    ssl_result = check_ssl(url)
    vt_result, vt_status, vt_stats = virustotal_check(url)
    
    # Determine verdict based on checks
    if vt_result is True or not domain_result["https"] or domain_result["suspicious_domain"] or ssl_result is False:
        verdict = "⚠️ Unsafe / Suspicious"
    elif vt_result is None:
        verdict = "❔ Unknown (VirusTotal check failed)"
    else:
        verdict = "✅ Safe"
    
    # Build response with debug fields
    response = {
        "url": url,
        "https": domain_result["https"],
        "suspicious_domain": domain_result["suspicious_domain"],
        "ssl_valid": ssl_result,
        "virustotal_flag": vt_result,
        "verdict": verdict
    }
    
    # Add debug fields when available
    if vt_status is not None:
        response["vt_status"] = vt_status
    if vt_stats is not None:
        response["vt_stats"] = vt_stats
        
    return response
