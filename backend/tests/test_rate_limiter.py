import pytest
import time
from backend.app.core.rate_limiter import TokenBucketRateLimiter, TenantTier

def test_rate_limiter_allow_under_quota():
    limiter = TokenBucketRateLimiter()
    tenant_key = "tenant_alpha:api"
    
    allowed, retry_after, remaining = limiter.check_rate_limit(tenant_key, TenantTier.STARTER, cost=1.0)
    assert allowed is True
    assert retry_after == 0.0
    assert remaining >= 60

def test_rate_limiter_burst_exhaustion():
    limiter = TokenBucketRateLimiter()
    tenant_key = "tenant_beta:burst"
    
    # Consume entire burst capacity
    allowed, _, _ = limiter.check_rate_limit(tenant_key, TenantTier.STARTER, cost=70.0)
    assert allowed is True

    # Immediate next request should exceed capacity
    allowed, retry_after, remaining = limiter.check_rate_limit(tenant_key, TenantTier.STARTER, cost=1.0)
    assert allowed is False
    assert retry_after > 0.0
    assert remaining == 0

def test_rate_limiter_enterprise_tier_capacity():
    limiter = TokenBucketRateLimiter()
    tenant_key = "tenant_enterprise:heavy"
    
    allowed, retry_after, remaining = limiter.check_rate_limit(tenant_key, TenantTier.ENTERPRISE, cost=500.0)
    assert allowed is True
    assert remaining >= 800

def test_rate_limiter_reset():
    limiter = TokenBucketRateLimiter()
    tenant_key = "tenant_reset_test"
    
    limiter.check_rate_limit(tenant_key, TenantTier.STARTER, cost=70.0)
    limiter.reset_bucket(tenant_key)
    
    # After reset, full capacity is available again
    allowed, _, remaining = limiter.check_rate_limit(tenant_key, TenantTier.STARTER, cost=1.0)
    assert allowed is True
    assert remaining >= 60
