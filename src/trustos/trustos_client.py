import requests
import json
import os

# Load config.json for TrustOS endpoint and token
config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path) as f:
    config = json.load(f)

ENDPOINT = config["endpoint"]
AUTH_TOKEN = config["auth_token"]

# Path for persistent query counts
counts_path = os.path.join(os.path.dirname(__file__), "query_counts.json")

# Load existing counts if file exists, otherwise start fresh
if os.path.exists(counts_path):
    with open(counts_path) as f:
        query_counts = json.load(f)
else:
    query_counts = {"billing": 0, "login": 0, "outage": 0, "other": 0}

def query_trustos(user_query):
    try:
        response = requests.post(
            ENDPOINT,
            headers={"Authorization": f"Bearer {AUTH_TOKEN}", "Content-Type": "application/json"},
            json={"query": user_query}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def categorize_query(q):
    q = q.lower()
    if any(word in q for word in ["billing", "invoice", "payment", "charges"]):
        query_counts["billing"] += 1
        return "billing"
    elif any(word in q for word in ["login", "auth", "password", "credentials"]):
        query_counts["login"] += 1
        return "login"
    elif any(word in q for word in ["outage", "downtime", "system crash", "server issue"]):
        query_counts["outage"] += 1
        return "outage"
    else:
        query_counts["other"] += 1
        return "other"

def print_analytics():
    print("\nQuery Analytics:")
    for category, count in query_counts.items():
        print(f"{category.capitalize()} queries: {count}")

if __name__ == "__main__":
    print("TrustOS Client connected. Type your queries below.")
    while True:
        user_input = input("\nEnter your query (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting TrustOS client.")
            break

        # Send query to TrustOS
        result = query_trustos(user_input)

        # Categorize and count
        category = categorize_query(user_input)

        # Display results
        print(f"\nQuery: {user_input}")
        if "matches" in result:
            print("Cascadeflow Echo:")
            for m in result["matches"]:
                print(m)
        else:
            print("Cascadeflow Echo: No matches found.")

        # Simulated structured answer
        if category == "billing":
            print("Simulated Answer: Case Report: Ticket #4321 — Customer reported a billing issue.\nResolution: Applied patch to invoice system and verified fix.")
        elif category == "login":
            print("Simulated Answer: Case Report: Ticket #9876 — Customer unable to log in.\nResolution: Password reset performed and access restored.")
        elif category == "outage":
            print("Simulated Answer: Incident Report: Outage affecting premium customers.\nResolution: Server restarted and services restored.")
        else:
            print("Simulated Answer: No structured case report available for this query.")

        # Show analytics
        print_analytics()
        with open(counts_path, "w") as f:
            json.dump(query_counts, f, indent=2)

