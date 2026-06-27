import requests

def route_query(question: str):
    if "billing" in question.lower():
        try:
            response = requests.post(
                "http://127.0.0.1:6000/query",
                json={"query": question}
            )
            response.raise_for_status()
            data = response.json()

            # Format matches into clean strings
            formatted = []
            for match in data.get("matches", []):
                note = match.get("note", "")
                time = match.get("time", "")
                formatted.append(f"Note: {note}\nTime: {time}")

            return {"matches": formatted}

        except Exception as e:
            return {"error": str(e)}

    elif "auth" in question.lower() or "login" in question.lower():
        return {"answer": "Auth module would handle this"}
    else:
        return {"answer": "Support module would handle this"}
