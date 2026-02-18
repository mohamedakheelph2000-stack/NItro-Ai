// Nitro AI - Enhanced Frontend with Multilingual & Video Support
// ================================================================

// API Configuration - now loaded from config.js
// const API_BASE_URL is set in config.js

// State Management
const state = {
    currentSessionId: null,
    currentUserId: 'user_' + Math.random().toString(36).substr(2, 9),
    currentTab: 'chat',
    selectedLanguage: 'auto',
    detectedLanguage: 'en',
    messages: [],
    sessions: [],
    videos: []
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    console.log('🚀 Nitro AI initializing...');
    
    // Load user preferences
    loadUserPreferences();
    
    // Setup input listeners
    setupInputListeners();
    
    // Load initial data
    await Promise.all([
        loadRecentSessions(),
        loadStatistics(),
        checkConnection()
    ]);
    
    console.log('✅ Nitro AI ready!');
}

// ============================================================================
// LANGUAGE DETECTION & MANAGEMENT
// ============================================================================

async function detectLanguage(text) {
    try {
        const response = await fetch(`${API_BASE_URL}/language/detect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) throw new Error('Language detection failed');
        
        const data = await response.json();
        state.detectedLanguage = data.detected_language;
        
        // Update UI
        updateLanguageIndicator(data.language_name, data.confidence);
        
        return data;
    } catch (error) {
        console.error('Language detection error:', error);
        return { detected_language: 'en', language_name: 'English', confidence: 0.5 };
    }
}

function updateLanguageIndicator(languageName, confidence) {
    const indicator = document.getElementById('detectedLanguage');
    if (indicator) {
        indicator.textContent = languageName;
        indicator.title = `Confidence: ${(confidence * 100).toFixed(0)}%`;
    }
}

async function changeLanguage() {
    const select = document.getElementById('languageSelect');
    state.selectedLanguage = select.value;
    
    // Save preference
    localStorage.setItem('preferredLanguage', state.selectedLanguage);
    
    // If not auto-detect, update indicator
    if (state.selectedLanguage !== 'auto') {
        const option = select.options[select.selectedIndex];
        const langName = option.text.split(' ')[1]; // Get name after emoji
        updateLanguageIndicator(langName || 'English', 1.0);
    }
    
    showToast(`Language preference: ${select.options[select.selectedIndex].text}`, 'success');
}

// ============================================================================
// TAB MANAGEMENT
// ============================================================================

function switchTab(tabName) {
    state.currentTab = tabName;
    
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}Tab`);
    });
}

// ============================================================================
// CHAT FUNCTIONALITY
// ============================================================================

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Disable send button
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    
    // Add user message to UI
    addMessage(message, 'user');
    
    // Clear input
    input.value = '';
    updateCharCounter();
    
    // Auto-detect language if enabled
    if (state.selectedLanguage === 'auto') {
        await detectLanguage(message);
    }
    
    // Show loading
    showLoading();
    
    try {
        // Prepare request data
        const requestData = {
            message: message,
            user_id: state.currentUserId,
            session_id: state.currentSessionId
        };
        
        // Log API call
        CONFIG.logApiCall('/chat', 'POST', requestData);
        
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            CONFIG.logApiError('/chat', `HTTP ${response.status}: ${response.statusText}`);
            throw new Error('Failed to send message');
        }
        
        const data = await response.json();
        
        // Log successful response
        CONFIG.logApiResponse('/chat', response, data);
        
        // Update session if new
        if (!state.currentSessionId && data.session_id) {
            state.currentSessionId = data.session_id;
            updateSessionInfo();
        }
        
        // Add AI response
        addMessage(data.response, 'assistant');
        
        // Reload sessions to show updated conversation
        setTimeout(() => loadRecentSessions(), 500);
        
    } catch (error) {
        console.error('Send message error:', error);
        CONFIG.logApiError('/chat', error);
        showToast('Failed to send message. Please try again.', 'error');
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    } finally {
        hideLoading();
        sendBtn.disabled = false;
        input.focus();
    }
}

function addMessage(text, sender) {
    const container = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    container.appendChild(messageDiv);
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
    
    // Store in state
    state.messages.push({ text, sender, timestamp: new Date().toISOString() });
}

function startNewChat() {
    state.currentSessionId = null;
    state.messages = [];
    
    // Clear chat container except welcome message
    const container = document.getElementById('chatContainer');
    const welcomeMessage = container.querySelector('.message.assistant-message');
    container.innerHTML = '';
    if (welcomeMessage) {
        container.appendChild(welcomeMessage.cloneNode(true));
    }
    
    updateSessionInfo();
    showToast('New chat started', 'success');
    
    // Focus input
    document.getElementById('messageInput').focus();
}

function updateSessionInfo() {
    const sessionText = document.getElementById('currentSessionText');
    if (sessionText) {
        sessionText.textContent = state.currentSessionId ? 
            `Session: ${state.currentSessionId.slice(0, 8)}...` : 
            'New Session';
    }
}

// ============================================================================
// VIDEO GENERATION - NEW
// ============================================================================

async function generateVideo() {
    const prompt = document.getElementById('videoPrompt').value.trim();
    
    if (!prompt) {
        showToast('Please enter a video description', 'error');
        return;
    }
    
    const duration = parseInt(document.getElementById('videoDuration').value);
    const style = document.getElementById('videoStyle').value;
    const resolution = document.getElementById('videoResolution').value;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/video/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                duration,
                style,
                resolution,
                fps: 24
            })
        });
        
        if (!response.ok) throw new Error('Video generation failed');
        
        const data = await response.json();
        
        // Show result
        showToast(`Video queued! ID: ${data.video_id}`, 'success');
        
        // Add to gallery
        addVideoToGallery(data);
        
        // Clear input
        document.getElementById('videoPrompt').value = '';
        
    } catch (error) {
        console.error('Video generation error:', error);
        showToast('Video generation failed. This is a placeholder feature.', 'error');
    } finally {
        hideLoading();
    }
}

function addVideoToGallery(videoData) {
    const gallery = document.getElementById('videoGallery');
    
    // Remove empty state
    const emptyState = gallery.querySelector('.empty-state');
    if (emptyState) emptyState.remove();
    
    // Create video card
    const card = document.createElement('div');
    card.className = 'video-card';
    card.innerHTML = `
        <div class="video-thumbnail">
            <i class="fas fa-film"></i>
            <div class="video-overlay">${videoData.status}</div>
        </div>
        <div class="video-info">
            <p class="video-prompt">${videoData.prompt.slice(0, 50)}...</p>
            <div class="video-meta">
                <span><i class="fas fa-clock"></i> ${videoData.duration}s</span>
                <span><i class="fas fa-expand"></i> ${videoData.resolution}</span>
            </div>
            <p class="video-message">${videoData.message}</p>
        </div>
    `;
    
    gallery.insertBefore(card, gallery.firstChild);
    state.videos.push(videoData);
}

// ============================================================================
// SESSION MANAGEMENT
// ============================================================================

async function loadRecentSessions() {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/recent`);
        if (!response.ok) throw new Error('Failed to load sessions');
        
        const data = await response.json();
        state.sessions = data.sessions || [];
        
        renderSessions();
    } catch (error) {
        console.error('Load sessions error:', error);
    }
}

function renderSessions() {
    const list = document.getElementById('sessionsList');
    
    if (state.sessions.length === 0) {
        list.innerHTML = `
            <div class="session-item-placeholder">
                <p>No conversations yet</p>
                <p class="small-text">Start chatting to see your history</p>
            </div>
        `;
        return;
    }
    
    list.innerHTML = state.sessions.map(session => `
        <div class="session-item ${session.session_id === state.currentSessionId ? 'active' : ''}" 
             onclick="loadSession('${session.session_id}')">
            <div class="session-title">${session.title || 'Untitled'}</div>
            <div class="session-meta">
                <span><i class="fas fa-message"></i> ${session.message_count}</span>
                <span class="small-text">${formatTimeAgo(session.last_updated)}</span>
            </div>
        </div>
    `).join('');
}

async function loadSession(sessionId) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/history/${sessionId}`);
        if (!response.ok) throw new Error('Failed to load session');
        
        const data = await response.json();
        
        // Clear current chat
        state.currentSessionId = sessionId;
        state.messages = [];
        
        const container = document.getElementById('chatContainer');
        container.innerHTML = '';
        
        // Render messages
        data.messages.forEach(msg => {
            if (msg.sender) {
                addMessage(msg.message, msg.sender);
            }
            if (msg.response) {
                addMessage(msg.response, 'assistant');
            }
        });
        
        updateSessionInfo();
        renderSessions(); // Update active state
        
        showToast('Session loaded', 'success');
        
    } catch (error) {
        console.error('Load session error:', error);
        showToast('Failed to load session', 'error');
    } finally {
        hideLoading();
    }
}

// ============================================================================
// STATISTICS
// ============================================================================

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (!response.ok) throw new Error('Failed to load stats');
        
        const data = await response.json();
        const stats = data.statistics;
        
        document.getElementById('totalSessions').textContent = 
            `${stats.total_sessions || 0} sessions`;
        document.getElementById('totalMessages').textContent = 
            `${stats.total_messages || 0} messages`;
            
    } catch (error) {
        console.error('Load stats error:', error);
    }
}

// ============================================================================
// UI HELPERS
// ============================================================================

function setupInputListeners() {
    const input = document.getElementById('messageInput');
    
    // Character counter
    input.addEventListener('input', updateCharCounter);
    
    // Enter to send (Shift+Enter for new line)
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

function updateCharCounter() {
    const input = document.getElementById('messageInput');
    const counter = document.getElementById('charCounter');
    const length = input.value.length;
    counter.textContent = `${length}/1000`;
    
    if (length > 900) {
        counter.style.color = 'var(--warning-color)';
    } else {
        counter.style.color = 'var(--text-secondary)';
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const messageSpan = document.getElementById('toastMessage');
    const icon = toast.querySelector('i');
    
    messageSpan.textContent = message;
    toast.className = `toast ${type} active`;
    
    // Update icon
    if (type === 'success') {
        icon.className = 'fas fa-check-circle';
    } else if (type === 'error') {
        icon.className = 'fas fa-exclamation-circle';
    }
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

async function checkConnection() {
    try {
        CONFIG.logApiCall('/health', 'GET');
        
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        CONFIG.logApiResponse('/health', response, data);
        
        const statusEl = document.getElementById('connectionStatus');
        if (data.status === 'healthy') {
            statusEl.querySelector('.status-text').textContent = 'Connected';
            statusEl.querySelector('.status-dot').style.background = 'var(--success-color)';
            console.log('%c✅ Backend Connection: SUCCESS', 'color: #00ff88; font-weight: bold');
        }
    } catch (error) {
        const statusEl = document.getElementById('connectionStatus');
        statusEl.querySelector('.status-text').textContent = 'Disconnected';
        statusEl.querySelector('.status-dot').style.background = 'var(--error-color)';
        CONFIG.logApiError('/health', error);
        console.error('%c❌ Backend Connection: FAILED', 'color: #ff0066; font-weight: bold');
        console.error('Make sure backend is running at:', API_BASE_URL);
    }
}

// ============================================================================
// UTILITIES
// ============================================================================

function formatTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diff = Math.floor((now - time) / 1000); // seconds
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
    return time.toLocaleDateString();
}

function loadUserPreferences() {
    // Load saved language preference
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang) {
        state.selectedLanguage = savedLang;
        const select = document.getElementById('languageSelect');
        if (select) select.value = savedLang;
    }
}

// ============================================================================
// IMAGE GENERATION FEATURES
// ============================================================================

async function generateImage() {
    const prompt = document.getElementById('imagePrompt')?.value.trim();
    const negativePrompt = document.getElementById('imageNegativePrompt')?.value.trim();
    const size = document.getElementById('imageSize')?.value || '512x512';
    const quality = document.getElementById('imageQuality')?.value || 'standard';
    
    if (!prompt) {
        showToast('Please enter an image description', 'error');
        return;
    }
    
    const btn = document.getElementById('generateImageBtn');
    const originalText = btn.innerHTML;
    
    try {
        // Show loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        showLoading('Generating your image...');
        
        const response = await fetch(`${API_BASE_URL}/image/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                negative_prompt: negativePrompt || undefined,
                size,
                quality
            })
        });
        
        if (!response.ok) throw new Error('Image generation failed');
        
        const data = await response.json();
        
        // Display the generated image
        displayGeneratedImage(data);
        showToast('Image generated successfully!', 'success');
        
        // Refresh gallery
        await loadImageGallery();
        
    } catch (error) {
        console.error('Image generation error:', error);
        showToast(error.message || 'Failed to generate image', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
        hideLoading();
    }
}

function displayGeneratedImage(data) {
    const gallery = document.getElementById('imageGallery');
    if (!gallery) return;
    
    // Remove empty state
    const emptyState = gallery.querySelector('.empty-state');
    if (emptyState) emptyState.remove();
    
    // Create image card
    const imageCard = document.createElement('div');
    imageCard.className = 'image-card';
    imageCard.innerHTML = `
        <img src="data:image/png;base64,${data.image_base64}" alt="Generated image">
        <div class="image-info">
            <p class="image-prompt">${data.prompt.substring(0, 100)}...</p>
            <div class="image-actions">
                <button onclick="downloadImage('${data.file_path}')" title="Download">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        </div>
    `;
    
    gallery.insertBefore(imageCard, gallery.firstChild);
}

async function loadImageGallery() {
    try {
        const response = await fetch(`${API_BASE_URL}/image/gallery?limit=20`);
        if (!response.ok) return;
        
        const data = await response.json();
        const gallery = document.getElementById('imageGallery');
        
        if (data.images && data.images.length > 0) {
            // Clear gallery
            gallery.innerHTML = '';
            
            // Add images
            data.images.forEach(img => {
                const imageCard = document.createElement('div');
                imageCard.className = 'image-card';
                imageCard.innerHTML = `
                    <img src="${img.thumbnail || img.file_path}" alt="Generated image">
                    <div class="image-info">
                        <p class="image-prompt">${img.prompt?.substring(0, 100) || 'No description'}...</p>
                        <p class="image-date">${new Date(img.created_at).toLocaleDateString()}</p>
                    </div>
                `;
                gallery.appendChild(imageCard);
            });
        }
    } catch (error) {
        console.error('Failed to load image gallery:', error);
    }
}

function downloadImage(filePath) {
    window.open(`${API_BASE_URL}/image/download?path=${encodeURIComponent(filePath)}`, '_blank');
}

// ============================================================================
// VOICE ASSISTANT FEATURES
// ============================================================================

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

async function startVoiceRecording() {
    const btn = document.getElementById('voiceBtn');
    const icon = document.getElementById('voiceIcon');
    const text = document.getElementById('voiceText');
    const status = document.getElementById('voiceStatusText');
    
    if (!isRecording) {
        try {
            // Request microphone permission
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await processVoiceInput(audioBlob);
            };
            
            mediaRecorder.start();
            isRecording = true;
            
            // Update UI
            btn.classList.add('recording');
            icon.className = 'fas fa-stop';
            text.textContent = 'Stop Recording';
            status.textContent = 'Recording...';
            
        } catch (error) {
            console.error('Microphone error:', error);
            showToast('Could not access microphone', 'error');
        }
    } else {
        // Stop recording
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        isRecording = false;
        
        // Update UI
        btn.classList.remove('recording');
        icon.className = 'fas fa-microphone';
        text.textContent = 'Start Recording';
        status.textContent = 'Processing...';
    }
}

async function processVoiceInput(audioBlob) {
    const status = document.getElementById('voiceStatusText');
    const transcriptBox = document.getElementById('transcriptBox');
    const responseBox = document.getElementById('voiceResponseBox');
    
    try {
        status.textContent = 'Transcribing...';
        
        // Convert audio to base64
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        
        reader.onloadend = async () => {
            const base64Audio = reader.result.split(',')[1];
            const language = document.getElementById('voiceLanguage')?.value || 'en';
            
            // Send to speech-to-text endpoint
            const response = await fetch(`${API_BASE_URL}/voice/speech-to-text`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    audio_base64: base64Audio,
                    language
                })
            });
            
            if (!response.ok) throw new Error('Speech recognition failed');
            
            const data = await response.json();
            
            // Display transcript
            transcriptBox.innerHTML = `<p>${data.text}</p>`;
            
            // Get AI response
            status.textContent = 'Getting AI response...';
            
            const chatResponse = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: data.text,
                    user_id: state.currentUserId
                })
            });
            
            if (!chatResponse.ok) throw new Error('AI response failed');
            
            const chatData = await chatResponse.json();
            
            // Display AI response
            responseBox.innerHTML = `<p>${chatData.response}</p>`;
            
            // Convert response to speech
            await convertToSpeech(chatData.response, language);
            
            status.textContent = 'Ready';
            showToast('Voice interaction complete!', 'success');
        };
        
    } catch (error) {
        console.error('Voice processing error:', error);
        status.textContent = 'Error';
        showToast(error.message || 'Voice processing failed', 'error');
    }
}

async function convertToSpeech(text, language) {
    try {
        const response = await fetch(`${API_BASE_URL}/voice/text-to-speech`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, language })
        });
        
        if (!response.ok) throw new Error('Text-to-speech failed');
        
        const data = await response.json();
        
        // Show play button
        const playBtn = document.getElementById('playAudioBtn');
        if (playBtn) {
            playBtn.style.display = 'block';
            playBtn.dataset.audioPath = data.file_path;
        }
        
    } catch (error) {
        console.error('Text-to-speech error:', error);
    }
}

function playAudioResponse() {
    const playBtn = document.getElementById('playAudioBtn');
    const audioPath = playBtn?.dataset.audioPath;
    
    if (audioPath) {
        const audio = new Audio(`${API_BASE_URL}/voice/play?path=${encodeURIComponent(audioPath)}`);
        audio.play().catch(error => {
            console.error('Audio playback error:', error);
            showToast('Could not play audio', 'error');
        });
    }
}

// ============================================================================
// WEB SEARCH FEATURES
// ============================================================================

async function performWebSearch() {
    const query = document.getElementById('searchInput')?.value.trim();
    const summarize = document.getElementById('summarizeResults')?.checked ?? true;
    
    if (!query) {
        showToast('Please enter a search query', 'error');
        return;
    }
    
    const btn = document.getElementById('searchBtn');
    const resultsDiv = document.getElementById('searchResults');
    const originalBtnContent = btn.innerHTML;
    
    try {
        // Show loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        showLoading('Searching the web...');
        
        resultsDiv.innerHTML = '<div class="loading-state"><i class="fas fa-spinner fa-spin"></i> Searching and analyzing results...</div>';
        
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query,
                summarize
            })
        });
        
        if (!response.ok) throw new Error('Search failed');
        
        const data = await response.json();
        
        // Display results
        displaySearchResults(data);
        showToast('Search complete!', 'success');
        
    } catch (error) {
        console.error('Search error:', error);
        resultsDiv.innerHTML = `<div class="error-state"><i class="fas fa-exclamation-circle"></i> ${error.message}</div>`;
        showToast(error.message || 'Search failed', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnContent;
        hideLoading();
    }
}

function displaySearchResults(data) {
    const resultsDiv = document.getElementById('searchResults');
    if (!resultsDiv) return;
    
    let html = '';
    
    // Add AI summary if available
    if (data.summary) {
        html += `
            <div class="search-summary">
                <h3><i class="fas fa-robot"></i> AI Summary</h3>
                <div class="summary-content">${formatTextWithCitations(data.summary)}</div>
            </div>
        `;
    }
    
    // Add sources
    if (data.sources && data.sources.length > 0) {
        html += '<div class="search-sources"><h3><i class="fas fa-link"></i> Sources</h3><div class="sources-list">';
        
        data.sources.forEach((source, index) => {
            html += `
                <div class="source-card">
                    <div class="source-number">[${index + 1}]</div>
                    <div class="source-content">
                        <h4><a href="${source.url}" target="_blank">${source.title || 'Untitled'}</a></h4>
                        <p class="source-snippet">${source.snippet || ''}</p>
                        <p class="source-url">${source.url}</p>
                    </div>
                </div>
            `;
        });
        
        html += '</div></div>';
    }
    
    resultsDiv.innerHTML = html;
}

function formatTextWithCitations(text) {
    // Convert citation markers [1], [2], etc. to clickable links
    return text.replace(/\[(\d+)\]/g, '<sup class="citation">[$1]</sup>');
}

// ============================================================================
// PERIODIC UPDATES
// ============================================================================

// Refresh data every 30 seconds
setInterval(() => {
    if (state.currentTab === 'chat') {
        loadStatistics();
    } else if (state.currentTab === 'image') {
        loadImageGallery();
    }
}, 30000);

// Check connection every 10 seconds
setInterval(checkConnection, 10000);

// Load gallery when switching to image tab
const originalSwitchTab = switchTab;
switchTab = function(tabName) {
    originalSwitchTab(tabName);
    if (tabName === 'image') {
        loadImageGallery();
    }
};

console.log('🌐 Nitro AI - Full-Featured AI Assistant Platform Ready!');
console.log('✅ Features: Chat, Images, Voice, Search, Video, Memory, Multi-language');

