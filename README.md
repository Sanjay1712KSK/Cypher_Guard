# 🔐 Cypher Guard - For NLH X AI Legal Hackathon

Cypher Guard is a Python-based backend security toolkit built with FastAPI. It provides multiple security-related services such as file encryption, URL safety checks, IP lookup, system security health checks, privacy policy generation, and a rule-based legal chatbot.

> This project is an educational/experimental backend API collection for learning backend security tooling and FastAPI.

---

## Table of contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Running the Services](#running-the-services)
- [Testing the APIs](#testing-the-apis)
- [Important Notes & Security](#important-notes--security)
- [Future Improvements](#future-improvements)
- [Project Status](#project-status)
- [License](#license)

---

## Project Overview
Cypher Guard is a backend-only API project where each module exposes REST endpoints via FastAPI. Each module demonstrates a different security-related utility and can be launched as a separate FastAPI service for testing via Swagger UI.

---

## Features

- 🔐 File Encryption & Decryption
  - Password-based file encryption
  - AES-GCM (authenticated encryption)
  - Secure key derivation using Scrypt
  - Upload/download encrypted and decrypted files via API

- 🌍 IP & Domain Lookup
  - Extract domain from URL
  - Resolve IP address
  - Fetch country information using a public IP API

- 🛡️ System Security Health Check
  - Firewall status check (macOS)
  - Basic antivirus detection
  - Password strength validation
  - System update status (platform-dependent)

- 🔗 URL Safety Checker
  - HTTPS availability check
  - SSL certificate validation
  - Suspicious domain pattern detection
  - VirusTotal API integration (basic threat check)

- 📜 Privacy Policy Generator
  - Generates privacy policy PDF
  - Accepts business and data-handling details
  - Optional user consent logging
  - Stores consent records locally

- ⚖️ Rule-Based Legal Chatbot
  - Simple keyword-based chatbot
  - Answers legal questions using predefined rules
  - Rules configured in `rules.yaml`

---

## Project Structure

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
```

---

## Requirements

- Python 3.8+
- Internet connection (for IP lookup & VirusTotal checks)
- Supported OS: Windows / Linux / macOS  
  (Note: some system checks are platform-specific)

Recommended Python packages (example):
- fastapi
- uvicorn
- cryptography
- requests
- pydantic
- fpdf
- pyyaml

You can create a requirements file like:
```bash
pip install fastapi uvicorn cryptography requests pydantic fpdf pyyaml
```

---

## Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/Sanjay1712KSK/Cypher_Guard.git
cd Cypher_Guard
```

2. Create and activate a virtual environment

Windows (PowerShell / CMD):
```powershell
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install fastapi uvicorn cryptography requests pydantic fpdf pyyaml
```

(Optionally create a `requirements.txt` for easier installs:
```bash
pip freeze > requirements.txt
```)

---

## Running the Services

Each module runs as a separate FastAPI service. Example commands:

- File Encryption API:
```bash
uvicorn main:app --reload
```

- IP Lookup API:
```bash
uvicorn ip_lookup:app --reload
```

- Security Health Check API:
```bash
uvicorn security_check:app --reload
```

- URL Safety Checker API:
```bash
uvicorn url_checker:app --reload
```

- Privacy Policy Generator API:
```bash
uvicorn privacy_policy:app --reload
```

- Legal Chatbot API:
```bash
uvicorn chatbot:app --reload
```

By default, uvicorn serves on http://127.0.0.1:8000. If running multiple services at once, run each on a different port:
```bash
uvicorn main:app --reload --port 8001
uvicorn ip_lookup:app --reload --port 8002
# etc.
```

---

## Testing the APIs (UI)

FastAPI automatically provides an interactive API docs page (Swagger UI) for each running service.

Open in browser (example service):
```
http://127.0.0.1:8000/docs
```

From there you can:
- View all endpoints
- Send requests
- Upload files
- See responses and example schemas

---

## Important Notes & Security

- This is a learning and experimental project — not production-ready.
- VirusTotal API keys (if any) must not be hard-coded for production. Use environment variables and secure secret storage.
- Some system checks are basic demonstrations and platform-dependent (macOS/Windows/Linux differences).
- Handle user data, logs, and keys carefully — avoid storing secrets in plaintext.
- Improve authentication/authorization before exposing any endpoints publicly.

---

## Future Improvements

- Combine modules into a single FastAPI app using routers
- Secure API keys via environment variables (do not hardcode)
- Add authentication & authorization (OAuth2 / JWT)
- Harden system security checks and make cross-platform
- Add a frontend dashboard
- Add tests and CI
- Provide a `requirements.txt` and example Dockerfile
- Deploy using Render / Railway / other platforms

---

## Project Status

- ✅ Completed (educational/experimental)
- 📘 Educational / Learning Project
- 🧪 Experimental

---

## Contributing

Contributions, issues, and feature requests are welcome. This project is primarily for learning — feel free to open issues or fork the repo to experiment.

---

## License

This project is intended for educational purposes only. No warranty is provided. If you want to add a license, consider adding an explicit LICENSE file (e.g., MIT, Apache-2.0) depending on your preference.
