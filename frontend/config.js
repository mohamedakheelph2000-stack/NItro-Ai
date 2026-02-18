// ============================================================================
// NITRO AI - PRODUCTION API CONFIGURATION
// ============================================================================
// This file configures the backend API endpoint based on environment

const CONFIG = {
    // Production Backend API URL (deployed on Render)
    API_BASE_URL: 'https://nitro-ai-pk9l.onrender.com',
    
    // Development Backend API URL (local development)
    DEV_API_URL: 'http://localhost:8000',
    
    // Auto-detect environment and return appropriate API URL
    getApiUrl: function() {
        const hostname = window.location.hostname;
        const isDev = hostname === 'localhost' || hostname === '127.0.0.1';
        
        const apiUrl = isDev ? this.DEV_API_URL : this.API_BASE_URL;
        
        console.log(`%c🌐 Environment: ${isDev ? 'DEVELOPMENT' : 'PRODUCTION'}`, 'color: #00d4ff; font-weight: bold');
        console.log(`%c🔗 API URL: ${apiUrl}`, 'color: #00ff88; font-weight: bold');
        console.log(`%c📍 Frontend: ${window.location.origin}`, 'color: #ffaa00; font-weight: bold');
        
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
