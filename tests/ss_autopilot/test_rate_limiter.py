"""
Unit tests for rate_limiter.py

Tests:
- RateLimitConfig validation
- TokenBucket token refilling
- TokenBucket token consumption
- TokenBucket cooldown
- RateLimiter multi-tier
- RateLimiter per-identifier tracking
- @rate_limit decorator
"""

import pytest
import time
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.rate_limiter import (
    RateLimitConfig,
    RateLimitState,
    TokenBucket,
    RateLimiter,
    rate_limit
)


# ============================================================================
# Test RateLimitConfig
# ============================================================================

class TestRateLimitConfig:
    """Test RateLimitConfig validation"""
    
    def test_valid_config(self):
        """Test creating valid config"""
        config = RateLimitConfig(max_requests=10, time_window=60, cooldown=30)
        assert config.max_requests == 10
        assert config.time_window == 60
        assert config.cooldown == 30
    
    def test_invalid_max_requests(self):
        """Test invalid max_requests"""
        with pytest.raises(ValueError):
            RateLimitConfig(max_requests=0, time_window=60)
    
    def test_invalid_time_window(self):
        """Test invalid time_window"""
        with pytest.raises(ValueError):
            RateLimitConfig(max_requests=10, time_window=0)
    
    def test_invalid_cooldown(self):
        """Test invalid cooldown"""
        with pytest.raises(ValueError):
            RateLimitConfig(max_requests=10, time_window=60, cooldown=-1)


# ============================================================================
# Test TokenBucket
# ============================================================================

class TestTokenBucket:
    """Test TokenBucket implementation"""
    
    def test_initial_tokens(self):
        """Test initial token count"""
        config = RateLimitConfig(max_requests=10, time_window=60)
        bucket = TokenBucket(config)
        
        stats = bucket.get_stats()
        assert stats["tokens_remaining"] == 10
        assert stats["tokens_max"] == 10
    
    def test_consume_tokens(self):
        """Test consuming tokens"""
        config = RateLimitConfig(max_requests=10, time_window=60)
        bucket = TokenBucket(config)
        
        # Consume 1 token
        allowed, info = bucket.consume(1)
        assert allowed is True
        assert info["allowed"] is True
        assert info["tokens_remaining"] < 10
    
    def test_consume_multiple_tokens(self):
        """Test consuming multiple tokens"""
        config = RateLimitConfig(max_requests=10, time_window=60)
        bucket = TokenBucket(config)
        
        # Consume 5 tokens
        allowed, info = bucket.consume(5)
        assert allowed is True
        assert info["tokens_remaining"] == 5
    
    def test_rate_limit_exceeded(self):
        """Test rate limit exceeded"""
        config = RateLimitConfig(max_requests=2, time_window=60)
        bucket = TokenBucket(config)
        
        # Consume all tokens
        bucket.consume(2)
        
        # Try to consume more
        allowed, info = bucket.consume(1)
        assert allowed is False
        assert info["reason"] == "rate_limit_exceeded"
    
    def test_token_refill(self):
        """Test token refilling over time"""
        config = RateLimitConfig(max_requests=10, time_window=1)  # 10 tokens per second
        bucket = TokenBucket(config)
        
        # Consume all tokens
        bucket.consume(10)
        
        # Wait for refill
        time.sleep(0.5)  # Should refill ~5 tokens
        
        # Should be able to consume some tokens
        allowed, info = bucket.consume(3)
        assert allowed is True
    
    def test_cooldown_period(self):
        """Test cooldown period after rate limit"""
        config = RateLimitConfig(max_requests=2, time_window=60, cooldown=1)
        bucket = TokenBucket(config)
        
        # Consume all tokens
        bucket.consume(2)
        
        # Try to consume more (should trigger cooldown)
        allowed, info = bucket.consume(1)
        assert allowed is False
        assert info["reason"] == "rate_limit_exceeded"
        
        # Try again immediately (should be in cooldown)
        allowed, info = bucket.consume(1)
        assert allowed is False
        assert info["reason"] == "cooldown"
        assert "cooldown_remaining" in info
    
    def test_stats(self):
        """Test getting statistics"""
        config = RateLimitConfig(max_requests=10, time_window=60)
        bucket = TokenBucket(config)
        
        # Make some requests
        bucket.consume(1)
        bucket.consume(1)
        bucket.consume(20)  # This will be blocked
        
        stats = bucket.get_stats()
        assert stats["total_requests"] == 2
        assert stats["blocked_requests"] == 1
        assert "success_rate" in stats
    
    def test_reset(self):
        """Test resetting bucket"""
        config = RateLimitConfig(max_requests=10, time_window=60)
        bucket = TokenBucket(config)
        
        # Consume tokens
        bucket.consume(5)
        
        # Reset
        bucket.reset()
        
        # Should have full tokens again
        stats = bucket.get_stats()
        assert stats["tokens_remaining"] == 10
        assert stats["total_requests"] == 0


# ============================================================================
# Test RateLimiter
# ============================================================================

class TestRateLimiter:
    """Test RateLimiter multi-tier system"""
    
    def test_default_tier(self):
        """Test default tier initialization"""
        limiter = RateLimiter(default_tier="moderate")
        
        result = limiter.check_rate_limit("user1")
        assert result["success"] is True
        assert result["allowed"] is True
    
    def test_invalid_tier(self):
        """Test invalid tier raises error"""
        with pytest.raises(ValueError):
            RateLimiter(default_tier="invalid")
    
    def test_per_identifier_tracking(self):
        """Test separate tracking per identifier"""
        limiter = RateLimiter(default_tier="strict")  # 10 req/min
        
        # User1 makes requests
        for i in range(10):
            result = limiter.check_rate_limit("user1")
            assert result["allowed"] is True
        
        # User1 exceeds limit
        result = limiter.check_rate_limit("user1")
        assert result["allowed"] is False
        
        # User2 should still be allowed
        result = limiter.check_rate_limit("user2")
        assert result["allowed"] is True
    
    def test_tier_override(self):
        """Test tier override per request"""
        limiter = RateLimiter(default_tier="strict")
        
        # Use relaxed tier for this request
        result = limiter.check_rate_limit("user1", tier="relaxed")
        assert result["success"] is True
    
    def test_get_stats(self):
        """Test getting stats for identifier"""
        limiter = RateLimiter(default_tier="moderate")
        
        # Make some requests
        limiter.check_rate_limit("user1")
        limiter.check_rate_limit("user1")
        
        # Get stats
        stats = limiter.get_stats("user1")
        assert stats["success"] is True
        assert stats["exists"] is True
        assert "total_requests" in stats
    
    def test_get_stats_nonexistent(self):
        """Test getting stats for non-existent identifier"""
        limiter = RateLimiter(default_tier="moderate")
        
        stats = limiter.get_stats("nonexistent")
        assert stats["success"] is True
        assert stats["exists"] is False
    
    def test_reset_identifier(self):
        """Test resetting rate limit for identifier"""
        limiter = RateLimiter(default_tier="strict")
        
        # Consume all tokens
        for i in range(10):
            limiter.check_rate_limit("user1")
        
        # Should be rate limited
        result = limiter.check_rate_limit("user1")
        assert result["allowed"] is False
        
        # Reset
        reset_result = limiter.reset("user1")
        assert reset_result["success"] is True
        assert reset_result["reset"] is True
        
        # Should be allowed again
        result = limiter.check_rate_limit("user1")
        assert result["allowed"] is True
    
    def test_get_all_stats(self):
        """Test getting all statistics"""
        limiter = RateLimiter(default_tier="moderate")
        
        # Make requests from multiple users
        limiter.check_rate_limit("user1")
        limiter.check_rate_limit("user2")
        limiter.check_rate_limit("user3")
        
        # Get all stats
        all_stats = limiter.get_all_stats()
        assert all_stats["success"] is True
        assert all_stats["total_identifiers"] == 3
        assert "user1" in all_stats["stats"]
        assert "user2" in all_stats["stats"]
        assert "user3" in all_stats["stats"]
    
    def test_cleanup_inactive(self):
        """Test cleanup of inactive buckets"""
        limiter = RateLimiter(default_tier="moderate")
        
        # Make requests
        limiter.check_rate_limit("user1")
        limiter.check_rate_limit("user2")
        
        # Cleanup with 0 seconds (should remove all)
        removed = limiter.cleanup_inactive(inactive_seconds=0)
        assert removed == 2


# ============================================================================
# Test @rate_limit Decorator
# ============================================================================

class TestRateLimitDecorator:
    """Test @rate_limit decorator"""
    
    def test_decorator_allows_request(self):
        """Test decorator allows valid requests"""
        @rate_limit(identifier_key="user_id", tier="relaxed")
        def process_request(user_id: str, data: dict):
            return {"success": True, "data": data}
        
        result = process_request(user_id="user1", data={"test": "data"})
        assert result["success"] is True
        assert result["data"]["test"] == "data"
    
    def test_decorator_blocks_excessive_requests(self):
        """Test decorator blocks excessive requests"""
        @rate_limit(identifier_key="user_id", tier="strict")
        def process_request(user_id: str):
            return {"success": True}
        
        # Make requests up to limit
        for i in range(10):
            result = process_request(user_id="user2")
            assert result["success"] is True
        
        # Next request should be blocked
        result = process_request(user_id="user2")
        assert result.get("error") is True
        assert result.get("error_code") == "RATE_LIMIT_EXCEEDED"


# ============================================================================
# Test Rate Limit Tiers
# ============================================================================

class TestRateLimitTiers:
    """Test different rate limit tiers"""
    
    def test_strict_tier(self):
        """Test strict tier (10 req/min)"""
        limiter = RateLimiter(default_tier="strict")
        
        # Should allow 10 requests
        for i in range(10):
            result = limiter.check_rate_limit("user1")
            assert result["allowed"] is True
        
        # 11th request should be blocked
        result = limiter.check_rate_limit("user1")
        assert result["allowed"] is False
    
    def test_moderate_tier(self):
        """Test moderate tier (30 req/min)"""
        limiter = RateLimiter(default_tier="moderate")
        
        # Should allow 30 requests
        for i in range(30):
            result = limiter.check_rate_limit("user1")
            assert result["allowed"] is True
        
        # 31st request should be blocked
        result = limiter.check_rate_limit("user1")
        assert result["allowed"] is False
    
    def test_relaxed_tier(self):
        """Test relaxed tier (100 req/min)"""
        limiter = RateLimiter(default_tier="relaxed")
        
        # Should allow 100 requests
        for i in range(100):
            result = limiter.check_rate_limit("user1")
            assert result["allowed"] is True
        
        # 101st request should be blocked
        result = limiter.check_rate_limit("user1")
        assert result["allowed"] is False
    
    def test_unlimited_tier(self):
        """Test unlimited tier (10000 req/sec)"""
        limiter = RateLimiter(default_tier="unlimited")
        
        # Should allow many requests
        for i in range(1000):
            result = limiter.check_rate_limit("user1")
            assert result["allowed"] is True


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
