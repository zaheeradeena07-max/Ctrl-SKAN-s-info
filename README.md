# Ctrl-SKAN-info
This repository contains the prototype implementation of TrustOS, an AI-powered organizational memory platform designed to help SKAN preserve knowledge, reduce repetitive work, and improve decision-making.

## 🧠 Hindsight – Memory Layer
- **Purpose:** Hindsight acts as the *long‑term memory engine* for TrustOS.  
- **How it works here:**
  - Every query submitted through the Flask interface can be logged into Hindsight.
  - Hindsight stores not just the query, but the *reasoning and context* behind responses.
  - Later, you can ask: *“Why was this query resolved in a certain way?”* and Hindsight recalls the decision history.
- **Benefit:** Prevents loss of knowledge over time. Even months later, the system remembers why a billing issue was handled a certain way.

---

## ⚡ Cascadeflow – Query Routing Layer
- **Purpose:** Cascadeflow is the *query router* for TrustOS.  
- **How it works here:**
  - When a user submits a query, Cascadeflow decides which AI model or service should handle it.
  - Example:  
    - Billing queries → routed to a financial support model.  
    - Login queries → routed to an authentication support model.  
    - Unknown queries → routed to a fallback or escalation path.
- **Benefit:** Makes the system efficient and scalable by ensuring queries are answered by the right engine.

---

## 🔍 Combined Workflow
1. User submits a query in the Flask interface (`index.html`).  
2. `app.py` processes the query and logs it into **Hindsight** for memory.  
3. **Cascadeflow** routes the query to the correct AI model or service.  
4. The response is displayed back to the user, while Hindsight keeps track of the reasoning for future reference.

---

## 📌 Example
- User types: **“billing issue”**  
- `app.py` sends the query to Cascadeflow.  
- Cascadeflow routes it to the billing support model.  
- The response is logged in Hindsight: *“Resolved on June 27, 2026 – duplicate charges corrected.”*  
- Next time someone asks *“Why was billing issue resolved?”*, Hindsight provides the full context