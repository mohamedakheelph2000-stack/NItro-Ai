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
        // Call API with timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
        
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: CONFIG.getFetchHeaders(),
            body: JSON.stringify({ message: message }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        const aiResponse = data.response || 'Sorry, I could not generate a response.';
        
        // Update model badge (including error state)
        if (data.ai_model) {
            state.model = data.ai_model;
            const badge = document.getElementById('modelBadge');
            badge.textContent = data.ai_model;
            // Visual indicator for error state
            if (data.ai_source === 'error') {
                badge.style.backgroundColor = '#ff4444';
                badge.title = 'Ollama connection error';
            } else {
                badge.style.backgroundColor = '';
                badge.title = '';
            }
        }
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant message
        appendMessage('assistant', aiResponse);
        
        // Save chat (only if not an error response)
        if (data.ai_source !== 'error') {
            saveChat(message, aiResponse);
        }
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        
        // Provide specific error messages
        let errorMsg;
        if (error.name === 'AbortError') {
            errorMsg = '⏱️ **Request Timeout**\n\nThe request took too long. The AI model might be loading or your system is busy.\n\nPlease try again in a moment.';
        } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMsg = '🚨 **Backend Not Connected**\n\nCannot reach the backend server at ' + API_BASE_URL + '\n\n**Quick Fix:**\n1. Make sure the backend is running\n2. Check if Ollama is started: `ollama serve`\n3. Refresh the page and try again';
        } else if (error.message.includes('Message cannot be empty')) {
            errorMsg = '⚠️ Please enter a message before sending.';
        } else {
            errorMsg = '❌ **Error**\n\n' + error.message + '\n\nPlease try again or check the console for details.';
        }
        
        appendMessage('assistant', errorMsg);
        showToast('Message failed to send', 'error');
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
    
    // Show install button
    const installBtn = document.getElementById('installBtn');
    if (installBtn) {
        installBtn.style.display = 'flex';
        console.log('💡 PWA install prompt available');
    }
});

window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully');
    deferredPrompt = null;
    
    // Hide install button
    const installBtn = document.getElementById('installBtn');
    if (installBtn) {
        installBtn.style.display = 'none';
    }
    
    showToast('Nitro AI installed successfully! 🎉', 'success');
});

async function installPWA() {
    if (!deferredPrompt) {
        console.log('⚠️ Install prompt not available');
        showToast('App already installed or not available for installation', 'info');
        return;
    }
    
    // Show the install prompt
    deferredPrompt.prompt();
    
    // Wait for the user's response
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
        console.log('✅ User accepted install');
    } else {
        console.log('❌ User declined install');
    }
    
    // Clear the deferred prompt
    deferredPrompt = null;
    
    // Hide install button
    const installBtn = document.getElementById('installBtn');
    if (installBtn) {
        installBtn.style.display = 'none';
    }
}

// Check if already running as PWA
if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    console.log('✅ Running as installed PWA');
    // Hide install button if running as PWA
    window.addEventListener('DOMContentLoaded', () => {
        const installBtn = document.getElementById('installBtn');
        if (installBtn) {
            installBtn.style.display = 'none';
        }
    });
}
