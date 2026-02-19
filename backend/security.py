"""
security.py - Security middleware for Nitro AI Backend
Handles API key validation, rate limiting, and security headers
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import time
from typing import Dict, Tuple

try:
    from .config import settings
except ImportError:
    from config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses.
    Protects against common web vulnerabilities.
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Only add HSTS in production with HTTPS
        if not settings.DEBUG_MODE and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:;"
        )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent abuse.
    Tracks requests per IP address.
    """
    def __init__(self, app, requests_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_times: Dict[str, list] = defaultdict(list)
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request, accounting for proxies."""
        # Check Cloudflare headers first
        forwarded_for = request.headers.get("CF-Connecting-IP")
        if forwarded_for:
            return forwarded_for
        
        # Check standard X-Forwarded-For header
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
    
    def _is_rate_limited(self, client_ip: str) -> Tuple[bool, int]:
        """
        Check if client has exceeded rate limit.
        Returns (is_limited, requests_remaining)
        """
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old requests
        self.request_times[client_ip] = [
            req_time for req_time in self.request_times[client_ip]
            if req_time > minute_ago
        ]
        
        # Check limit
        current_requests = len(self.request_times[client_ip])
        if current_requests >= self.requests_per_minute:
            return True, 0
        
        # Add current request
        self.request_times[client_ip].append(now)
        
        return False, self.requests_per_minute - current_requests - 1
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        client_ip = self._get_client_ip(request)
        is_limited, remaining = self._is_rate_limited(client_ip)
        
        if is_limited:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.",
                    "retry_after": 60
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": "60"
                }
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response


async def verify_api_key(request: Request):
    """
    Verify API key from request headers.
    Use this as a dependency for protected routes.
    """
    if not settings.ENABLE_API_KEY:
        # API key not required
        return True
    
    # Skip API key for health check
    if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
        return True
    
    # Get API key from header
    api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization")
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Add 'X-API-Key' header with your API key."
        )
    
    # Remove "Bearer " prefix if present
    if api_key.startswith("Bearer "):
        api_key = api_key[7:]
    
    # Verify API key
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return True


def validate_origin(origin: str) -> bool:
    """
    Validate if origin is allowed.
    Used for additional CORS validation.
    """
    if not origin:
        return False
    
    allowed_origins = settings._build_origins()
    
    # Check exact match
    if origin in allowed_origins:
        return True
    
    # Check wildcard patterns (if configured)
    for allowed in allowed_origins:
        if allowed.endswith("/*") and origin.startswith(allowed[:-2]):
            return True
    
    return False
