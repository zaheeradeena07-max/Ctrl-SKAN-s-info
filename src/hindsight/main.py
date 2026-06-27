from flask import Flask, request, jsonify
from difflib import SequenceMatcher
import json, os

app = Flask(__name__)

# Load persisted notes from hindsight_store.json
store_path = os.path.join(os.path.dirname(__file__), "hindsight_store.json")
if os.path.exists(store_path):
    with open(store_path) as f:
        hindsight_store = json.load(f)
else:
    hindsight_store = []

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("query", "").lower()

    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    # Define keyword groups for fallback
    keyword_map = {
        "billing": ["billing", "invoice", "payment", "charges"],
        "login": ["login", "auth", "password", "credentials"],
        "outage": ["outage", "downtime", "system crash", "server issue"]
    }

    matches = []
    for entry in hindsight_store:
        note_text = entry["note"].lower()

        # Fuzzy similarity
        if similarity(question, note_text) > 0.3:
            matches.append(entry)
            continue

        # Keyword fallback
        for group, keywords in keyword_map.items():
            if any(word in question for word in keywords) and group in note_text:
                matches.append(entry)
                break

    # Format results into clean strings
    formatted = []
    for m in matches:
        formatted.append(f"Note: {m['note']}\nTime: {m['time']}")

    return jsonify({"matches": formatted})

@app.route("/remember", methods=["POST"])
def remember():
    data = request.get_json()
    note = data.get("note")

    if not note:
        return jsonify({"error": "No note provided"}), 400

    entry = {
        "note": note,
        "time": __import__("datetime").datetime.now().isoformat()
    }
    hindsight_store.append(entry)

    # Persist to hindsight_store.json
    with open(store_path, "w") as f:
        json.dump(hindsight_store, f, indent=2)

    return jsonify({"status": "saved", "note": note})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6000)

