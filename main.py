from flask import Flask, request, jsonify
import routing

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    question = data.get("query", "")
    try:
        model = routing.route_query(question)

        # If routing returns a dict, jsonify it.
        if isinstance(model, dict):
            return jsonify(model)
        # If routing returns a string (like response.text), wrap it in a dict.
        else:
            return jsonify({"answer": model})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)




