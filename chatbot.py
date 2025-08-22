from fastapi import FastAPI
from pydantic import BaseModel
import yaml

# Load rules from rules.yaml
with open("rules.yaml", "r", encoding="utf8") as f:
    rules = yaml.safe_load(f)["rules"]

app = FastAPI(title="Legal Q&A Chatbot",
              description="Rule-based chatbot for legal questions",
              version="1.0")

# Request body model
class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    text = q.question.lower()
    best_rule = None
    best_match_count = 0

    # simple keyword match
    for rule in rules:
        match_count = sum(1 for kw in rule["keywords"] if kw in text)
        if match_count > best_match_count:
            best_match_count = match_count
            best_rule = rule

    if best_rule:
        return {
            "question": q.question,
            "answer": best_rule["answer"],
            "law_reference": best_rule["law"]
        }
    else:
        return {
            "question": q.question,
            "answer": "Sorry, I could not find a matching law. Please consult a lawyer.",
            "law_reference": None
        }

