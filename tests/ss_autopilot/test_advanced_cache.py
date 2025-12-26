"""
Unit tests for advanced_cache.py

Tests:
- CacheEntry metadata
- MultiLevelCache L1/L2
- Cache eviction strategies
- Cache invalidation
- CacheWarmer
- WriteThroughCache
- WriteBackCache
"""

import pytest
import time
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.advanced_cache import (
    CacheStrategy,
    InvalidationStrategy,
    CacheEntry,
    MultiLevelCache,
    CacheWarmer,
    WriteThroughCache,
    WriteBackCache
)


# ============================================================================
# Helper Functions
# ============================================================================

def unwrap(result):
    """Unwrap result from @with_error_handling decorator"""
    if isinstance(result, dict) and "result" in result:
        return result["result"]
    return result


# ============================================================================
# Test CacheEntry
# ============================================================================

class TestCacheEntry:
    """Test CacheEntry class"""
    
    def test_cache_entry_creation(self):
        """Test creating cache entry"""
        entry = CacheEntry(
            key="test_key",
            value="test_value",
            timestamp=time.time(),
            ttl=300
        )
        assert entry.key == "test_key"
        assert entry.value == "test_value"
        assert entry.access_count == 0
    
    def test_cache_entry_expiration(self):
        """Test cache entry expiration"""
        entry = CacheEntry(
            key="test",
            value="value",
            timestamp=time.time() - 400,  # 400 seconds ago
            ttl=300  # 5 minutes TTL
        )
        assert entry.is_expired() is True
    
    def test_cache_entry_touch(self):
        """Test cache entry touch"""
        entry = CacheEntry(
            key="test",
            value="value",
            timestamp=time.time()
        )
        
        initial_count = entry.access_count
        entry.touch()
        
        assert entry.access_count == initial_count + 1
    
    def test_cache_entry_tags(self):
        """Test cache entry tags"""
        entry = CacheEntry(
            key="test",
            value="value",
            timestamp=time.time(),
            tags={"user", "profile"}
        )
        assert "user" in entry.tags
        assert "profile" in entry.tags


# ============================================================================
# Test MultiLevelCache
# ============================================================================

class TestMultiLevelCache:
    """Test MultiLevelCache class"""
    
    def test_l1_cache_hit(self):
        """Test L1 cache hit"""
        cache = MultiLevelCache(l1_max_size=10, l2_max_size=100)
        
        cache.set("key1", "value1")
        result = unwrap(cache.get("key1"))
        
        assert result == "value1"
        stats = unwrap(cache.get_stats())
        assert stats["l1_hits"] == 1
    
    def test_l2_cache_hit_and_promotion(self):
        """Test L2 cache hit and promotion to L1"""
        cache = MultiLevelCache(l1_max_size=2, l2_max_size=10)
        
        # Fill L1
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # This will evict key1 to L2
        cache.set("key3", "value3")
        
        # Access key1 (should be in L2, then promoted to L1)
        result = unwrap(cache.get("key1"))
        
        assert result == "value1"
        stats = unwrap(cache.get_stats())
        assert stats["l2_hits"] >= 1
        assert stats["promotions"] >= 1
    
    def test_cache_miss(self):
        """Test cache miss"""
        cache = MultiLevelCache()
        
        result = unwrap(cache.get("nonexistent"))
        
        assert result is None
        stats = unwrap(cache.get_stats())
        assert stats["misses"] == 1
    
    def test_lru_eviction(self):
        """Test LRU eviction strategy"""
        cache = MultiLevelCache(
            l1_max_size=3,
            strategy=CacheStrategy.LRU
        )
        
        # Fill cache
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        
        # Access key1 to make it recently used
        cache.get("key1")
        
        # Add new key (should evict key2, least recently used)
        cache.set("key4", "value4")
        
        # key2 should be evicted to L2
        stats = unwrap(cache.get_stats())
        assert stats["evictions"] >= 1
    
    def test_ttl_expiration(self):
        """Test TTL expiration"""
        cache = MultiLevelCache(l1_ttl=1)  # 1 second TTL
        
        cache.set("key1", "value1")
        
        # Wait for expiration
        time.sleep(1.1)
        
        result = unwrap(cache.get("key1"))
        assert result is None
    
    def test_delete(self):
        """Test cache delete"""
        cache = MultiLevelCache()
        
        cache.set("key1", "value1")
        cache.delete("key1")
        
        result = unwrap(cache.get("key1"))
        assert result is None
    
    def test_invalidate_by_tag(self):
        """Test invalidation by tag"""
        cache = MultiLevelCache()
        
        cache.set("key1", "value1", tags={"user"})
        cache.set("key2", "value2", tags={"user"})
        cache.set("key3", "value3", tags={"admin"})
        
        cache.invalidate_by_tag("user")
        
        assert unwrap(cache.get("key1")) is None
        assert unwrap(cache.get("key2")) is None
        assert unwrap(cache.get("key3")) == "value3"
    
    def test_invalidate_by_pattern(self):
        """Test invalidation by pattern"""
        cache = MultiLevelCache()
        
        cache.set("user:1", "value1")
        cache.set("user:2", "value2")
        cache.set("admin:1", "value3")
        
        cache.invalidate_by_pattern("user:")
        
        assert unwrap(cache.get("user:1")) is None
        assert unwrap(cache.get("user:2")) is None
        assert unwrap(cache.get("admin:1")) == "value3"
    
    def test_clear(self):
        """Test cache clear"""
        cache = MultiLevelCache()
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        
        stats = unwrap(cache.get_stats())
        assert stats["l1_size"] == 0
        assert stats["l2_size"] == 0
    
    def test_hit_rate_calculation(self):
        """Test hit rate calculation"""
        cache = MultiLevelCache()
        
        cache.set("key1", "value1")
        
        # 2 hits
        cache.get("key1")
        cache.get("key1")
        
        # 1 miss
        cache.get("nonexistent")
        
        stats = unwrap(cache.get_stats())
        # 2 hits out of 3 requests = 66.67%
        assert stats["hit_rate"] > 60


# ============================================================================
# Test CacheWarmer
# ============================================================================

class TestCacheWarmer:
    """Test CacheWarmer class"""
    
    def test_register_warming_task(self):
        """Test registering warming task"""
        cache = MultiLevelCache()
        warmer = CacheWarmer(cache)
        
        def load_users():
            return {"user:1": "Alice", "user:2": "Bob"}
        
        warmer.register_warming_task("users", load_users)
        
        # Warm cache
        result = warmer.warm("users")
        
        assert result["success"] is True
        assert result["items_loaded"] == 2
        assert unwrap(cache.get("user:1")) == "Alice"
    
    def test_warm_all_tasks(self):
        """Test warming all tasks"""
        cache = MultiLevelCache()
        warmer = CacheWarmer(cache)
        
        def load_users():
            return {"user:1": "Alice"}
        
        def load_products():
            return {"product:1": "Widget"}
        
        warmer.register_warming_task("users", load_users)
        warmer.register_warming_task("products", load_products)
        
        # Warm all
        result = warmer.warm()
        
        assert result["success"] is True
        assert result["tasks_run"] == 2
        assert result["items_loaded"] == 2


# ============================================================================
# Test WriteThroughCache
# ============================================================================

class TestWriteThroughCache:
    """Test WriteThroughCache class"""
    
    def test_write_through(self):
        """Test write-through cache"""
        cache = MultiLevelCache()
        backend_data = {}
        
        def backend_writer(key, value):
            backend_data[key] = value
        
        wt_cache = WriteThroughCache(cache, backend_writer)
        
        # Write
        wt_cache.set("key1", "value1")
        
        # Check both cache and backend
        assert unwrap(wt_cache.get("key1")) == "value1"
        assert backend_data["key1"] == "value1"


# ============================================================================
# Test WriteBackCache
# ============================================================================

class TestWriteBackCache:
    """Test WriteBackCache class"""
    
    def test_write_back(self):
        """Test write-back cache"""
        cache = MultiLevelCache()
        backend_data = {}
        
        def backend_writer(key, value):
            backend_data[key] = value
        
        wb_cache = WriteBackCache(cache, backend_writer, sync_interval=60)
        
        # Write (goes to cache only)
        wb_cache.set("key1", "value1")
        
        # Check cache (should have value)
        assert unwrap(wb_cache.get("key1")) == "value1"
        
        # Check backend (should NOT have value yet)
        assert "key1" not in backend_data
        
        # Manual sync
        wb_cache.sync()
        
        # Check backend (should have value now)
        assert backend_data["key1"] == "value1"


# ============================================================================
# Integration Tests
# ============================================================================

class TestAdvancedCacheIntegration:
    """Integration tests for advanced cache"""
    
    def test_multi_level_with_warming(self):
        """Test multi-level cache with warming"""
        cache = MultiLevelCache(l1_max_size=5, l2_max_size=20)
        warmer = CacheWarmer(cache)
        
        def load_data():
            return {f"key{i}": f"value{i}" for i in range(10)}
        
        warmer.register_warming_task("data", load_data)
        warmer.warm("data")
        
        # Check data is in cache
        assert unwrap(cache.get("key0")) == "value0"
        assert unwrap(cache.get("key9")) == "value9"
        
        stats = unwrap(cache.get_stats())
        assert stats["l1_size"] + stats["l2_size"] == 10
    
    def test_write_through_with_invalidation(self):
        """Test write-through cache with invalidation"""
        cache = MultiLevelCache()
        backend_data = {}
        
        def backend_writer(key, value):
            backend_data[key] = value
        
        wt_cache = WriteThroughCache(cache, backend_writer)
        
        # Write with tags
        wt_cache.set("user:1", "Alice", tags={"user"})
        wt_cache.set("user:2", "Bob", tags={"user"})
        
        # Invalidate by tag
        cache.invalidate_by_tag("user")
        
        # Cache should be empty
        assert unwrap(wt_cache.get("user:1")) is None
        
        # Backend should still have data
        assert backend_data["user:1"] == "Alice"


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
