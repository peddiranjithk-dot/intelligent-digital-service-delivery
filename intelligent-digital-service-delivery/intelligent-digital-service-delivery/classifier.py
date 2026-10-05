"""Simple rule-based 'intelligence' layer: routes a request to a department
and assigns a priority. Replace with an ML/LLM model later."""

CATEGORIES = {
    "Water Supply":   ["water", "pipe", "leak", "tap", "drain", "sewage"],
    "Electricity":    ["power", "electric", "outage", "transformer", "voltage", "meter"],
    "Roads":          ["road", "pothole", "streetlight", "traffic", "footpath"],
    "Sanitation":     ["garbage", "waste", "trash", "cleaning", "dustbin"],
    "Healthcare":     ["hospital", "clinic", "doctor", "ambulance", "medicine"],
    "Certificates":   ["certificate", "license", "id card", "birth", "income", "caste"],
}
URGENT = ["urgent", "emergency", "danger", "accident", "fire", "no water", "sparking", "injured"]


def classify(text: str):
    t = text.lower()
    scores = {c: sum(k in t for k in kws) for c, kws in CATEGORIES.items()}
    category, hits = max(scores.items(), key=lambda x: x[1])
    if hits == 0:
        category = "General"
    urgent_hits = sum(k in t for k in URGENT)
    priority = "High" if urgent_hits >= 1 else ("Medium" if hits >= 2 else "Low")
    return category, priority
