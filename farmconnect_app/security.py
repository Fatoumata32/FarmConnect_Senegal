"""
Security utilities for FarmConnect

This module provides security-related utilities including:
- Rate limiting decorator for API endpoints
- Input sanitization functions
- Security validation helpers
"""

from django.core.cache import cache
from django.http import JsonResponse
from functools import wraps
import time
import hashlib


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


def rate_limit(requests_per_minute=60, key_prefix='ratelimit'):
    """
    Simple rate limiting decorator.

    Args:
        requests_per_minute: Maximum number of requests allowed per minute
        key_prefix: Cache key prefix for rate limiting

    Usage:
        @rate_limit(requests_per_minute=10)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get client identifier (IP + user ID if authenticated)
            client_ip = get_client_ip(request)
            if request.user.is_authenticated:
                client_id = f"{client_ip}_{request.user.id}"
            else:
                client_id = client_ip

            # Create cache key
            cache_key = f"{key_prefix}_{hashlib.md5(client_id.encode()).hexdigest()}"

            # Get current request count and timestamp
            rate_data = cache.get(cache_key)
            current_time = time.time()

            if rate_data is None:
                # First request
                rate_data = {
                    'count': 1,
                    'window_start': current_time
                }
            else:
                # Check if we're still in the same window (1 minute)
                if current_time - rate_data['window_start'] > 60:
                    # New window
                    rate_data = {
                        'count': 1,
                        'window_start': current_time
                    }
                else:
                    # Same window, increment count
                    rate_data['count'] += 1

            # Check if rate limit exceeded
            if rate_data['count'] > requests_per_minute:
                return JsonResponse({
                    'error': 'Trop de requêtes. Veuillez réessayer plus tard.',
                    'retry_after': int(60 - (current_time - rate_data['window_start']))
                }, status=429)

            # Update cache
            cache.set(cache_key, rate_data, 120)  # 2 minutes TTL

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


def rate_limit_login(requests_per_minute=5):
    """
    Stricter rate limiting for login attempts.

    Uses IP-based tracking to prevent brute force attacks.
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        key_prefix='login_ratelimit'
    )


def rate_limit_api(requests_per_minute=30):
    """
    Rate limiting for API endpoints.
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        key_prefix='api_ratelimit'
    )


def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension to prevent malicious uploads.

    Args:
        filename: Name of the uploaded file
        allowed_extensions: List of allowed extensions (e.g., ['.jpg', '.png'])

    Returns:
        bool: True if valid, False otherwise
    """
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions


def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal attacks.

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    import os
    import re

    # Get basename to prevent directory traversal
    filename = os.path.basename(filename)

    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)

    return filename
