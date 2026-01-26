# Cypher Guard 🔐

Cypher Guard is a **Python-based security utility project** built using **FastAPI**.  
It combines multiple small security-related services such as file encryption, URL safety checks, IP lookup, system security checks, and a rule-based legal chatbot.

This project was developed as a **learning and experimentation project** to understand backend APIs, cybersecurity concepts, and modular Python design.

---

## 🚀 Features

- 🔐 **File Encryption & Decryption**
  - Password-based encryption using AES-GCM
- 🌍 **IP & Domain Lookup**
  - Fetch IP address and country information for a given URL
- 🛡️ **System Security Health Check**
  - Firewall status (macOS)
  - Antivirus detection (basic)
  - Password strength checking
- 🔗 **URL Safety Checker**
  - HTTPS & SSL validation
  - Domain structure checks
  - VirusTotal API integration
- 📜 **Privacy Policy Generator**
  - Generate privacy policy PDFs
  - Optional user consent logging
- ⚖️ **Rule-Based Legal Chatbot**
  - Answers legal questions using predefined rules

---

## 🧩 Project Structure

```text
Cypher_Guard/
│
├── 3main.py                # File encryption & decryption API
├── 5ip_lookup.py           # IP address & country lookup
├── 6security_check.py      # System security health checks
├── 7url_checker.py         # URL safety checker
├── 8PrivacyPolicy.py       # Privacy policy PDF generator
├── chatbot.py              # Rule-based legal chatbot
├── rules.yaml              # Legal rules for chatbot
├── sample_module.py        # Sample / placeholder module
├── .gitignore
└── README.md

