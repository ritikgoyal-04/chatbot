from flask import Flask, render_template, request, jsonify
import requests

# Together API details
API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = "tgp_v1_gMtRgWbjvUri1pF7a1YFhjGI5OQ_0aRf8vNwHiePNzw"

app = Flask(__name__)


def chat_with_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()

    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        return "Error: Could not generate a response."


@app.route("/")
def index():
    return render_template('chat.html')  # your HTML file


@app.route("/get", methods=["POST"])
def get_response():
    msg = request.get_json().get("message")  # reading from JSON body
    reply = chat_with_gpt(msg)
    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(port=5001)
