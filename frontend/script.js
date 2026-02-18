/* ============================================================================
   NITRO AI - ChatGPT-Style Frontend Logic
   100% Free Local AI Assistant
   ============================================================================ */

// State Management
const state = {
    currentChatId: null,
    chats: [],
    theme: localStorage.getItem('theme') || 'light',
    model: 'llama3.2:1b',
    isLoading: false
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    loadChatHistory();
    checkOllamaStatus();
});

/* ============================================================================
   THEME MANAGEMENT
   ============================================================================ */

function initializeTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    updateThemeIcon();
}

function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', state.theme);
    document.documentElement.setAttribute('data-theme', state.theme);
    updateThemeIcon();
}

function updateThemeIcon() {
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');
    if (state.theme === 'dark') {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
    } else {
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
    }
}

/* ============================================================================
   SIDEBAR MANAGEMENT
   ============================================================================ */

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

function newChat() {
    state.currentChatId = null;
    document.getElementById('messages').innerHTML = '';
    document.getElementById('welcomeScreen').style.display = 'flex';
    document.getElementById('messageInput').focus();
    
    // Clear selection in history
    document.querySelectorAll('.chat-history-item').forEach(item => {
        item.classList.remove('active');
    });
}

function loadChatHistory() {
    const historyContainer = document.getElementById('chatHistory');
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    
    if (chats.length === 0) {
        historyContainer.innerHTML = '<p style="padding: 16px; text-align: center; color: var(--text-secondary); font-size: 14px;">No chats yet</p>';
        return;
    }
    
    historyContainer.innerHTML = chats.map((chat, index) => `
        <div class="chat-history-item ${index === 0 ? 'active' : ''}" onclick="loadChat('${chat.id}')">
            ${chat.title || 'New conversation'}
        </div>
    `).join('');
    
    state.chats = chats;
}

function loadChat(chatId) {
    const chat = state.chats.find(c => c.id === chatId);
    if (!chat) return;
    
    state.currentChatId = chatId;
    
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';
    document.getElementById('welcomeScreen').style.display = 'none';
    
    chat.messages.forEach(msg => {
        appendMessage(msg.role, msg.content, false);
    });
    
    // Update active state
    document.querySelectorAll('.chat-history-item').forEach((item, index) => {
        item.classList.toggle('active', state.chats[index].id === chatId);
    });
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function saveChat(userMessage, assistantMessage) {
    if (!state.currentChatId) {
        // New chat
        state.currentChatId = Date.now().toString();
        const title = userMessage.substring(0, 50);
        state.chats.unshift({
            id: state.currentChatId,
            title: title,
            messages: [
                { role: 'user', content: userMessage },
                { role: 'assistant', content: assistantMessage }
            ]
        });
    } else {
        // Existing chat
        const chat = state.chats.find(c => c.id === state.currentChatId);
        if (chat) {
            chat.messages.push(
                { role: 'user', content: userMessage },
                { role: 'assistant', content: assistantMessage }
            );
        }
    }
    
    // Keep only last 50 chats
    state.chats = state.chats.slice(0, 50);
    localStorage.setItem('chats', JSON.stringify(state.chats));
    loadChatHistory();
}

/* ============================================================================
   MESSAGE HANDLING
   ============================================================================ */

function sendSuggestion(text) {
    document.getElementById('messageInput').value = text;
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || state.isLoading) return;
    
    // Hide welcome screen
    document.getElementById('welcomeScreen').style.display = 'none';
    
    // Add user message
    appendMessage('user', message);
    
    // Clear input
    input.value = '';
    autoResize(input);
    
    // Disable input
    state.isLoading = true;
    document.getElementById('sendBtn').disabled = true;
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        const aiResponse = data.response || 'Sorry, I could not generate a response.';
        
        // Update model badge
        if (data.model) {
            state.model = data.model;
            document.getElementById('modelBadge').textContent = data.model;
        }
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant message
        appendMessage('assistant', aiResponse);
        
        // Save chat
        saveChat(message, aiResponse);
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        
        const errorMsg = error.message.includes('Failed to fetch')
            ? '❌ Cannot connect to backend. Make sure the server is running at ' + API_BASE_URL
            : '❌ Error: ' + error.message;
        
        appendMessage('assistant', errorMsg);
        showToast('Failed to send message. Check console for details.', 'error');
    } finally {
        state.isLoading = false;
        document.getElementById('sendBtn').disabled = false;
        input.focus();
    }
}

function appendMessage(role, content, shouldScroll = true) {
    const messagesContainer = document.getElementById('messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? 'You' : 'AI';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    
    // Simple markdown rendering
    let formattedContent = content
        .replace(/```(\w+)?\n([\s\S]*?)```/g, (_, lang, code) => {
            return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
        })
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    textDiv.innerHTML = formattedContent;
    
    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    if (shouldScroll) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant-message';
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    
    typingDiv.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return id;
}

function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

/* ============================================================================
   INPUT HANDLING
   ============================================================================ */

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

/* ============================================================================
   UTILITIES
   ============================================================================ */

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function checkOllamaStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET'
        });
        
        if (response.ok) {
            console.log('✅ Backend connected');
        }
    } catch (error) {
        console.warn('⚠️ Backend not reachable:', error.message);
        showToast('Backend not connected. Start the server to use AI features.', 'error');
    }
}

/* ============================================================================
   PWA INSTALL PROMPT
   ============================================================================ */

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    // Could show a custom install button here
});

window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed');
    deferredPrompt = null;
});
