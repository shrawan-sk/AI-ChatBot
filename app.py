from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    """Render the chatbot interface."""
    return render_template("index.html")

@app.route("/get-response", methods=["POST"])
def get_response():
    """Fetch AI response from OpenAI API."""
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message received"}), 400

    try:
        # New API interface for OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )
        ai_message = response['choices'][0]['message']['content']
        return jsonify({"message": ai_message})
    except openai.AuthenticationError as e:
        print(f"Authentication Error: {e}")
        return jsonify({"error": "Invalid API key"}), 500
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({"error": "API error, try again later"}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": "Unexpected server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
