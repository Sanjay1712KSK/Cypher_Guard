from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import socket
import requests

app = FastAPI()

def get_ip(domain: str):
    return socket.gethostbyname(domain)

def get_country(ip: str):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        return data.get("country_name", "Unknown")
    except:
        return "Unknown"

@app.post("/check_ip")
async def check_ip(url: str = Form(...)):
    try:
        # Get domain from URL (remove https:// or http://)
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]

        ip = get_ip(domain)
        country = get_country(ip)

        is_india = (country == "India")

        return JSONResponse({
            "url": url,
            "domain": domain,
            "ip": ip,
            "country": country,
            "is_india": is_india
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

