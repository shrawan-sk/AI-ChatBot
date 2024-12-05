from flask import Flask, render_template, request, jsonify, session
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app with a secret key for session management
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    """Render the chatbot interface."""
    # Initialize chat history in session if not already present
    if "chat_history" not in session:
        session["chat_history"] = [{"role": "system", "content": "You are a helpful assistant."}]
    return render_template("index.html")

@app.route("/get-response", methods=["POST"])
def get_response():
    """Fetch AI response from OpenAI API."""
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message received"}), 400

    try:
        # Add the user's message to the chat history
        session["chat_history"].append({"role": "user", "content": user_message})

        # Use OpenAI ChatCompletion with extended max_tokens for longer responses
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 Turbo
            messages=session["chat_history"],
            max_tokens=1000,  # Increased token limit for longer responses
            temperature=0.7
        )

        # Get the AI's response
        ai_message = response['choices'][0]['message']['content']

        # Add the AI's response to the chat history
        session["chat_history"].append({"role": "assistant", "content": ai_message})

        return jsonify({"message": ai_message})
    except openai.error.RateLimitError as e:
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    except openai.error.AuthenticationError as e:
        return jsonify({"error": "Invalid API key. Please check your key."}), 401
    except openai.error.OpenAIError as e:
        return jsonify({"error": "API error. Please try again later."}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": "Unexpected server error occurred."}), 500

@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear the chat history."""
    session.pop("chat_history", None)
    session["chat_history"] = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify({"message": "Chat history cleared!"})

if __name__ == "__main__":
    app.run(debug=True)
