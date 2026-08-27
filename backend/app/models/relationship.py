from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from app.models.base import TenantBaseModel


class Relationship(TenantBaseModel):
    __tablename__ = "relationships"

    source_id = Column(String(36), index=True, nullable=False)  # Person ID or Organization ID
    source_type = Column(String(50), nullable=False)  # person, organization, program
    relationship_type = Column(String(50), index=True, nullable=False)  # HAS_PARENT, ADVISED_BY, TAUGHT_BY, ENROLLED_IN, MEMBER_OF, APPLIED_TO, MENTORED_BY
    target_id = Column(String(36), index=True, nullable=False)  # Person ID or Organization ID
    target_type = Column(String(50), nullable=False)  # person, organization, program
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="active", nullable=False)
    attributes = Column(JSON, default=dict, nullable=False)
