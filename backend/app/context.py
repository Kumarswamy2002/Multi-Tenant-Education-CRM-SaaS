from contextvars import ContextVar
from typing import Optional, List
from fastapi import HTTPException, status

_tenant_id_ctx: ContextVar[Optional[str]] = ContextVar("tenant_id", default=None)
_user_id_ctx: ContextVar[Optional[str]] = ContextVar("user_id", default=None)
_user_roles_ctx: ContextVar[List[str]] = ContextVar("user_roles", default=[])
_is_super_admin_ctx: ContextVar[bool] = ContextVar("is_super_admin", default=False)


class TenantContext:
    @staticmethod
    def get_tenant_id() -> Optional[str]:
        return _tenant_id_ctx.get()

    @staticmethod
    def require_tenant_id() -> str:
        tid = _tenant_id_ctx.get()
        if not tid and not _is_super_admin_ctx.get():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant context missing. Operation denied."
            )
        return tid or "system"

    @staticmethod
    def set_tenant_id(tenant_id: Optional[str]) -> None:
        _tenant_id_ctx.set(tenant_id)

    @staticmethod
    def get_user_id() -> Optional[str]:
        return _user_id_ctx.get()

    @staticmethod
    def set_user_id(user_id: Optional[str]) -> None:
        _user_id_ctx.set(user_id)

    @staticmethod
    def get_user_roles() -> List[str]:
        return _user_roles_ctx.get()

    @staticmethod
    def set_user_roles(roles: List[str]) -> None:
        _user_roles_ctx.set(roles)

    @staticmethod
    def is_super_admin() -> bool:
        return _is_super_admin_ctx.get()

    @staticmethod
    def set_super_admin(is_admin: bool) -> None:
        _is_super_admin_ctx.set(is_admin)

    @staticmethod
    def clear() -> None:
        _tenant_id_ctx.set(None)
        _user_id_ctx.set(None)
        _user_roles_ctx.set([])
        _is_super_admin_ctx.set(False)


def get_current_tenant_id() -> str:
    tid = TenantContext.get_tenant_id()
    return tid or "default-tenant"


def get_current_user() -> Optional[str]:
    return TenantContext.get_user_id()

