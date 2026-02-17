// Production API Configuration
// Update this after deploying frontend to match your deployment URL

const CONFIG = {
    // Backend API URL - deployed on Render
    API_BASE_URL: 'https://nitro-ai-pk9l.onrender.com',
    
    // Fallback to localhost for development
    DEV_API_URL: 'http://localhost:8000',
    
    // Auto-detect environment
    getApiUrl: function() {
        // If running on localhost, use dev URL
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.DEV_API_URL;
        }
        // Otherwise use production URL
        return this.API_BASE_URL;
    }
};

// Export configuration
const API_BASE_URL = CONFIG.getApiUrl();

console.log('🌐 API URL:', API_BASE_URL);
