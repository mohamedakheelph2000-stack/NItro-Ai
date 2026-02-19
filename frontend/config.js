// ============================================================================
// NITRO AI - PRODUCTION API CONFIGURATION
// ============================================================================
// This file configures the backend API endpoint based on environment

const CONFIG = {
    // ===== CONFIGURATION VARIABLES =====
    // Edit these for your deployment
    
    // Local Backend API URL (for development)
    LOCAL_API_URL: 'http://localhost:8000',
    
    // Cloudflare Tunnel URL (for public access)
    // Set this to your Cloudflare Tunnel domain (e.g., https://nitro-ai.yourdomain.com)
    // Leave empty to disable public access
    CLOUDFLARE_TUNNEL_URL: '',
    
    // API Key (optional, for secured public access)
    // If backend has ENABLE_API_KEY=True, set your API key here
    // SECURITY: In production, move this to a secure config or user login
    API_KEY: '',
    
    // Auto-detect environment and return appropriate API URL
    getApiUrl: function() {
        // Check if we're accessing from Cloudflare Tunnel domain
        const currentHost = window.location.hostname;
        
        // If Cloudflare Tunnel is configured and we're not on localhost
        if (this.CLOUDFLARE_TUNNEL_URL && !currentHost.includes('localhost') && !currentHost.includes('127.0.0.1')) {
            console.log(`%c🌐 Environment: CLOUDFLARE TUNNEL (Public)`, 'color: #00d4ff; font-weight: bold');
            console.log(`%c🔗 API URL: ${this.CLOUDFLARE_TUNNEL_URL}`, 'color: #00ff88; font-weight: bold');
            console.log(`%c📍 Frontend: ${window.location.origin}`, 'color: #ffaa00; font-weight: bold');
            console.log(`%c🔒 API Key: ${this.API_KEY ? '✓ Set' : '✗ Not Set'}`, 'color: #9d4edd; font-weight: bold');
            return this.CLOUDFLARE_TUNNEL_URL;
        }
        
        // Default to local API
        console.log(`%c🌐 Environment: LOCAL LAPTOP SERVER`, 'color: #00d4ff; font-weight: bold');
        console.log(`%c🔗 API URL: ${this.LOCAL_API_URL}`, 'color: #00ff88; font-weight: bold');
        console.log(`%c📍 Frontend: ${window.location.origin}`, 'color: #ffaa00; font-weight: bold');
        console.log(`%c💻 Backend: Ollama on your laptop`, 'color: #9d4edd; font-weight: bold');
        
        return this.LOCAL_API_URL;
    },
    
    // Get fetch headers (includes API key if configured)
    getFetchHeaders: function(additionalHeaders = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...additionalHeaders
        };
        
        // Add API key if configured
        if (this.API_KEY) {
            headers['X-API-Key'] = this.API_KEY;
        }
        
        return headers;
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
