from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.relationship import Relationship
from app.context import TenantContext


class RelationshipEngine:
    """
    Central Relationship Graph Service supporting edge insertion, querying, and verification
    for all relationships: HAS_PARENT, ADVISED_BY, TAUGHT_BY, ENROLLED_IN, MEMBER_OF, APPLIED_TO, MENTORED_BY.
    """

    @staticmethod
    async def create_edge(
        db: AsyncSession,
        source_id: str,
        source_type: str,
        relationship_type: str,
        target_id: str,
        target_type: str,
        attributes: Dict[str, Any] = None
    ) -> Relationship:
        tenant_id = TenantContext.require_tenant_id()
        rel = Relationship(
            tenant_id=tenant_id,
            source_id=source_id,
            source_type=source_type,
            relationship_type=relationship_type,
            target_id=target_id,
            target_type=target_type,
            attributes=attributes or {},
            status="active"
        )
        db.add(rel)
        await db.flush()
        return rel

    @staticmethod
    async def get_relationships_for_entity(
        db: AsyncSession,
        entity_id: str,
        relationship_type: Optional[str] = None
    ) -> List[Relationship]:
        tenant_id = TenantContext.require_tenant_id()
        stmt = select(Relationship).where(
            Relationship.tenant_id == tenant_id,
            (Relationship.source_id == entity_id) | (Relationship.target_id == entity_id)
        )
        if relationship_type:
            stmt = stmt.where(Relationship.relationship_type == relationship_type)
        res = await db.execute(stmt)
        return list(res.scalars().all())
