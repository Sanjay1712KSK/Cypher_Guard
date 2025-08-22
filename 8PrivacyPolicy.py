from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from fpdf import FPDF
import json
import os

app = FastAPI(title="Privacy Policy & Consent Helper with PDF")

# In-memory consent storage
consent_db = []

class PrivacyPolicyRequest(BaseModel):
    business_name: str
    data_collected: str
    data_usage: str
    data_retention: str
    third_party_sharing: str

class ConsentRequest(BaseModel):
    user_name: str
    user_email: str
    agreed_to_policy: bool

# Generate PDF with optional consent info
@app.post("/generate_policy_pdf")
def generate_policy_pdf(req: PrivacyPolicyRequest, user_name: str = None, user_email: str = None, agreed_to_policy: bool = None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Privacy Policy for {req.business_name}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.multi_cell(0, 8, f"1. Data Collected: {req.data_collected}")
    pdf.multi_cell(0, 8, f"2. How We Use Your Data: {req.data_usage}")
    pdf.multi_cell(0, 8, f"3. Data Retention Period: {req.data_retention}")
    pdf.multi_cell(0, 8, f"4. Third-Party Sharing: {req.third_party_sharing}")
    pdf.ln(10)
    pdf.multi_cell(0, 8, "By using our service, you agree to this privacy policy.")

    # Add user consent section if provided
    if user_name and user_email and agreed_to_policy is not None:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "User Consent", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.ln(5)
        consent_text = f"""
        User Name: {user_name}
        User Email: {user_email}
        Agreed to Policy: {'Yes' if agreed_to_policy else 'No'}
        Timestamp: {datetime.now().isoformat()}
        """
        pdf.multi_cell(0, 8, consent_text.strip())

        # Record consent in memory and JSON file
        if agreed_to_policy:
            consent_record = {
                "user_name": user_name,
                "user_email": user_email,
                "agreed_to_policy": agreed_to_policy,
                "timestamp": datetime.now().isoformat()
            }
            consent_db.append(consent_record)
            with open("consent_records.json", "w") as f:
                json.dump(consent_db, f, indent=4)

    # Save PDF
    filename = f"PrivacyPolicy_{req.business_name}.pdf"
    pdf.output(filename)

    return FileResponse(path=filename, filename=filename, media_type='application/pdf')

