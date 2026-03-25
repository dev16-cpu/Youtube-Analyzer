def detect_genre(text):
    text = text.lower()

    if any(word in text for word in ["python", "coding", "programming", "developer"]):
        return "Tech"

    elif any(word in text for word in ["math", "mathematics", "education", "learn", "tutorial"]):
        return "Education"

    elif any(word in text for word in ["vlog", "travel", "daily", "life"]):
        return "Lifestyle"

    elif any(word in text for word in ["game", "gaming", "pubg", "minecraft"]):
        return "Gaming"

    else:
        return "Other"
 
def extract_keywords(text):
    text = text.lower().replace("https", "")
    words = text.split()

    stopwords = ["the", "is", "in", "and", "to", "of", "a", "this"]

    keywords = [
        word for word in words 
        if word not in stopwords and len(word) > 3
    ]

    return list(set(keywords))[:5]  

import re

def format_duration(duration):
    # Example: PT1H2M15S
    hours = minutes = seconds = 0

    h = re.search(r'(\d+)H', duration)
    m = re.search(r'(\d+)M', duration)
    s = re.search(r'(\d+)S', duration)

    if h:
        hours = int(h.group(1))
    if m:
        minutes = int(m.group(1))
    if s:
        seconds = int(s.group(1))

    return f"{hours}h {minutes}m {seconds}s"