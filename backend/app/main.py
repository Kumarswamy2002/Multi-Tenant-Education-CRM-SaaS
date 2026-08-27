import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.middleware import TenantSecurityMiddleware
from app.api.v1 import (
    auth, organizations, people, leads, admissions, cases,
    workflows, career, analytics, ai, search, custom_objects, integrations,
    academics, admissions_pipeline, billing_finance, career_placement,
    campus_facilities, ai_insights, workflow_automation,
    portal_student_api, portal_parent_api, portal_counselor_api,
    portal_employer_api, portal_alumni_api, reports_analytics, security_audit
)

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CampusSphere Enterprise Multi-Tenant Education CRM SaaS",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 1. Tenant Security & Execution Context Middleware
app.add_middleware(TenantSecurityMiddleware)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include Core API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(organizations.router, prefix=settings.API_V1_STR)
app.include_router(people.router, prefix=settings.API_V1_STR)
app.include_router(leads.router, prefix=settings.API_V1_STR)
app.include_router(admissions.router, prefix=settings.API_V1_STR)
app.include_router(cases.router, prefix=settings.API_V1_STR)
app.include_router(workflows.router, prefix=settings.API_V1_STR)
app.include_router(career.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(custom_objects.router, prefix=settings.API_V1_STR)
app.include_router(integrations.router, prefix=settings.API_V1_STR)

# 4. Include Enterprise Extended Routers
app.include_router(academics.router, prefix=settings.API_V1_STR)
app.include_router(admissions_pipeline.router, prefix=settings.API_V1_STR)
app.include_router(billing_finance.router, prefix=settings.API_V1_STR)
app.include_router(career_placement.router, prefix=settings.API_V1_STR)
app.include_router(campus_facilities.router, prefix=settings.API_V1_STR)
app.include_router(ai_insights.router, prefix=settings.API_V1_STR)
app.include_router(workflow_automation.router, prefix=settings.API_V1_STR)
app.include_router(portal_student_api.router, prefix=settings.API_V1_STR)
app.include_router(portal_parent_api.router, prefix=settings.API_V1_STR)
app.include_router(portal_counselor_api.router, prefix=settings.API_V1_STR)
app.include_router(portal_employer_api.router, prefix=settings.API_V1_STR)
app.include_router(portal_alumni_api.router, prefix=settings.API_V1_STR)
app.include_router(reports_analytics.router, prefix=settings.API_V1_STR)
app.include_router(security_audit.router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def on_startup():
    logger.info("Initializing database schemas...")
    await init_db()
    logger.info("Database schemas ready!")


@app.get("/")
async def root():
    return {
        "title": "CampusSphere Enterprise Multi-Tenant Education CRM SaaS",
        "version": settings.VERSION,
        "status": "healthy",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "tenant_context": "active"
    }
