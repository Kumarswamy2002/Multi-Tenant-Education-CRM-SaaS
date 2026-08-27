from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer
from app.models.base import TenantBaseModel


class WorkflowDefinition(TenantBaseModel):
    __tablename__ = "workflow_definitions"

    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    trigger_event = Column(String(100), index=True, nullable=False)  # ApplicationSubmitted, DocumentUploaded, LeadCreated, CaseCreated
    conditions_tree = Column(JSON, default=dict, nullable=False)  # Nested AND/OR conditions
    action_steps = Column(JSON, default=list, nullable=False)  # Sequential list of actions (create_task, send_email, assign_counselor, update_status)
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)


class WorkflowExecution(TenantBaseModel):
    __tablename__ = "workflow_executions"

    workflow_id = Column(String(36), index=True, nullable=False)
    trigger_event_id = Column(String(36), nullable=True)
    entity_id = Column(String(36), index=True, nullable=False)
    status = Column(String(50), default="RUNNING", index=True, nullable=False)  # RUNNING, COMPLETED, FAILED, WAITING
    current_step_index = Column(Integer, default=0, nullable=False)
    execution_context = Column(JSON, default=dict, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String(2000), nullable=True)


class WorkflowStepExecution(TenantBaseModel):
    __tablename__ = "workflow_step_executions"

    execution_id = Column(String(36), index=True, nullable=False)
    step_number = Column(Integer, nullable=False)
    action_type = Column(String(100), nullable=False)
    status = Column(String(50), default="SUCCESS", nullable=False)  # SUCCESS, FAILED, SKIPPED
    input_payload = Column(JSON, default=dict, nullable=False)
    output_payload = Column(JSON, default=dict, nullable=False)
    executed_at = Column(DateTime(timezone=True), nullable=False)
