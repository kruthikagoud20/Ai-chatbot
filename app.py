from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# OpenRouter API Key
OPENROUTER_API_KEY = "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"


# OR directly:
# OPENROUTER_API_KEY = "your_openrouter_api_key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:
        # Get user message from frontend
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({
                "error": "Message is required"
            }), 400

        # Send request to OpenRouter
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",

                # Optional but recommended
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Flask AI Chatbot"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        # Convert API response to JSON
        result = response.json()

        # Debugging (optional)
        print(result)

        # Extract AI message
        ai_response = result["choices"][0]["message"]["content"]

        # Return response to frontend
        return jsonify({
            "response": ai_response
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)