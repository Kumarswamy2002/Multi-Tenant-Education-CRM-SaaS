import hmac
import hashlib
import time
import struct
import base64
from typing import Tuple


class MFAEngine:
    """
    TOTP (Time-based One-Time Password) engine for Multi-Factor Authentication.
    Uses RFC 6238 standard TOTP generation and verification.
    """

    @staticmethod
    def generate_secret() -> str:
        random_bytes = base64.b32encode(hashlib.sha256(str(time.time()).encode()).digest()[:10]).decode('utf-8')
        return random_bytes.replace("=", "")

    @staticmethod
    def generate_totp(secret: str, time_step: int = 30) -> str:
        key = base64.b32decode(secret + '=' * (8 - len(secret) % 8), True)
        counter = int(time.time() // time_step)
        msg = struct.pack(">Q", counter)
        h = hmac.new(key, msg, hashlib.sha1).digest()
        offset = h[-1] & 0x0F
        code = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
        return f"{code:06d}"

    @classmethod
    def verify_totp(cls, secret: str, user_code: str, time_step: int = 30) -> bool:
        if not secret or not user_code:
            return False
        # Allow +/- 1 time step window for clock drift tolerance
        for offset in [-1, 0, 1]:
            counter = int((time.time() // time_step) + offset)
            key = base64.b32decode(secret + '=' * (8 - len(secret) % 8), True)
            msg = struct.pack(">Q", counter)
            h = hmac.new(key, msg, hashlib.sha1).digest()
            off = h[-1] & 0x0F
            code = (struct.unpack(">I", h[off:off + 4])[0] & 0x7FFFFFFF) % 1000000
            if f"{code:06d}" == user_code:
                return True
        return False
