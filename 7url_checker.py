from fastapi import FastAPI
from pydantic import BaseModel
import requests
import ssl
import socket
import os
import base64
import time
from urllib.parse import urlparse

app = FastAPI(title="Payment URL Safety Checker")

# Get VirusTotal API key from environment variable
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
class URLRequest(BaseModel):
    url: str

def normalize_url(url):
    """Normalize URL by adding https:// if no scheme is provided"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def simple_domain_check(url):
    result = {"https": False, "suspicious_domain": False}
    normalized_url = normalize_url(url)
    parsed = urlparse(normalized_url)
    if parsed.scheme.startswith("https"):
        result["https"] = True
    if "-" in parsed.netloc or len(parsed.netloc.split(".")) > 3:
        result["suspicious_domain"] = True
    return result
def check_ssl(url):
    """Check SSL certificate validity, only for https URLs"""
    normalized_url = normalize_url(url)
    parsed = urlparse(normalized_url)
    
    # Only check SSL for https URLs
    if not parsed.scheme.startswith("https"):
        return None  # Not applicable for non-https URLs
    
    hostname = parsed.hostname
    if not hostname:
        return False  # Invalid hostname
    
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
        return True
    except Exception:
        return False
def virustotal_check(url):
    """Check URL with VirusTotal API using proper workflow"""
    if not VIRUSTOTAL_API_KEY:
        return None  # No API key available
    
    normalized_url = normalize_url(url)
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    
    try:
        # Create base64-url-safe encoded URL ID without padding
        url_id = base64.urlsafe_b64encode(normalized_url.encode()).decode().rstrip('=')
        
        # First, try to get existing analysis
        get_resp = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers,
            timeout=10
        )
        
        if get_resp.status_code == 200:
            # Analysis exists, check results
            data = get_resp.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            return malicious > 0 or suspicious > 0
        
        elif get_resp.status_code == 404:
            # No cached analysis, submit URL for analysis
            post_resp = requests.post(
                "https://www.virustotal.com/api/v3/urls",
                headers=headers,
                data={"url": normalized_url},
                timeout=10
            )
            
            if post_resp.status_code != 200:
                return None
            
            analysis_id = post_resp.json()["data"]["id"]
            
            # Poll analysis until completed or timeout
            timeout_time = time.time() + 15  # 15 second timeout
            while time.time() < timeout_time:
                analysis_resp = requests.get(
                    f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                    headers=headers,
                    timeout=10
                )
                
                if analysis_resp.status_code == 200:
                    analysis_data = analysis_resp.json()
                    status = analysis_data.get("data", {}).get("attributes", {}).get("status")
                    
                    if status == "completed":
                        # Analysis complete, get results
                        get_resp = requests.get(
                            f"https://www.virustotal.com/api/v3/urls/{url_id}",
                            headers=headers,
                            timeout=10
                        )
                        
                        if get_resp.status_code == 200:
                            data = get_resp.json()
                            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                            malicious = stats.get("malicious", 0)
                            suspicious = stats.get("suspicious", 0)
                            return malicious > 0 or suspicious > 0
                        break
                
                time.sleep(1)  # Wait 1 second before next poll
            
            # Timeout or error during polling
            return None
        
        else:
            # Other error
            return None
            
    except Exception:
        return None
@app.post("/check-url")
def check_url(request: URLRequest):
    url = request.url
    normalized_url = normalize_url(url)
    
    domain_result = simple_domain_check(url)
    ssl_result = check_ssl(url)
    vt_result = virustotal_check(url)
    
    # Determine verdict based on combined signals
    if vt_result is True or domain_result["suspicious_domain"] or ssl_result is False:
        verdict = "⚠️ Unsafe / Suspicious"
    elif vt_result is None and (not domain_result["https"] or ssl_result is None):
        verdict = "❔ Unknown (VirusTotal check unavailable)"
    elif vt_result is None:
        # VirusTotal unavailable but other checks passed
        verdict = "❔ Unknown (VirusTotal check unavailable)"
    else:
        verdict = "✅ Safe"
    
    return {
        "url": normalized_url,
        "https": domain_result["https"],
        "suspicious_domain": domain_result["suspicious_domain"],
        "ssl_valid": ssl_result,
        "virustotal_flag": vt_result,
        "verdict": verdict
    }
