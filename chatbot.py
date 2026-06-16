from fastapi import FastAPI
from pydantic import BaseModel
import yaml
import os
import re

def load_rules():
    """Load rules from rules.yaml with fallback mechanism"""
    rules = []
    
    # Try loading from script directory first
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(script_dir, "rules.yaml")
    
    # Fallback to current working directory
    if not os.path.exists(rules_path):
        rules_path = "rules.yaml"
    
    try:
        with open(rules_path, "r", encoding="utf8") as f:
            data = yaml.safe_load(f)
            rules = data.get("rules", [])
        print(f"Successfully loaded {len(rules)} rules from {rules_path}")
    except FileNotFoundError:
        print(f"Warning: rules.yaml not found in {script_dir} or current directory")
    except Exception as e:
        print(f"Error loading rules: {e}")
    
    return rules

# Load rules from rules.yaml
rules = load_rules()

app = FastAPI(title="Legal Q&A Chatbot",
              description="Rule-based chatbot for legal questions",
              version="1.0")

# Request body model
class Question(BaseModel):
    question: str

def tokenize_and_match(text, keywords):
    """Improved keyword matching with tokenization and case-insensitive matching"""
    # Simple tokenization: split on whitespace and punctuation
    text_tokens = re.findall(r'\b\w+\b', text.lower())
    
    match_count = 0
    exact_matches = 0
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_tokens = re.findall(r'\b\w+\b', keyword_lower)
        
        # Check for substring match (original behavior)
        if keyword_lower in text.lower():
            match_count += 1
            
            # Bonus for exact token matches
            if any(token in text_tokens for token in keyword_tokens):
                exact_matches += 1
    
    # Give slight weight boost to exact token matches
    return match_count + (exact_matches * 0.1)

@app.post("/ask")
def ask(q: Question):
    text = q.question
    best_rule = None
    best_match_score = 0

    # Improved keyword matching
    for rule in rules:
        match_score = tokenize_and_match(text, rule["keywords"])
        if match_score > best_match_score:
            best_match_score = match_score
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

@app.get("/rules")
def get_rules():
    """Return sanitized list of loaded rules for debugging"""
    return {
        "total_rules": len(rules),
        "rules": [
            {
                "id": rule.get("id", "unknown"),
                "question": rule.get("question", "")
            }
            for rule in rules
        ]
    }

