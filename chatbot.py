from fastapi import FastAPI
from pydantic import BaseModel
import yaml
import os
import re

# Load rules from rules.yaml with robust path handling
def load_rules():
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rules_path = os.path.join(script_dir, "rules.yaml")
        
        with open(rules_path, "r", encoding="utf8") as f:
            data = yaml.safe_load(f)
            return data.get("rules", []) if data else []
    except (FileNotFoundError, yaml.YAMLError, KeyError):
        # Return empty rules if file is missing or malformed
        return []

rules = load_rules()

app = FastAPI(title="Legal Q&A Chatbot",
              description="Rule-based chatbot for legal questions",
              version="1.0")

# Request body model
class Question(BaseModel):
    question: str

def tokenize_text(text):
    """Tokenize text into words, removing punctuation and converting to lowercase"""
    # Convert to lowercase and extract words (letters and numbers)
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

def calculate_keyword_match_score(question_words, rule_keywords):
    """Calculate match score based on whole-word keyword matching"""
    matches = 0
    for keyword in rule_keywords:
        # Convert keyword to lowercase for case-insensitive matching
        keyword_words = set(re.findall(r'\b\w+\b', keyword.lower()))
        # Check if all words in the keyword phrase are present in the question
        if keyword_words.issubset(question_words):
            matches += 1
    return matches

@app.post("/ask")
def ask(q: Question):
    if not rules:
        # No rules loaded, return fallback response
        return {
            "question": q.question,
            "answer": "Sorry, I could not find a matching law. Please consult a lawyer.",
            "law_reference": None
        }
    
    question_words = tokenize_text(q.question)
    best_rule = None
    best_match_count = 0

    # Find the rule with the highest keyword match score
    for rule in rules:
        match_count = calculate_keyword_match_score(question_words, rule.get("keywords", []))
        if match_count > best_match_count:
            best_match_count = match_count
            best_rule = rule

    if best_rule and best_match_count > 0:
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

