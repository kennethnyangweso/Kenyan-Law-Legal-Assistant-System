// static/js/chat.js
const chatMessages = document.getElementById('chat-messages');
const questionInput = document.getElementById('question-input');
const sendButton = document.getElementById('send-button');

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (isUser) {
        contentDiv.innerHTML = `<strong>👤 You:</strong><p>${escapeHtml(message)}</p>`;
    } else {
        // Convert markdown-style bullet points to HTML
        let formattedMessage = message.replace(/•/g, '<br>•');
        contentDiv.innerHTML = `<strong>⚖️ Legal Assistant:</strong><div>${formattedMessage}</div>`;
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function sendMessage() {
    const question = questionInput.value.trim();
    if (!question) return;
    
    // Add user message to chat
    addMessage(question, true);
    
    // Clear input
    questionInput.value = '';
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = '<div class="message-content"><em>🤔 Thinking...</em></div>';
    typingDiv.id = 'typing-indicator';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        document.getElementById('typing-indicator')?.remove();
        
        if (data.error) {
            addMessage(`Sorry, I encountered an error: ${data.error}`, false);
        } else {
            addMessage(data.answer, false);
        }
    } catch (error) {
        document.getElementById('typing-indicator')?.remove();
        addMessage('Sorry, I could not connect to the server. Please try again.', false);
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});