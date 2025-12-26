# SmartSpec Autopilot Integration Guide

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** Phase 1 Complete

---

## 📋 Overview

SmartSpec Autopilot now includes a comprehensive integration layer that adds advanced features to all agents without modifying their original code.

### Features

- ✅ **Advanced Logging** - Structured JSON logs with correlation IDs
- ✅ **Input Validation** - Automatic path sanitization and schema validation
- ✅ **Performance Profiling** - Track execution time of all operations
- ✅ **Result Caching** - Cache expensive operations (optional)
- ✅ **Rate Limiting** - Prevent abuse (optional)

---

## 🚀 Quick Start

### Option 1: Use Pre-configured Agents (Recommended)

```python
from .integrated_agents import (
    get_orchestrator_agent,
    get_status_agent,
    get_intent_parser_agent,
    get_workflow_catalog
)

# Get wrapped agents with all features enabled
orchestrator = get_orchestrator_agent()
status = get_status_agent()
intent_parser = get_intent_parser_agent()
catalog = get_workflow_catalog()

# Use as normal - all features work automatically!
state = orchestrator.read_state("spec-core-001")
```

### Option 2: Wrap Custom Agents

```python
from .agent_wrapper import wrap_agent
from .my_agent import MyAgent

# Create your agent
agent = MyAgent()

# Wrap with features
wrapped = wrap_agent(
    agent,
    "my_agent",
    enable_logging=True,
    enable_validation=True,
    enable_profiling=True,
    enable_caching=True,
    enable_rate_limiting=False
)

# Use wrapped agent
result = wrapped.my_method("input")
```

---

## 📦 Available Agents

### 1. Orchestrator Agent

**Features:**
- Logging: ✅
- Validation: ✅
- Profiling: ✅
- Caching: ✅ (state reads, workflow searches)
- Rate limiting: ❌

**Usage:**
```python
from .integrated_agents import get_orchestrator_agent

agent = get_orchestrator_agent()

# All methods automatically logged, validated, profiled, cached
state = agent.read_state("spec-core-001")
recommendation = agent.recommend_next_workflow(state)
```

### 2. Status Agent

**Features:**
- Logging: ✅
- Validation: ✅
- Profiling: ✅
- Caching: ✅ (status queries)
- Rate limiting: ❌

**Usage:**
```python
from .integrated_agents import get_status_agent

agent = get_status_agent()

# Query status with automatic caching
status = agent.query("What is the status of spec-core-001?")
```

### 3. Intent Parser Agent

**Features:**
- Logging: ✅
- Validation: ✅
- Profiling: ✅
- Caching: ✅ (parsed intents)
- Rate limiting: ✅ (30 req/min)

**Usage:**
```python
from .integrated_agents import get_intent_parser_agent

agent = get_intent_parser_agent()

# Parse intent with rate limiting
intent = agent.parse("Create a new spec for user authentication")
```

### 4. Workflow Catalog

**Features:**
- Logging: ✅
- Validation: ✅
- Profiling: ✅
- Caching: ✅ (workflow searches)
- Rate limiting: ❌

**Usage:**
```python
from .integrated_agents import get_workflow_catalog

catalog = get_workflow_catalog()

# Search workflows with caching
workflows = catalog.search("generate spec")
```

---

## 🔧 Configuration

### Enable/Disable Features

```python
from .agent_wrapper import wrap_agent
from .my_agent import MyAgent

agent = MyAgent()

# Customize features
wrapped = wrap_agent(
    agent,
    "my_agent",
    enable_logging=True,        # ✅ Enable logging
    enable_validation=False,    # ❌ Disable validation
    enable_profiling=True,      # ✅ Enable profiling
    enable_caching=False,       # ❌ Disable caching
    enable_rate_limiting=False  # ❌ Disable rate limiting
)
```

### Configure Rate Limiting

```python
from .agent_wrapper import wrap_agent
from .rate_limiter import RateLimitConfig

config = RateLimitConfig(
    max_requests=10,      # 10 requests
    time_window=60,       # per 60 seconds
    cooldown_period=30    # 30 second cooldown
)

wrapped = wrap_agent(
    agent,
    "my_agent",
    enable_rate_limiting=True,
    rate_limit_config=config
)
```

---

## 📊 Monitoring

### View Logs

Logs are written to `logs/smartspec_autopilot.log` in JSON format:

```json
{
  "timestamp": "2025-12-26T10:30:00",
  "level": "INFO",
  "logger": "orchestrator",
  "message": "Starting orchestrator.read_state",
  "args": "('spec-core-001',)",
  "correlation_id": "abc123"
}
```

### View Performance Metrics

```python
from .performance_profiler import _profiler

# Get stats for a function
stats = _profiler.get_metrics("orchestrator.read_state")

print(f"Total calls: {stats['calls']}")
print(f"Avg time: {stats['avg_time']:.3f}s")
print(f"Max time: {stats['max_time']:.3f}s")
```

### View Cache Statistics

```python
from .integrated_agents import get_orchestrator_agent

agent = get_orchestrator_agent()

# Access cache through wrapper
cache_stats = agent.cache.get_stats()

print(f"L1 hits: {cache_stats['l1_hits']}")
print(f"L2 hits: {cache_stats['l2_hits']}")
print(f"Misses: {cache_stats['misses']}")
```

---

## 🎯 Best Practices

### 1. Use Pre-configured Agents

```python
# ✅ Good
from .integrated_agents import get_orchestrator_agent
agent = get_orchestrator_agent()

# ❌ Bad
from .orchestrator_agent import OrchestratorAgent
agent = OrchestratorAgent()  # No integration features!
```

### 2. Enable Caching for Expensive Operations

```python
# ✅ Good - Cache expensive operations
wrapped = wrap_agent(
    agent,
    "my_agent",
    enable_caching=True
)

# ❌ Bad - Don't cache operations that change frequently
wrapped = wrap_agent(
    status_writer,
    "status_writer",
    enable_caching=True  # Status changes frequently!
)
```

### 3. Use Rate Limiting for User-facing APIs

```python
# ✅ Good - Rate limit user inputs
intent_parser = get_intent_parser_agent()  # Has rate limiting

# ❌ Bad - Don't rate limit internal operations
orchestrator = get_orchestrator_agent()  # No rate limiting
```

### 4. Monitor Performance Regularly

```python
from .performance_profiler import _profiler, BottleneckAnalyzer

# Analyze bottlenecks
analyzer = BottleneckAnalyzer(_profiler)
report = analyzer.analyze()

print(report["summary"])
for bottleneck in report["bottlenecks"]:
    print(f"Slow: {bottleneck['function']} - {bottleneck['avg_time']:.3f}s")
```

---

## 🐛 Troubleshooting

### Issue: Logs not appearing

**Solution:** Check log level and file permissions

```python
from .advanced_logger import get_logger

logger = get_logger("my_agent")
logger.setLevel("DEBUG")  # Set to DEBUG to see all logs
```

### Issue: Cache not working

**Solution:** Verify caching is enabled

```python
# Check if caching is enabled
print(wrapped.enable_caching)  # Should be True

# Clear cache if needed
wrapped.cache.clear()
```

### Issue: Rate limit errors

**Solution:** Adjust rate limit configuration

```python
from .rate_limiter import RateLimitConfig

# Increase limits
config = RateLimitConfig(
    max_requests=100,  # Increase from 30
    time_window=60
)
```

---

## 📚 API Reference

### AgentWrapper

```python
class AgentWrapper:
    def __init__(
        self,
        agent: Any,
        agent_name: str,
        enable_logging: bool = True,
        enable_validation: bool = True,
        enable_rate_limiting: bool = False,
        enable_profiling: bool = True,
        enable_caching: bool = False,
        rate_limit_config: Optional[RateLimitConfig] = None
    )
```

### wrap_agent()

```python
def wrap_agent(
    agent: Any,
    agent_name: str,
    **kwargs
) -> AgentWrapper
```

### Integrated Agents

```python
def get_orchestrator_agent(workflows_dir: str = None) -> AgentWrapper
def get_status_agent() -> AgentWrapper
def get_intent_parser_agent() -> AgentWrapper
def get_workflow_catalog(workflows_dir: str = None) -> AgentWrapper
def get_all_agents(workflows_dir: str = None) -> dict
```

---

## 🎊 Summary

**Phase 1 Integration provides:**

- ✅ Non-invasive integration layer
- ✅ Advanced logging everywhere
- ✅ Input validation everywhere
- ✅ Performance profiling everywhere
- ✅ Optional caching
- ✅ Optional rate limiting
- ✅ Easy to enable/disable features
- ✅ Zero changes to existing code

**Next Steps:**

- Phase 2: Add checkpointing and streaming
- Phase 3: Add parallel execution
- Phase 4: Add human-in-the-loop

---

**Questions?** Check the test files for more examples:
- `tests/ss_autopilot/test_agent_wrapper.py`
- `tests/ss_autopilot/test_integrated_agents.py` (coming soon)
