"""
Advanced Caching Module for SmartSpec Autopilot

Provides advanced caching strategies:
- Multi-level caching (L1/L2)
- Cache warming strategies
- Cache invalidation patterns
- Write-through and write-back caching
- Cache statistics and monitoring
- Distributed cache support (Redis-compatible interface)

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import time
import threading
from typing import Dict, Any, Optional, Callable, List, Set
from dataclasses import dataclass, field
from enum import Enum
from .error_handler import with_error_handling
from .performance_profiler import SimpleCache


class CacheStrategy(Enum):
    """Cache strategies"""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In First Out
    TTL = "ttl"  # Time To Live


class InvalidationStrategy(Enum):
    """Cache invalidation strategies"""
    TIME_BASED = "time_based"  # Invalidate after TTL
    EVENT_BASED = "event_based"  # Invalidate on specific events
    PATTERN_BASED = "pattern_based"  # Invalidate by key pattern
    MANUAL = "manual"  # Manual invalidation only


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    timestamp: float
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    ttl: Optional[int] = None
    tags: Set[str] = field(default_factory=set)
    
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if self.ttl is None:
            return False
        return (time.time() - self.timestamp) > self.ttl
    
    def touch(self):
        """Update access metadata"""
        self.access_count += 1
        self.last_access = time.time()


class MultiLevelCache:
    """Multi-level cache (L1: memory, L2: optional backend)"""
    
    def __init__(
        self,
        l1_max_size: int = 1000,
        l1_ttl: Optional[int] = 300,
        l2_max_size: int = 10000,
        l2_ttl: Optional[int] = 3600,
        strategy: CacheStrategy = CacheStrategy.LRU
    ):
        """
        Initialize multi-level cache.
        
        Args:
            l1_max_size: L1 cache max size
            l1_ttl: L1 cache TTL in seconds
            l2_max_size: L2 cache max size
            l2_ttl: L2 cache TTL in seconds
            strategy: Cache eviction strategy
        """
        self.l1_max_size = l1_max_size
        self.l1_ttl = l1_ttl
        self.l2_max_size = l2_max_size
        self.l2_ttl = l2_ttl
        self.strategy = strategy
        
        # L1 cache (fast, small)
        self.l1_cache: Dict[str, CacheEntry] = {}
        
        # L2 cache (slower, larger)
        self.l2_cache: Dict[str, CacheEntry] = {}
        
        self._lock = threading.Lock()
        
        # Statistics
        self.stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "misses": 0,
            "evictions": 0,
            "promotions": 0  # L2 -> L1
        }
    
    def _evict_l1(self):
        """Evict entry from L1 cache based on strategy"""
        if not self.l1_cache:
            return
        
        if self.strategy == CacheStrategy.LRU:
            # Evict least recently used
            victim_key = min(
                self.l1_cache.keys(),
                key=lambda k: self.l1_cache[k].last_access
            )
        elif self.strategy == CacheStrategy.LFU:
            # Evict least frequently used
            victim_key = min(
                self.l1_cache.keys(),
                key=lambda k: self.l1_cache[k].access_count
            )
        elif self.strategy == CacheStrategy.FIFO:
            # Evict oldest
            victim_key = min(
                self.l1_cache.keys(),
                key=lambda k: self.l1_cache[k].timestamp
            )
        else:  # TTL
            # Evict oldest
            victim_key = min(
                self.l1_cache.keys(),
                key=lambda k: self.l1_cache[k].timestamp
            )
        
        # Move to L2 before evicting
        entry = self.l1_cache[victim_key]
        if len(self.l2_cache) < self.l2_max_size:
            entry.ttl = self.l2_ttl
            self.l2_cache[victim_key] = entry
        
        del self.l1_cache[victim_key]
        self.stats["evictions"] += 1
    
    @with_error_handling
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            # Check L1 cache
            if key in self.l1_cache:
                entry = self.l1_cache[key]
                
                if entry.is_expired():
                    del self.l1_cache[key]
                    self.stats["misses"] += 1
                    return None
                
                entry.touch()
                self.stats["l1_hits"] += 1
                return entry.value
            
            # Check L2 cache
            if key in self.l2_cache:
                entry = self.l2_cache[key]
                
                if entry.is_expired():
                    del self.l2_cache[key]
                    self.stats["misses"] += 1
                    return None
                
                entry.touch()
                self.stats["l2_hits"] += 1
                
                # Promote to L1
                if len(self.l1_cache) >= self.l1_max_size:
                    self._evict_l1()
                
                entry.ttl = self.l1_ttl
                self.l1_cache[key] = entry
                del self.l2_cache[key]
                self.stats["promotions"] += 1
                
                return entry.value
            
            self.stats["misses"] += 1
            return None
    
    @with_error_handling
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[Set[str]] = None
    ):
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional TTL override
            tags: Optional tags for invalidation
        """
        with self._lock:
            # Create entry
            entry = CacheEntry(
                key=key,
                value=value,
                timestamp=time.time(),
                ttl=ttl or self.l1_ttl,
                tags=tags or set()
            )
            
            # Add to L1
            if len(self.l1_cache) >= self.l1_max_size:
                self._evict_l1()
            
            self.l1_cache[key] = entry
    
    @with_error_handling
    def delete(self, key: str):
        """Delete key from all cache levels"""
        with self._lock:
            if key in self.l1_cache:
                del self.l1_cache[key]
            if key in self.l2_cache:
                del self.l2_cache[key]
    
    @with_error_handling
    def invalidate_by_tag(self, tag: str):
        """Invalidate all entries with given tag"""
        with self._lock:
            # Invalidate L1
            to_remove = [
                k for k, v in self.l1_cache.items()
                if tag in v.tags
            ]
            for key in to_remove:
                del self.l1_cache[key]
            
            # Invalidate L2
            to_remove = [
                k for k, v in self.l2_cache.items()
                if tag in v.tags
            ]
            for key in to_remove:
                del self.l2_cache[key]
    
    @with_error_handling
    def invalidate_by_pattern(self, pattern: str):
        """Invalidate all entries matching pattern"""
        with self._lock:
            # Invalidate L1
            to_remove = [
                k for k in self.l1_cache.keys()
                if pattern in k
            ]
            for key in to_remove:
                del self.l1_cache[key]
            
            # Invalidate L2
            to_remove = [
                k for k in self.l2_cache.keys()
                if pattern in k
            ]
            for key in to_remove:
                del self.l2_cache[key]
    
    @with_error_handling
    def clear(self):
        """Clear all cache levels"""
        with self._lock:
            self.l1_cache.clear()
            self.l2_cache.clear()
    
    @with_error_handling
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            total_requests = (
                self.stats["l1_hits"] +
                self.stats["l2_hits"] +
                self.stats["misses"]
            )
            
            hit_rate = (
                (self.stats["l1_hits"] + self.stats["l2_hits"]) /
                total_requests * 100
                if total_requests > 0 else 0
            )
            
            return {
                "l1_size": len(self.l1_cache),
                "l1_max_size": self.l1_max_size,
                "l2_size": len(self.l2_cache),
                "l2_max_size": self.l2_max_size,
                "l1_hits": self.stats["l1_hits"],
                "l2_hits": self.stats["l2_hits"],
                "misses": self.stats["misses"],
                "evictions": self.stats["evictions"],
                "promotions": self.stats["promotions"],
                "hit_rate": hit_rate,
                "total_requests": total_requests
            }


class CacheWarmer:
    """Cache warming strategies"""
    
    def __init__(self, cache: MultiLevelCache):
        """
        Initialize cache warmer.
        
        Args:
            cache: Cache instance to warm
        """
        self.cache = cache
        self._warming_tasks: Dict[str, Callable] = {}
        self._lock = threading.Lock()
    
    @with_error_handling
    def register_warming_task(
        self,
        name: str,
        loader: Callable[[], Dict[str, Any]]
    ):
        """
        Register a cache warming task.
        
        Args:
            name: Task name
            loader: Function that returns dict of key-value pairs to cache
        """
        with self._lock:
            self._warming_tasks[name] = loader
    
    @with_error_handling
    def warm(self, task_name: Optional[str] = None):
        """
        Warm cache with data.
        
        Args:
            task_name: Optional specific task to run, or all if None
        """
        with self._lock:
            if task_name:
                if task_name not in self._warming_tasks:
                    return {
                        "success": False,
                        "error": f"Task {task_name} not found"
                    }
                
                loader = self._warming_tasks[task_name]
                data = loader()
                
                for key, value in data.items():
                    self.cache.set(key, value)
                
                return {
                    "success": True,
                    "task": task_name,
                    "items_loaded": len(data)
                }
            else:
                # Run all tasks
                total_items = 0
                for name, loader in self._warming_tasks.items():
                    data = loader()
                    for key, value in data.items():
                        self.cache.set(key, value)
                    total_items += len(data)
                
                return {
                    "success": True,
                    "tasks_run": len(self._warming_tasks),
                    "items_loaded": total_items
                }


class WriteThroughCache:
    """Write-through cache (writes go to cache and backend)"""
    
    def __init__(
        self,
        cache: MultiLevelCache,
        backend_writer: Callable[[str, Any], None]
    ):
        """
        Initialize write-through cache.
        
        Args:
            cache: Cache instance
            backend_writer: Function to write to backend (key, value)
        """
        self.cache = cache
        self.backend_writer = backend_writer
    
    @with_error_handling
    def set(self, key: str, value: Any, **kwargs):
        """
        Set value in cache and backend.
        
        Args:
            key: Cache key
            value: Value to set
            **kwargs: Additional arguments for cache.set()
        """
        # Write to backend first
        self.backend_writer(key, value)
        
        # Then write to cache
        self.cache.set(key, value, **kwargs)
        
        return {"success": True, "key": key}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self.cache.get(key)


class WriteBackCache:
    """Write-back cache (writes go to cache, synced to backend later)"""
    
    def __init__(
        self,
        cache: MultiLevelCache,
        backend_writer: Callable[[str, Any], None],
        sync_interval: int = 60
    ):
        """
        Initialize write-back cache.
        
        Args:
            cache: Cache instance
            backend_writer: Function to write to backend
            sync_interval: Sync interval in seconds
        """
        self.cache = cache
        self.backend_writer = backend_writer
        self.sync_interval = sync_interval
        
        self.dirty_keys: Set[str] = set()
        self._lock = threading.Lock()
        
        # Start background sync thread
        self._sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._sync_thread.start()
    
    def _sync_loop(self):
        """Background sync loop"""
        while True:
            time.sleep(self.sync_interval)
            self.sync()
    
    @with_error_handling
    def set(self, key: str, value: Any, **kwargs):
        """
        Set value in cache (mark as dirty).
        
        Args:
            key: Cache key
            value: Value to set
            **kwargs: Additional arguments for cache.set()
        """
        self.cache.set(key, value, **kwargs)
        
        with self._lock:
            self.dirty_keys.add(key)
        
        return {"success": True, "key": key}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self.cache.get(key)
    
    @with_error_handling
    def sync(self):
        """Sync dirty keys to backend"""
        with self._lock:
            keys_to_sync = list(self.dirty_keys)
            self.dirty_keys.clear()
        
        synced = 0
        for key in keys_to_sync:
            result = self.cache.get(key)
            # Unwrap if wrapped by @with_error_handling
            if isinstance(result, dict) and "result" in result:
                value = result["result"]
            else:
                value = result
            
            if value is not None:
                self.backend_writer(key, value)
                synced += 1
        
        return {
            "success": True,
            "synced": synced
        }


# Export all
__all__ = [
    'CacheStrategy',
    'InvalidationStrategy',
    'CacheEntry',
    'MultiLevelCache',
    'CacheWarmer',
    'WriteThroughCache',
    'WriteBackCache',
]
