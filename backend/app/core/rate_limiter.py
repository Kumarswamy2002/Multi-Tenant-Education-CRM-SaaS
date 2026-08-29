"""
Multi-Tenant Token-Bucket & Sliding-Window Rate Limiting Engine.
Enforces tiered request quotas (Starter, Pro, Enterprise) per tenant and client IP.
"""

import time
from typing import Dict, Tuple, Optional
from enum import Enum

class TenantTier(str, Enum):
    STARTER = "STARTER"      # 60 req/min, burst 10
    PRO = "PRO"              # 300 req/min, burst 50
    ENTERPRISE = "ENTERPRISE" # 1200 req/min, burst 200

TIER_LIMITS: Dict[TenantTier, Tuple[int, int]] = {
    TenantTier.STARTER: (60, 10),
    TenantTier.PRO: (300, 50),
    TenantTier.ENTERPRISE: (1200, 200),
}

class TokenBucketRateLimiter:
    def __init__(self):
        # key -> (tokens, last_refill_timestamp, max_capacity, refill_rate_per_sec)
        self._buckets: Dict[str, Dict[str, float]] = {}

    def _get_bucket_params(self, tier: TenantTier) -> Tuple[float, float]:
        rate_per_min, burst = TIER_LIMITS.get(tier, (60, 10))
        refill_rate = rate_per_min / 60.0
        max_capacity = float(rate_per_min + burst)
        return refill_rate, max_capacity

    def check_rate_limit(
        self,
        identifier: str,
        tier: TenantTier = TenantTier.STARTER,
        cost: float = 1.0
    ) -> Tuple[bool, float, int]:
        """
        Evaluates rate limit using Token Bucket algorithm.
        Returns: (is_allowed, retry_after_seconds, remaining_tokens_int)
        """
        now = time.time()
        refill_rate, max_capacity = self._get_bucket_params(tier)

        bucket = self._buckets.get(identifier)
        if bucket is None:
            bucket = {
                "tokens": max_capacity,
                "last_refill": now,
                "capacity": max_capacity,
                "rate": refill_rate
            }
            self._buckets[identifier] = bucket

        # Refill tokens based on elapsed time
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(bucket["capacity"], bucket["tokens"] + (elapsed * bucket["rate"]))
        bucket["last_refill"] = now

        if bucket["tokens"] >= cost:
            bucket["tokens"] -= cost
            remaining = int(bucket["tokens"])
            return True, 0.0, remaining
        else:
            needed = cost - bucket["tokens"]
            retry_after = round(needed / bucket["rate"], 2)
            return False, retry_after, 0

    def reset_bucket(self, identifier: str) -> None:
        if identifier in self._buckets:
            del self._buckets[identifier]
