import time
import logging
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.context import TenantContext
from app.config import settings

logger = logging.getLogger(__name__)


class TenantSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        TenantContext.clear()

        # Public endpoints that bypass tenant header requirement
        public_paths = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            f"{settings.API_V1_STR}/auth/login",
            f"{settings.API_V1_STR}/auth/register-tenant",
            f"{settings.API_V1_STR}/webhooks",
        ]

        path = request.url.path
        is_public = any(path.startswith(p) for p in public_paths)

        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            TenantContext.set_tenant_id(tenant_id)

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            response.headers["X-Process-Time-MS"] = f"{process_time:.2f}"
            return response
        except Exception as exc:
            logger.error(f"Unhandled exception during request to {path}: {exc}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error occurred.", "path": path}
            )
        finally:
            TenantContext.clear()
