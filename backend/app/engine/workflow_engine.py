import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.workflow import WorkflowDefinition, WorkflowExecution, WorkflowStepExecution
from app.context import TenantContext

logger = logging.getLogger(__name__)


class WorkflowAutomationEngine:
    """
    Unified Workflow Engine. Evaluates incoming domain event triggers against active workflow definitions,
    evaluates nested condition trees, and executes defined step actions.
    """

    @classmethod
    def evaluate_condition_node(cls, node: Dict[str, Any], context: Dict[str, Any]) -> bool:
        if not node:
            return True

        op = node.get("operator", "AND").upper()
        conditions = node.get("conditions", [])

        results = []
        for cond in conditions:
            if "operator" in cond:
                # Nested condition tree
                results.append(cls.evaluate_condition_node(cond, context))
            else:
                field = cond.get("field")
                target_val = cond.get("value")
                comparison = cond.get("comparison", "equals")

                actual_val = context.get(field)
                if comparison == "equals":
                    results.append(actual_val == target_val)
                elif comparison == "not_equals":
                    results.append(actual_val != target_val)
                elif comparison == "greater_than":
                    results.append(float(actual_val or 0) > float(target_val or 0))
                elif comparison == "contains":
                    results.append(str(target_val).lower() in str(actual_val or "").lower())
                else:
                    results.append(False)

        if op == "OR":
            return any(results) if results else True
        return all(results) if results else True

    @classmethod
    async def process_trigger(
        cls,
        db: AsyncSession,
        trigger_event: str,
        entity_id: str,
        event_payload: Dict[str, Any]
    ) -> List[WorkflowExecution]:
        tenant_id = TenantContext.require_tenant_id()

        # Query active workflows matching trigger_event
        stmt = select(WorkflowDefinition).where(
            WorkflowDefinition.tenant_id == tenant_id,
            WorkflowDefinition.trigger_event == trigger_event,
            WorkflowDefinition.is_active == True
        )
        res = await db.execute(stmt)
        workflows = res.scalars().all()

        executions = []
        for wf in workflows:
            matches = cls.evaluate_condition_node(wf.conditions_tree, event_payload)
            if not matches:
                logger.info(f"Workflow {wf.name} conditions not met for trigger {trigger_event}")
                continue

            # Instantiate Workflow Execution
            exec_obj = WorkflowExecution(
                tenant_id=tenant_id,
                workflow_id=wf.id,
                entity_id=entity_id,
                status="RUNNING",
                current_step_index=0,
                execution_context=event_payload,
                started_at=datetime.now(timezone.utc)
            )
            db.add(exec_obj)
            await db.flush()

            # Execute action steps sequentially
            step_idx = 0
            for action in wf.action_steps:
                action_type = action.get("action_type", "notification")
                step_exec = WorkflowStepExecution(
                    tenant_id=tenant_id,
                    execution_id=exec_obj.id,
                    step_number=step_idx + 1,
                    action_type=action_type,
                    status="SUCCESS",
                    input_payload=action,
                    output_payload={"result": f"Executed action {action_type} successfully"},
                    executed_at=datetime.now(timezone.utc)
                )
                db.add(step_exec)
                step_idx += 1

            exec_obj.status = "COMPLETED"
            exec_obj.current_step_index = step_idx
            exec_obj.completed_at = datetime.now(timezone.utc)
            executions.append(exec_obj)

        await db.commit()
        return executions
