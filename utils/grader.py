import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def process_resume(path):
    text = extract_text_from_pdf(path)
    doc = nlp(text)

    score = 0
    feedback = []

    # Keywords
    keywords = ["Python", "Machine Learning", "Data", "Project", "API", "Leadership"]
    matched_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    score += len(matched_keywords) * 5
    if len(matched_keywords) < 4:
        feedback.append("Add more role-specific keywords like Python, API, etc.")

    # Contact Info
    if any(token.like_email for token in doc):
        score += 10
    else:
        feedback.append("Add a professional email address.")

    # Experience Section
    if "experience" in text.lower():
        score += 15
    else:
        feedback.append("Include a dedicated 'Experience' section.")

    # Education Section
    if "education" in text.lower():
        score += 15
    else:
        feedback.append("Include a dedicated 'Education' section.")

    # Skills Section
    if "skills" in text.lower():
        score += 10
    else:
        feedback.append("Include a 'Skills' section with your tech stack.")

    # Final Cap
    score = min(score, 100)
    return score, feedback
