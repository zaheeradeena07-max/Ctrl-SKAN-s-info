from fastapi import FastAPI, Request, Header, HTTPException
import os, yaml, datetime

# Create FastAPI app
app = FastAPI()

# Load routing.yaml safely
file_path = os.path.join(os.path.dirname(__file__), "routing.yaml")
with open(file_path, "r") as f:
    routing = yaml.safe_load(f)

def route_query(query: str):
    query_lower = query.lower()
    for rule in routing["rules"]:
        if rule.get("match") and rule["match"].lower() in query_lower:
            return rule["model"]
    return routing["rules"][-1]["default"]

def log_query(query, model):
    # If file doesn't exist, create it with headers
    if not os.path.exists("cascadeflow_log.md"):
        with open("cascadeflow_log.md", "w", encoding="utf-8") as f:
            f.write("| Timestamp | Query | Model |\n")
            f.write("|-----------|-------|-------|\n")

    # Append new row
    with open("cascadeflow_log.md", "a", encoding="utf-8") as f:
        f.write(f"| {datetime.datetime.now()} | {query} | {model} |\n")

# Add a session divider when the server starts
with open("cascadeflow_log.md", "a", encoding="utf-8") as f:
    f.write("\n## --- New Session Started at "
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n\n")

@app.post("/query")
async def handle_query(request: Request, authorization: str = Header(None)):
    if authorization != "Bearer cascadeflow_key_123":
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    query = data.get("query", "")
    model = route_query(query)
    log_query(query, model)
    return {
        "answer": f"(Simulated) handled by {model}",
        "model_used": model
    }

# Optional test block if you run with python main.py
if __name__ == "__main__":
    test_queries = [
        "Has this customer reported similar issues before?",
        "Billing error in my invoice",
        "Login password not working",
        "System outage yesterday",
        "Random general question"
    ]
    for q in test_queries:
        model = route_query(q)
        print(f"Query: {q} -> {model}")
        log_query(q, model)






