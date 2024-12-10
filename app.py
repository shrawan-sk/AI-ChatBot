'''
Program Name: AI ChatBot Application
Author: Shrawan Khanal, Abhishekh, Jordan, Arafat
Last Modified By: Shrawan Khanal
Date Last Modified: 2024-12-09
Program Description:
    This is a Flask-based chatbot application that uses the OpenAI API to provide AI responses.
    Users can interact with the bot through a simple web interface.

Revision History:
    v1.0 - Initial implementation of Flask app (2024-12-02).
    v1.1 - Added session-based chat history and error handling (2024-12-07).
    v1.2 - Added inline comments and headers for functions (2024-12-09).
'''

from flask import Flask, render_template, request, jsonify, session
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = "supersecretkey"  # Replace with a secure key in production

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def render_home_page():
    """
    Function: render_home_page
    Description: Displays the chatbot interface.
                 Initializes chat history in the session if not already present.
    Returns: Rendered HTML template for the chatbot UI.
    """
    # Initialize chat history with a default system message if not present
    if "chat_history" not in session:
        session["chat_history"] = [{"role": "system", "content": "You are a helpful assistant."}]
    return render_template("index.html")

@app.route("/get-response", methods=["POST"])
def fetch_ai_response():
    """
    Function: fetch_ai_response
    Description: Handles user input, communicates with the OpenAI API to generate a response,
                 and maintains session-based chat history.
    Returns: JSON response containing the AI's message or an error message.
    """
    # Retrieve the user's message from the POST request
    user_message = request.json.get("message", "")

    # If no message is received, return an error response
    if not user_message:
        return jsonify({"error": "No message received"}), 400

    try:
        # Add the user's message to the session chat history
        session["chat_history"].append({"role": "user", "content": user_message})

        # Call OpenAI API to generate a response based on the chat history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the model
            messages=session["chat_history"],  # Pass chat history to the API
            max_tokens=1000,  # Set token limit for longer responses
            temperature=0.7  # Adjust response creativity
        )

        # Extract the AI's response message
        ai_message = response['choices'][0]['message']['content']

        # Add the AI's response to the session chat history
        session["chat_history"].append({"role": "assistant", "content": ai_message})

        # Return the AI's message as a JSON response
        return jsonify({"message": ai_message})
    except openai.error.RateLimitError:
        # Handle rate limit error from OpenAI
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    except openai.error.AuthenticationError:
        # Handle authentication error (invalid API key)
        return jsonify({"error": "Invalid API key. Please check your key."}), 401
    except openai.error.OpenAIError:
        # Handle other OpenAI API errors
        return jsonify({"error": "API error. Please try again later."}), 500
    except Exception as error:
        # Handle any unexpected errors
        print(f"Unexpected Error: {error}")
        return jsonify({"error": "Unexpected server error occurred."}), 500

@app.route("/clear-history", methods=["POST"])
def clear_chat_history():
    """
    Function: clear_chat_history
    Description: Clears the chat history in the session and resets it to the default state.
    Returns: JSON response confirming that the chat history has been cleared.
    """
    # Remove existing chat history from the session
    session.pop("chat_history", None)
    # Reset chat history to a default system message
    session["chat_history"] = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify({"message": "Chat history cleared!"})

if __name__ == "__main__":
    # Run the Flask application in debug mode for development
    app.run(debug=True)
