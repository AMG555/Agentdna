"""Simple in-memory rate limiter for API protection."""
import time
import logging
from collections import defaultdict, deque
from typing import Dict, Deque, Tuple

logger = logging.getLogger(__name__)

class RateLimiter:
    """Token bucket rate limiter with per-endpoint limits."""
    
    def __init__(self):
        # endpoint -> (requests_per_minute, requests_per_hour)
        self.limits: Dict[str, Tuple[int, int]] = {
            '/api/privacy/allow': (10, 100),
            '/api/privacy/data': (5, 20),
            '/api/agents/feedback': (30, 300),
            '/api/automations': (20, 200),
            '/api/ai/suggestion': (10, 100),
            '/api/reasoning/plan': (10, 100),
            '/api/automation/execute': (5, 50),
        }
        # client_id -> endpoint -> deque of timestamps
        self.requests: Dict[str, Dict[str, Deque[float]]] = defaultdict(lambda: defaultdict(deque))
    
    def check_limit(self, client_id: str, endpoint: str) -> Tuple[bool, str]:
        """Check if request is within rate limits.
        
        Args:
            client_id: Client identifier (IP or user ID)
            endpoint: API endpoint path
            
        Returns:
            Tuple of (allowed, reason)
        """
        if endpoint not in self.limits:
            return True, 'ok'
        
        per_minute, per_hour = self.limits[endpoint]
        now = time.time()
        
        # Clean old requests
        client_requests = self.requests[client_id][endpoint]
        while client_requests and client_requests[0] < now - 3600:
            client_requests.popleft()
        
        # Count recent requests
        minute_ago = now - 60
        hour_ago = now - 3600
        
        minute_count = sum(1 for ts in client_requests if ts > minute_ago)
        hour_count = len(client_requests)
        
        if minute_count >= per_minute:
            logger.warning(f'Rate limit exceeded: {client_id} hit {endpoint} {minute_count}/min (limit {per_minute})')
            return False, f'rate_limit_minute_{per_minute}'
        
        if hour_count >= per_hour:
            logger.warning(f'Rate limit exceeded: {client_id} hit {endpoint} {hour_count}/hour (limit {per_hour})')
            return False, f'rate_limit_hour_{per_hour}'
        
        # Allow request and record it
        client_requests.append(now)
        return True, 'ok'
    
    def reset(self, client_id: str | None = None):
        """Reset rate limits for client or all clients."""
        if client_id:
            if client_id in self.requests:
                del self.requests[client_id]
                logger.info(f'Reset rate limits for {client_id}')
        else:
            self.requests.clear()
            logger.info('Reset all rate limits')
    
    def get_stats(self, client_id: str) -> Dict[str, Dict[str, int]]:
        """Get current rate limit stats for a client."""
        stats = {}
        now = time.time()
        minute_ago = now - 60
        hour_ago = now - 3600
        
        for endpoint, timestamps in self.requests[client_id].items():
            minute_count = sum(1 for ts in timestamps if ts > minute_ago)
            hour_count = sum(1 for ts in timestamps if ts > hour_ago)
            per_minute, per_hour = self.limits.get(endpoint, (999, 9999))
            
            stats[endpoint] = {
                'minute_count': minute_count,
                'minute_limit': per_minute,
                'hour_count': hour_count,
                'hour_limit': per_hour,
                'minute_remaining': per_minute - minute_count,
                'hour_remaining': per_hour - hour_count
            }
        
        return stats

rate_limiter = RateLimiter()
