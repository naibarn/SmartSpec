"""
Rate Limiting Module for SmartSpec Autopilot

Provides comprehensive rate limiting to prevent abuse:
- Token bucket algorithm
- Per-user/IP rate limiting
- Cooldown periods
- Usage tracking
- Multiple rate limit tiers

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import time
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from threading import Lock
from .error_handler import with_error_handling


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    max_requests: int  # Maximum requests allowed
    time_window: int   # Time window in seconds
    cooldown: int = 0  # Cooldown period in seconds after limit exceeded
    
    def __post_init__(self):
        """Validate configuration"""
        if self.max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if self.time_window <= 0:
            raise ValueError("time_window must be positive")
        if self.cooldown < 0:
            raise ValueError("cooldown cannot be negative")


@dataclass
class RateLimitState:
    """State for a single rate limit bucket"""
    tokens: float  # Current number of tokens
    last_update: float  # Last update timestamp
    cooldown_until: float = 0.0  # Cooldown end timestamp
    total_requests: int = 0  # Total requests made
    blocked_requests: int = 0  # Total blocked requests


class TokenBucket:
    """Token bucket rate limiter implementation"""
    
    def __init__(self, config: RateLimitConfig):
        """
        Initialize token bucket.
        
        Args:
            config: Rate limit configuration
        """
        self.config = config
        self.state = RateLimitState(
            tokens=float(config.max_requests),
            last_update=time.time()
        )
        self.lock = Lock()
    
    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.state.last_update
        
        # Calculate refill rate (tokens per second)
        refill_rate = self.config.max_requests / self.config.time_window
        
        # Add tokens based on elapsed time
        new_tokens = elapsed * refill_rate
        self.state.tokens = min(
            self.config.max_requests,
            self.state.tokens + new_tokens
        )
        self.state.last_update = now
    
    def consume(self, tokens: int = 1) -> Tuple[bool, Dict]:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            Tuple of (allowed, info_dict)
        """
        with self.lock:
            now = time.time()
            
            # Check if in cooldown period
            if now < self.state.cooldown_until:
                self.state.blocked_requests += 1
                return False, {
                    "allowed": False,
                    "reason": "cooldown",
                    "cooldown_remaining": self.state.cooldown_until - now,
                    "retry_after": self.state.cooldown_until - now
                }
            
            # Refill tokens
            self._refill_tokens()
            
            # Check if enough tokens
            if self.state.tokens >= tokens:
                self.state.tokens -= tokens
                self.state.total_requests += 1
                
                return True, {
                    "allowed": True,
                    "tokens_remaining": self.state.tokens,
                    "tokens_max": self.config.max_requests,
                    "reset_after": self.config.time_window
                }
            else:
                # Not enough tokens - enter cooldown if configured
                if self.config.cooldown > 0:
                    self.state.cooldown_until = now + self.config.cooldown
                
                self.state.blocked_requests += 1
                
                return False, {
                    "allowed": False,
                    "reason": "rate_limit_exceeded",
                    "tokens_remaining": self.state.tokens,
                    "tokens_required": tokens,
                    "retry_after": self.config.time_window,
                    "cooldown_active": self.config.cooldown > 0
                }
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        with self.lock:
            self._refill_tokens()
            
            return {
                "tokens_remaining": self.state.tokens,
                "tokens_max": self.config.max_requests,
                "total_requests": self.state.total_requests,
                "blocked_requests": self.state.blocked_requests,
                "success_rate": (
                    (self.state.total_requests - self.state.blocked_requests) / 
                    self.state.total_requests * 100
                    if self.state.total_requests > 0 else 100.0
                ),
                "in_cooldown": time.time() < self.state.cooldown_until
            }
    
    def reset(self) -> None:
        """Reset the bucket to initial state"""
        with self.lock:
            self.state = RateLimitState(
                tokens=float(self.config.max_requests),
                last_update=time.time()
            )


class RateLimiter:
    """Multi-tier rate limiter with per-identifier tracking"""
    
    # Predefined rate limit tiers
    TIERS = {
        "strict": RateLimitConfig(max_requests=10, time_window=60, cooldown=60),
        "moderate": RateLimitConfig(max_requests=30, time_window=60, cooldown=30),
        "relaxed": RateLimitConfig(max_requests=100, time_window=60, cooldown=0),
        "unlimited": RateLimitConfig(max_requests=10000, time_window=1, cooldown=0),
    }
    
    def __init__(self, default_tier: str = "moderate"):
        """
        Initialize rate limiter.
        
        Args:
            default_tier: Default tier name
        """
        if default_tier not in self.TIERS:
            raise ValueError(f"Invalid tier: {default_tier}")
        
        self.default_tier = default_tier
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()
    
    def _get_bucket(self, identifier: str, tier: Optional[str] = None) -> TokenBucket:
        """Get or create bucket for identifier"""
        with self.lock:
            if identifier not in self.buckets:
                config = self.TIERS[tier or self.default_tier]
                self.buckets[identifier] = TokenBucket(config)
            return self.buckets[identifier]
    
    @with_error_handling
    def check_rate_limit(
        self,
        identifier: str,
        tokens: int = 1,
        tier: Optional[str] = None
    ) -> Dict:
        """
        Check if request is allowed under rate limit.
        
        Args:
            identifier: Unique identifier (user_id, IP, etc.)
            tokens: Number of tokens to consume
            tier: Optional tier override
            
        Returns:
            Dict with rate limit info
        """
        bucket = self._get_bucket(identifier, tier)
        allowed, info = bucket.consume(tokens)
        
        return {
            "success": True,
            "identifier": identifier,
            **info
        }
    
    @with_error_handling
    def get_stats(self, identifier: str) -> Dict:
        """
        Get statistics for an identifier.
        
        Args:
            identifier: Unique identifier
            
        Returns:
            Dict with statistics
        """
        with self.lock:
            if identifier not in self.buckets:
                return {
                    "success": True,
                    "identifier": identifier,
                    "exists": False
                }
            
            bucket = self.buckets[identifier]
            stats = bucket.get_stats()
            
            return {
                "success": True,
                "identifier": identifier,
                "exists": True,
                **stats
            }
    
    @with_error_handling
    def reset(self, identifier: str) -> Dict:
        """
        Reset rate limit for an identifier.
        
        Args:
            identifier: Unique identifier
            
        Returns:
            Dict with reset status
        """
        with self.lock:
            if identifier in self.buckets:
                self.buckets[identifier].reset()
                return {
                    "success": True,
                    "identifier": identifier,
                    "reset": True
                }
            else:
                return {
                    "success": True,
                    "identifier": identifier,
                    "reset": False,
                    "reason": "identifier_not_found"
                }
    
    @with_error_handling
    def get_all_stats(self) -> Dict:
        """
        Get statistics for all identifiers.
        
        Returns:
            Dict with all statistics
        """
        with self.lock:
            stats = {}
            for identifier, bucket in self.buckets.items():
                stats[identifier] = bucket.get_stats()
            
            return {
                "success": True,
                "total_identifiers": len(self.buckets),
                "stats": stats
            }
    
    def cleanup_inactive(self, inactive_seconds: int = 3600) -> int:
        """
        Remove inactive buckets to save memory.
        
        Args:
            inactive_seconds: Seconds of inactivity before cleanup
            
        Returns:
            Number of buckets removed
        """
        with self.lock:
            now = time.time()
            to_remove = []
            
            for identifier, bucket in self.buckets.items():
                if now - bucket.state.last_update > inactive_seconds:
                    to_remove.append(identifier)
            
            for identifier in to_remove:
                del self.buckets[identifier]
            
            return len(to_remove)


# Decorator for rate limiting
def rate_limit(identifier_key: str = "user_id", tier: str = "moderate"):
    """
    Decorator to apply rate limiting to functions.
    
    Args:
        identifier_key: Key to extract identifier from kwargs
        tier: Rate limit tier to use
        
    Example:
        @rate_limit(identifier_key="user_id", tier="strict")
        def process_request(user_id: str, data: dict):
            # Process request
            pass
    """
    def decorator(func):
        limiter = RateLimiter(default_tier=tier)
        
        def wrapper(*args, **kwargs):
            # Extract identifier
            identifier = kwargs.get(identifier_key, "default")
            
            # Check rate limit
            result = limiter.check_rate_limit(identifier)
            
            if not result.get("allowed", False):
                return {
                    "error": True,
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": "คำขอถูกปฏิเสธเนื่องจากเกินขอบเขตที่กำหนด",
                    "details": result
                }
            
            # Call original function
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Export all
__all__ = [
    'RateLimitConfig',
    'RateLimitState',
    'TokenBucket',
    'RateLimiter',
    'rate_limit',
]
