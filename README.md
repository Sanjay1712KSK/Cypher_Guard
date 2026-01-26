# 🔐 Cypher Guard

Cypher Guard is a **Python-based backend security toolkit** built using **FastAPI**.  
It provides multiple **security-related services** such as file encryption, URL safety checks, IP lookup, system security health checks, privacy policy generation, and a rule-based legal chatbot.

This project was developed as a **learning and experimentation project** to explore:
- Backend API development
- Cybersecurity fundamentals
- Encryption concepts
- Modular Python application design

---

## 📌 Project Overview

Cypher Guard is **not a frontend application**.  
It is a **backend-only API project**, where each module exposes REST APIs that can be tested using FastAPI’s built-in Swagger UI.

The project demonstrates how different security-related utilities can be implemented as independent services using FastAPI.

---

## 🚀 Features

### 🔐 File Encryption & Decryption
- Password-based file encryption
- Uses **AES-GCM** (authenticated encryption)
- Secure key derivation using **Scrypt**
- Upload and download encrypted/decrypted files via API

### 🌍 IP & Domain Lookup
- Extracts domain from a given URL
- Resolves IP address
- Fetches country information using a public IP API

### 🛡️ System Security Health Check
- Firewall status check (macOS)
- Basic antivirus detection
- Password strength validation
- System update status (platform-dependent)

### 🔗 URL Safety Checker
- HTTPS availability check
- SSL certificate validation
- Suspicious domain pattern detection
- VirusTotal API integration (basic threat check)

### 📜 Privacy Policy Generator
- Generates a privacy policy PDF
- Accepts business and data-handling details
- Optional user consent logging
- Stores consent records locally

### ⚖️ Rule-Based Legal Chatbot
- Simple keyword-based chatbot
- Answers legal questions using predefined rules
- Rules stored in a YAML configuration file

---

## 🧩 Project Structure

```text
Cypher_Guard/
│
├── main.py                  # File encryption & decryption API
├── ip_lookup.py             # IP address & country lookup service
├── security_check.py        # System security health checks
├── url_checker.py           # URL safety checker
├── privacy_policy.py        # Privacy policy PDF generator
├── chatbot.py               # Rule-based legal chatbot
├── rules.yaml               # Rules for legal chatbot
├── sample_module.py         # Sample placeholder module
├── .gitignore
└── README.md
🛠️ Requirements
Python 3.8 or above

Internet connection (for IP lookup & VirusTotal checks)

Supported OS: Windows / Linux / macOS
(Some system checks are platform-specific)

📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/Sanjay1712KSK/Cypher_Guard.git
cd Cypher_Guard
2️⃣ Create and Activate Virtual Environment
Windows (PowerShell / CMD):

python -m venv venv
venv\Scripts\activate
Linux / macOS:

python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies
pip install fastapi uvicorn cryptography requests pydantic fpdf pyyaml
▶️ Running the Application
Each module runs as a separate FastAPI service.

🔐 File Encryption API
uvicorn main:app --reload
🌍 IP Lookup API
uvicorn ip_lookup:app --reload
🛡️ Security Health Check API
uvicorn security_check:app --reload
🔗 URL Safety Checker API
uvicorn url_checker:app --reload
📜 Privacy Policy Generator API
uvicorn privacy_policy:app --reload
⚖️ Legal Chatbot API
uvicorn chatbot:app --reload
🧪 Testing the APIs (UI)
FastAPI provides an interactive API UI automatically.

After starting any service, open:

http://127.0.0.1:8000/docs
You can:

View all endpoints

Send requests

Upload files

See responses instantly

⚠️ Important Notes
This project is backend-only (no frontend UI)

Some checks are basic demonstrations, not enterprise-grade security

VirusTotal API key is hardcoded (not secure for production)

Not suitable for production use without improvements

🎓 Learning Outcomes
This project helped in understanding:

FastAPI and REST API development

Encryption fundamentals (AES, key derivation)

API-based security tools

Modular backend architecture

Working with external APIs

PDF generation and YAML-based rule systems

🚀 Future Improvements
Combine all modules into a single FastAPI app using routers

Secure API keys using environment variables

Add authentication & authorization

Improve system security checks

Add frontend dashboard

Create requirements.txt for deployment

Deploy using Render or Railway

📌 Project Status
✅ Completed

📘 Educational / Learning Project

🧪 Experimental
