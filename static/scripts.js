/**
 * scripts.js
 * Author: Shrawan Khanal, Abhishekh, Jordan, Arafat
 * Last Modified: 2024-12-09
 * Description: Handles chatbot interactions, including sending user input to the server,
 *              receiving AI responses, and dynamically updating the chat UI.
 * Revision History:
 *     v1.0 - Initial implementation of user input and AI response handling (2024-12-02)
 *     v1.1 - Added typing indicator and error handling (2024-12-08)
 *     v1.2 - Optimized chat scrolling and added comments for clarity (2024-12-09)
 */

// Get references to the chat box and typing indicator elements
const chatBox = document.getElementById('chat-box'); // Chat container for messages
const typingIndicator = document.getElementById('typing-indicator'); // Typing status indicator

/**
 * Function: appendMessage
 * Description: Appends a message to the chat box.
 * Parameters:
 *    sender (string): The sender of the message (e.g., 'User' or 'AI').
 *    message (string): The message text to be displayed.
 * Returns: None
 */
function appendMessage(sender, message) {
    const messageDiv = document.createElement('div'); // Create a new div for the message
    messageDiv.className = `message ${sender}`; // Assign a class based on the sender
    messageDiv.textContent = message; // Set the message text
    chatBox.appendChild(messageDiv); // Add the message to the chat box
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom of the chat box
}

/**
 * Function: sendMessage
 * Description: Handles the process of sending a user's message to the server
 *              and displaying the AI's response in the chat box.
 * Returns: None
 */
async function sendMessage() {
    const userInput = document.getElementById('user-input'); // Input field for user messages
    const message = userInput.value.trim(); // Get the user's input and trim whitespace

    if (!message) return; // Exit if the input is empty

    appendMessage('User', message); // Display the user's message in the chat
    userInput.value = ''; // Clear the input field

    // Show the typing indicator while waiting for a response
    typingIndicator.style.display = 'block';

    try {
        // Send the user's message to the server via a POST request
        const response = await fetch('/get-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }, // Specify JSON content type
            body: JSON.stringify({ message }), // Send the user's message in the request body
        });

        const data = await response.json(); // Parse the server's JSON response

        // Hide the typing indicator once the response is received
        typingIndicator.style.display = 'none';

        if (data.message) {
            // Display the AI's response in the chat
            appendMessage('AI', data.message);
        } else {
            // Display an error message if no response is received
            appendMessage('AI', 'Error: Unable to get a response.');
        }
    } catch (error) {
        // Hide the typing indicator if there's a connection error
        typingIndicator.style.display = 'none';

        // Display an error message in the chat
        appendMessage('AI', 'Error: Unable to connect to the server.');
    }
}
