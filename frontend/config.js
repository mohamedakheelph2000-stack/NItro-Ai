// ============================================================================
// NITRO AI - PRODUCTION API CONFIGURATION
// ============================================================================
// This file configures the backend API endpoint based on environment

const CONFIG = {
    // Local Backend API URL (runs on your laptop)
    API_BASE_URL: 'http://localhost:8000',
    
    // Network-accessible URL (for mobile/tablet access)
    // Change this to your laptop's IP if using Cloudflare tunnel
    NETWORK_API_URL: 'http://localhost:8000',
    
    // Auto-detect environment and return appropriate API URL
    getApiUrl: function() {
        // Always use local backend for laptop server mode
        const apiUrl = this.API_BASE_URL;
        
        console.log(`%c🌐 Environment: LOCAL LAPTOP SERVER`, 'color: #00d4ff; font-weight: bold');
        console.log(`%c🔗 API URL: ${apiUrl}`, 'color: #00ff88; font-weight: bold');
        console.log(`%c📍 Frontend: ${window.location.origin}`, 'color: #ffaa00; font-weight: bold');
        console.log(`%c💻 Backend: Ollama on your laptop`, 'color: #9d4edd; font-weight: bold');
        
        return apiUrl;
    },
    
    // Log API calls for debugging
    logApiCall: function(endpoint, method = 'GET', data = null) {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`%c[${timestamp}] API ${method}`, 'color: #00aaff; font-weight: bold', endpoint);
        if (data) {
            console.log('%c📤 Request:', 'color: #ffaa00', data);
        }
    },
    
    // Log API response
    logApiResponse: function(endpoint, response, data = null) {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`%c[${timestamp}] API Response`, 'color: #00ff88; font-weight: bold', endpoint);
        console.log('%c📥 Status:', 'color: #00ff88', response.status, response.statusText);
        if (data) {
            console.log('%c📦 Data:', 'color: #00ff88', data);
        }
    },
    
    // Log API error
    logApiError: function(endpoint, error) {
        const timestamp = new Date().toLocaleTimeString();
        console.error(`%c[${timestamp}] API Error`, 'color: #ff0066; font-weight: bold', endpoint);
        console.error('%c❌ Error:', 'color: #ff0066', error);
    }
};

// Export configuration
const API_BASE_URL = CONFIG.getApiUrl();
