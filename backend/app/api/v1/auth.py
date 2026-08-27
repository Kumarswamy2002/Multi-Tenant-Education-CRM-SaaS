from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.schemas.tenant import TenantCreate, TenantResponse
from app.models.tenant import Tenant
from app.models.auth import User, Role, UserRole
from app.models.person import Person
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.context import TenantContext

router = APIRouter(prefix="/auth", tags=["Authentication & Multi-Tenancy"])


@router.post("/register-tenant", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def register_tenant(payload: TenantCreate, db: AsyncSession = Depends(get_db)):
    # Check if slug exists
    stmt = select(Tenant).where(Tenant.slug == payload.slug)
    res = await db.execute(stmt)
    if res.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tenant slug '{payload.slug}' already exists."
        )

    # 1. Create Tenant
    tenant = Tenant(
        name=payload.name,
        slug=payload.slug,
        domain=payload.domain,
        plan_tier=payload.plan_tier,
        max_users=payload.max_users,
        max_students=payload.max_students,
        settings=payload.settings,
    )
    db.add(tenant)
    await db.flush()

    # Set context for initial admin creation
    TenantContext.set_tenant_id(tenant.id)

    # 2. Create Admin Person record
    admin_person = Person(
        tenant_id=tenant.id,
        first_name=payload.admin_first_name,
        last_name=payload.admin_last_name,
        email=payload.admin_email,
        primary_role="administrator"
    )
    db.add(admin_person)
    await db.flush()

    # 3. Create System Roles for Tenant
    admin_role = Role(
        tenant_id=tenant.id,
        name="Tenant Administrator",
        code="admin",
        description="Full access to tenant institution configuration",
        is_system_role=True
    )
    counselor_role = Role(
        tenant_id=tenant.id,
        name="Admissions Counselor",
        code="counselor",
        description="Access to leads, counseling, and applications",
        is_system_role=True
    )
    db.add_all([admin_role, counselor_role])
    await db.flush()

    # 4. Create Tenant Admin User
    admin_user = User(
        tenant_id=tenant.id,
        email=payload.admin_email,
        username=payload.admin_email,
        hashed_password=get_password_hash(payload.admin_password),
        first_name=payload.admin_first_name,
        last_name=payload.admin_last_name,
        is_active=True,
        person_id=admin_person.id
    )
    db.add(admin_user)
    await db.flush()

    # 5. Link User to Admin Role
    user_role = UserRole(
        tenant_id=tenant.id,
        user_id=admin_user.id,
        role_id=admin_role.id
    )
    db.add(user_role)
    await db.commit()

    return tenant


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == payload.email)
    res = await db.execute(stmt)
    user = res.scalars().first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Fetch user roles
    role_stmt = (
        select(Role.code)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user.id)
    )
    role_res = await db.execute(role_stmt)
    roles = list(role_res.scalars().all())

    access_token = create_access_token(
        data={
            "sub": user.id,
            "tenant_id": user.tenant_id,
            "email": user.email,
            "roles": roles,
            "is_super_admin": user.is_super_admin,
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=60,
        user_id=user.id,
        tenant_id=user.tenant_id,
        roles=roles,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
