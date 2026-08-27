from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.person import Person
from app.models.crm import Lead, Case
from app.models.admissions import Application
from app.models.organization import Program
from app.context import TenantContext


class GlobalSearchService:
    """
    Unified Search Engine abstraction across Students, Parents, Leads, Applications, Cases, and Programs.
    Enforces tenant context boundaries on all search queries.
    """

    @classmethod
    async def global_search(cls, db: AsyncSession, query_str: str) -> Dict[str, Any]:
        tenant_id = TenantContext.require_tenant_id()
        pattern = f"%{query_str}%"

        # 1. Search People (Students, Prospects, Parents, Alumni)
        people_stmt = select(Person).where(
            Person.tenant_id == tenant_id,
            or_(
                Person.first_name.ilike(pattern),
                Person.last_name.ilike(pattern),
                Person.email.ilike(pattern)
            )
        ).limit(10)
        people_res = await db.execute(people_stmt)
        people = people_res.scalars().all()

        # 2. Search Applications
        app_stmt = select(Application).where(
            Application.tenant_id == tenant_id,
            Application.application_number.ilike(pattern)
        ).limit(10)
        app_res = await db.execute(app_stmt)
        applications = app_res.scalars().all()

        # 3. Search Cases
        case_stmt = select(Case).where(
            Case.tenant_id == tenant_id,
            or_(
                Case.ticket_number.ilike(pattern),
                Case.title.ilike(pattern)
            )
        ).limit(10)
        case_res = await db.execute(case_stmt)
        cases = case_res.scalars().all()

        # 4. Search Academic Programs
        prog_stmt = select(Program).where(
            Program.tenant_id == tenant_id,
            or_(
                Program.name.ilike(pattern),
                Program.code.ilike(pattern)
            )
        ).limit(10)
        prog_res = await db.execute(prog_stmt)
        programs = prog_res.scalars().all()

        return {
            "tenant_id": tenant_id,
            "query": query_str,
            "results": {
                "people": people,
                "applications": applications,
                "cases": cases,
                "programs": programs
            }
        }
