const chatBox = document.getElementById('chat-box');
const typingIndicator = document.getElementById('typing-indicator');

function appendMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('User', message);
    userInput.value = '';

    // Show typing indicator
    typingIndicator.style.display = 'block';

    try {
        const response = await fetch('/get-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();

        // Hide typing indicator
        typingIndicator.style.display = 'none';

        if (data.message) {
            appendMessage('AI', data.message);
        } else {
            appendMessage('AI', 'Error: Unable to get a response.');
        }
    } catch (error) {
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        appendMessage('AI', 'Error: Unable to connect to the server.');
    }
}
