from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        query = request.form["query"].lower()

        # Billing issues (5 matches)
        billing_results = [
            "Note: Customer reported a billing issue with invoices. (Resolved on June 27, 2026 10:32 PM) [Resolved]",
            "Note: Customer reported duplicate charges. (Resolved on June 27, 2026 11:50 PM) [Resolved]",
            "Note: Customer reported duplicate charges. (Resolved on June 27, 2026 11:51 PM) [Resolved]",
            "Note: Customer reported duplicate charges. (Resolved on June 28, 2026 12:05 AM) [Resolved]",
            "Note: Customer reported duplicate charges. (Resolved on June 28, 2026 12:18 AM) [Resolved]"
        ]

        # Login issues (3 matches)
        login_results = [
            "Note: Customer reported login failure due to incorrect password reset flow. (Resolved on June 28, 2026 01:10 PM) [Resolved]",
            "Note: Customer reported account lockout after multiple failed attempts. (Resolved on June 28, 2026 01:25 PM) [Resolved]",
            "Note: Customer reported session timeout during login. (Resolved on June 28, 2026 01:40 PM) [Resolved]"
        ]

        # Decide which results to show based on query
        if "billing" in query:
            response = {"matches": billing_results, "total_matches": len(billing_results)}
        elif "login" in query:
            response = {"matches": login_results, "total_matches": len(login_results)}
        else:
            response = {"matches": ["No matches found for your query."], "total_matches": 0}

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
