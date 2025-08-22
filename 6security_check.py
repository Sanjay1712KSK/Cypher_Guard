from fastapi import FastAPI
import subprocess
import platform
import re

app = FastAPI()

# 🔒 Check Firewall Status (Mac)
def check_firewall():
    if platform.system() == "Darwin":  # Darwin = macOS
        try:
            output = subprocess.check_output(
                ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"],
                text=True
            )
            if "enabled" in output.lower():
                return "Enabled"
            else:
                return "Disabled"
        except:
            return "Unknown"
    else:
        return "Not supported"

# 🛡️ Check Antivirus (very basic, looks for popular AV processes)
def check_antivirus():
    if platform.system() == "Darwin":
        try:
            output = subprocess.check_output(["ps", "aux"], text=True)
            if any(av in output for av in ["Norton", "Avast", "McAfee", "Sophos", "Malwarebytes"]):
                return "Running"
            else:
                return "Not Detected"
        except:
            return "Unknown"
    else:
        return "Not supported"

# 🔑 Password Strength Check
def check_password_strength(password: str):
    if len(password) < 8:
        return "Weak"
    if not re.search(r"[A-Z]", password):
        return "Weak"
    if not re.search(r"[0-9]", password):
        return "Weak"
    if not re.search(r"[@$!%*?&#]", password):
        return "Weak"
    return "Strong"

# 🔄 macOS Update Check
def check_updates():
    if platform.system() == "Darwin":
        try:
            output = subprocess.check_output(["softwareupdate", "-l"], text=True)
            if "No new software available" in output:
                return "Up to Date"
            else:
                return "Updates Available"
        except:
            return "Unknown"
    else:
        return "Not supported"

# 🚀 FastAPI Endpoint
@app.get("/security_health")
def security_health(password: str = "Test@1234"):
    return {
        "firewall": check_firewall(),
        "antivirus": check_antivirus(),
        "password_strength": check_password_strength(password),
        "system_updates": check_updates()
    }

