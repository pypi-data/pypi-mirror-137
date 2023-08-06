"""
Type annotations for ssm service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm.client import SSMClient
    from types_aiobotocore_ssm.paginator import (
        DescribeActivationsPaginator,
        DescribeAssociationExecutionTargetsPaginator,
        DescribeAssociationExecutionsPaginator,
        DescribeAutomationExecutionsPaginator,
        DescribeAutomationStepExecutionsPaginator,
        DescribeAvailablePatchesPaginator,
        DescribeEffectiveInstanceAssociationsPaginator,
        DescribeEffectivePatchesForPatchBaselinePaginator,
        DescribeInstanceAssociationsStatusPaginator,
        DescribeInstanceInformationPaginator,
        DescribeInstancePatchStatesPaginator,
        DescribeInstancePatchStatesForPatchGroupPaginator,
        DescribeInstancePatchesPaginator,
        DescribeInventoryDeletionsPaginator,
        DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
        DescribeMaintenanceWindowExecutionTasksPaginator,
        DescribeMaintenanceWindowExecutionsPaginator,
        DescribeMaintenanceWindowSchedulePaginator,
        DescribeMaintenanceWindowTargetsPaginator,
        DescribeMaintenanceWindowTasksPaginator,
        DescribeMaintenanceWindowsPaginator,
        DescribeMaintenanceWindowsForTargetPaginator,
        DescribeOpsItemsPaginator,
        DescribeParametersPaginator,
        DescribePatchBaselinesPaginator,
        DescribePatchGroupsPaginator,
        DescribePatchPropertiesPaginator,
        DescribeSessionsPaginator,
        GetInventoryPaginator,
        GetInventorySchemaPaginator,
        GetOpsSummaryPaginator,
        GetParameterHistoryPaginator,
        GetParametersByPathPaginator,
        ListAssociationVersionsPaginator,
        ListAssociationsPaginator,
        ListCommandInvocationsPaginator,
        ListCommandsPaginator,
        ListComplianceItemsPaginator,
        ListComplianceSummariesPaginator,
        ListDocumentVersionsPaginator,
        ListDocumentsPaginator,
        ListOpsItemEventsPaginator,
        ListOpsItemRelatedItemsPaginator,
        ListOpsMetadataPaginator,
        ListResourceComplianceSummariesPaginator,
        ListResourceDataSyncPaginator,
    )

    session = get_session()
    with session.create_client("ssm") as client:
        client: SSMClient

        describe_activations_paginator: DescribeActivationsPaginator = client.get_paginator("describe_activations")
        describe_association_execution_targets_paginator: DescribeAssociationExecutionTargetsPaginator = client.get_paginator("describe_association_execution_targets")
        describe_association_executions_paginator: DescribeAssociationExecutionsPaginator = client.get_paginator("describe_association_executions")
        describe_automation_executions_paginator: DescribeAutomationExecutionsPaginator = client.get_paginator("describe_automation_executions")
        describe_automation_step_executions_paginator: DescribeAutomationStepExecutionsPaginator = client.get_paginator("describe_automation_step_executions")
        describe_available_patches_paginator: DescribeAvailablePatchesPaginator = client.get_paginator("describe_available_patches")
        describe_effective_instance_associations_paginator: DescribeEffectiveInstanceAssociationsPaginator = client.get_paginator("describe_effective_instance_associations")
        describe_effective_patches_for_patch_baseline_paginator: DescribeEffectivePatchesForPatchBaselinePaginator = client.get_paginator("describe_effective_patches_for_patch_baseline")
        describe_instance_associations_status_paginator: DescribeInstanceAssociationsStatusPaginator = client.get_paginator("describe_instance_associations_status")
        describe_instance_information_paginator: DescribeInstanceInformationPaginator = client.get_paginator("describe_instance_information")
        describe_instance_patch_states_paginator: DescribeInstancePatchStatesPaginator = client.get_paginator("describe_instance_patch_states")
        describe_instance_patch_states_for_patch_group_paginator: DescribeInstancePatchStatesForPatchGroupPaginator = client.get_paginator("describe_instance_patch_states_for_patch_group")
        describe_instance_patches_paginator: DescribeInstancePatchesPaginator = client.get_paginator("describe_instance_patches")
        describe_inventory_deletions_paginator: DescribeInventoryDeletionsPaginator = client.get_paginator("describe_inventory_deletions")
        describe_maintenance_window_execution_task_invocations_paginator: DescribeMaintenanceWindowExecutionTaskInvocationsPaginator = client.get_paginator("describe_maintenance_window_execution_task_invocations")
        describe_maintenance_window_execution_tasks_paginator: DescribeMaintenanceWindowExecutionTasksPaginator = client.get_paginator("describe_maintenance_window_execution_tasks")
        describe_maintenance_window_executions_paginator: DescribeMaintenanceWindowExecutionsPaginator = client.get_paginator("describe_maintenance_window_executions")
        describe_maintenance_window_schedule_paginator: DescribeMaintenanceWindowSchedulePaginator = client.get_paginator("describe_maintenance_window_schedule")
        describe_maintenance_window_targets_paginator: DescribeMaintenanceWindowTargetsPaginator = client.get_paginator("describe_maintenance_window_targets")
        describe_maintenance_window_tasks_paginator: DescribeMaintenanceWindowTasksPaginator = client.get_paginator("describe_maintenance_window_tasks")
        describe_maintenance_windows_paginator: DescribeMaintenanceWindowsPaginator = client.get_paginator("describe_maintenance_windows")
        describe_maintenance_windows_for_target_paginator: DescribeMaintenanceWindowsForTargetPaginator = client.get_paginator("describe_maintenance_windows_for_target")
        describe_ops_items_paginator: DescribeOpsItemsPaginator = client.get_paginator("describe_ops_items")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_patch_baselines_paginator: DescribePatchBaselinesPaginator = client.get_paginator("describe_patch_baselines")
        describe_patch_groups_paginator: DescribePatchGroupsPaginator = client.get_paginator("describe_patch_groups")
        describe_patch_properties_paginator: DescribePatchPropertiesPaginator = client.get_paginator("describe_patch_properties")
        describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
        get_inventory_paginator: GetInventoryPaginator = client.get_paginator("get_inventory")
        get_inventory_schema_paginator: GetInventorySchemaPaginator = client.get_paginator("get_inventory_schema")
        get_ops_summary_paginator: GetOpsSummaryPaginator = client.get_paginator("get_ops_summary")
        get_parameter_history_paginator: GetParameterHistoryPaginator = client.get_paginator("get_parameter_history")
        get_parameters_by_path_paginator: GetParametersByPathPaginator = client.get_paginator("get_parameters_by_path")
        list_association_versions_paginator: ListAssociationVersionsPaginator = client.get_paginator("list_association_versions")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_command_invocations_paginator: ListCommandInvocationsPaginator = client.get_paginator("list_command_invocations")
        list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
        list_compliance_items_paginator: ListComplianceItemsPaginator = client.get_paginator("list_compliance_items")
        list_compliance_summaries_paginator: ListComplianceSummariesPaginator = client.get_paginator("list_compliance_summaries")
        list_document_versions_paginator: ListDocumentVersionsPaginator = client.get_paginator("list_document_versions")
        list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
        list_ops_item_events_paginator: ListOpsItemEventsPaginator = client.get_paginator("list_ops_item_events")
        list_ops_item_related_items_paginator: ListOpsItemRelatedItemsPaginator = client.get_paginator("list_ops_item_related_items")
        list_ops_metadata_paginator: ListOpsMetadataPaginator = client.get_paginator("list_ops_metadata")
        list_resource_compliance_summaries_paginator: ListResourceComplianceSummariesPaginator = client.get_paginator("list_resource_compliance_summaries")
        list_resource_data_sync_paginator: ListResourceDataSyncPaginator = client.get_paginator("list_resource_data_sync")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    MaintenanceWindowResourceTypeType,
    OperatingSystemType,
    PatchPropertyType,
    PatchSetType,
    SessionStateType,
)
from .type_defs import (
    AssociationExecutionFilterTypeDef,
    AssociationExecutionTargetsFilterTypeDef,
    AssociationFilterTypeDef,
    AutomationExecutionFilterTypeDef,
    CommandFilterTypeDef,
    ComplianceStringFilterTypeDef,
    DescribeActivationsFilterTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsResponseTypeDef,
    DocumentFilterTypeDef,
    DocumentKeyValuesFilterTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaResultTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParametersByPathResultTypeDef,
    InstanceInformationFilterTypeDef,
    InstanceInformationStringFilterTypeDef,
    InstancePatchStateFilterTypeDef,
    InventoryAggregatorTypeDef,
    InventoryFilterTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncResultTypeDef,
    MaintenanceWindowFilterTypeDef,
    OpsAggregatorTypeDef,
    OpsFilterTypeDef,
    OpsItemEventFilterTypeDef,
    OpsItemFilterTypeDef,
    OpsItemRelatedItemsFilterTypeDef,
    OpsMetadataFilterTypeDef,
    OpsResultAttributeTypeDef,
    PaginatorConfigTypeDef,
    ParametersFilterTypeDef,
    ParameterStringFilterTypeDef,
    PatchOrchestratorFilterTypeDef,
    ResultAttributeTypeDef,
    SessionFilterTypeDef,
    StepExecutionFilterTypeDef,
    TargetTypeDef,
)

__all__ = (
    "DescribeActivationsPaginator",
    "DescribeAssociationExecutionTargetsPaginator",
    "DescribeAssociationExecutionsPaginator",
    "DescribeAutomationExecutionsPaginator",
    "DescribeAutomationStepExecutionsPaginator",
    "DescribeAvailablePatchesPaginator",
    "DescribeEffectiveInstanceAssociationsPaginator",
    "DescribeEffectivePatchesForPatchBaselinePaginator",
    "DescribeInstanceAssociationsStatusPaginator",
    "DescribeInstanceInformationPaginator",
    "DescribeInstancePatchStatesPaginator",
    "DescribeInstancePatchStatesForPatchGroupPaginator",
    "DescribeInstancePatchesPaginator",
    "DescribeInventoryDeletionsPaginator",
    "DescribeMaintenanceWindowExecutionTaskInvocationsPaginator",
    "DescribeMaintenanceWindowExecutionTasksPaginator",
    "DescribeMaintenanceWindowExecutionsPaginator",
    "DescribeMaintenanceWindowSchedulePaginator",
    "DescribeMaintenanceWindowTargetsPaginator",
    "DescribeMaintenanceWindowTasksPaginator",
    "DescribeMaintenanceWindowsPaginator",
    "DescribeMaintenanceWindowsForTargetPaginator",
    "DescribeOpsItemsPaginator",
    "DescribeParametersPaginator",
    "DescribePatchBaselinesPaginator",
    "DescribePatchGroupsPaginator",
    "DescribePatchPropertiesPaginator",
    "DescribeSessionsPaginator",
    "GetInventoryPaginator",
    "GetInventorySchemaPaginator",
    "GetOpsSummaryPaginator",
    "GetParameterHistoryPaginator",
    "GetParametersByPathPaginator",
    "ListAssociationVersionsPaginator",
    "ListAssociationsPaginator",
    "ListCommandInvocationsPaginator",
    "ListCommandsPaginator",
    "ListComplianceItemsPaginator",
    "ListComplianceSummariesPaginator",
    "ListDocumentVersionsPaginator",
    "ListDocumentsPaginator",
    "ListOpsItemEventsPaginator",
    "ListOpsItemRelatedItemsPaginator",
    "ListOpsMetadataPaginator",
    "ListResourceComplianceSummariesPaginator",
    "ListResourceDataSyncPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeActivationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeActivations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeactivationspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["DescribeActivationsFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeActivationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeActivations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeactivationspaginator)
        """


class DescribeAssociationExecutionTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutionTargets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeassociationexecutiontargetspaginator)
    """

    async def paginate(
        self,
        *,
        AssociationId: str,
        ExecutionId: str,
        Filters: Sequence["AssociationExecutionTargetsFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAssociationExecutionTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutionTargets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeassociationexecutiontargetspaginator)
        """


class DescribeAssociationExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeassociationexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        AssociationId: str,
        Filters: Sequence["AssociationExecutionFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAssociationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeassociationexecutionspaginator)
        """


class DescribeAutomationExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeautomationexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["AutomationExecutionFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAutomationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeautomationexecutionspaginator)
        """


class DescribeAutomationStepExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationStepExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeautomationstepexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        AutomationExecutionId: str,
        Filters: Sequence["StepExecutionFilterTypeDef"] = ...,
        ReverseOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAutomationStepExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationStepExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeautomationstepexecutionspaginator)
        """


class DescribeAvailablePatchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAvailablePatches)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeavailablepatchespaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["PatchOrchestratorFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAvailablePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAvailablePatches.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeavailablepatchespaginator)
        """


class DescribeEffectiveInstanceAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectiveInstanceAssociations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeeffectiveinstanceassociationspaginator)
    """

    async def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEffectiveInstanceAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectiveInstanceAssociations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeeffectiveinstanceassociationspaginator)
        """


class DescribeEffectivePatchesForPatchBaselinePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeeffectivepatchesforpatchbaselinepaginator)
    """

    async def paginate(
        self, *, BaselineId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEffectivePatchesForPatchBaselineResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeeffectivepatchesforpatchbaselinepaginator)
        """


class DescribeInstanceAssociationsStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceAssociationsStatus)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstanceassociationsstatuspaginator)
    """

    async def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstanceAssociationsStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceAssociationsStatus.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstanceassociationsstatuspaginator)
        """


class DescribeInstanceInformationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceInformation)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstanceinformationpaginator)
    """

    async def paginate(
        self,
        *,
        InstanceInformationFilterList: Sequence["InstanceInformationFilterTypeDef"] = ...,
        Filters: Sequence["InstanceInformationStringFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstanceInformationResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceInformation.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstanceinformationpaginator)
        """


class DescribeInstancePatchStatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstancepatchstatespaginator)
    """

    async def paginate(
        self, *, InstanceIds: Sequence[str], PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancePatchStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstancepatchstatespaginator)
        """


class DescribeInstancePatchStatesForPatchGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstancepatchstatesforpatchgrouppaginator)
    """

    async def paginate(
        self,
        *,
        PatchGroup: str,
        Filters: Sequence["InstancePatchStateFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancePatchStatesForPatchGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstancepatchstatesforpatchgrouppaginator)
        """


class DescribeInstancePatchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatches)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstancepatchespaginator)
    """

    async def paginate(
        self,
        *,
        InstanceId: str,
        Filters: Sequence["PatchOrchestratorFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatches.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinstancepatchespaginator)
        """


class DescribeInventoryDeletionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInventoryDeletions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinventorydeletionspaginator)
    """

    async def paginate(
        self, *, DeletionId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInventoryDeletionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInventoryDeletions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeinventorydeletionspaginator)
        """


class DescribeMaintenanceWindowExecutionTaskInvocationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowexecutiontaskinvocationspaginator)
    """

    async def paginate(
        self,
        *,
        WindowExecutionId: str,
        TaskId: str,
        Filters: Sequence["MaintenanceWindowFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowexecutiontaskinvocationspaginator)
        """


class DescribeMaintenanceWindowExecutionTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowexecutiontaskspaginator)
    """

    async def paginate(
        self,
        *,
        WindowExecutionId: str,
        Filters: Sequence["MaintenanceWindowFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowexecutiontaskspaginator)
        """


class DescribeMaintenanceWindowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        WindowId: str,
        Filters: Sequence["MaintenanceWindowFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowexecutionspaginator)
        """


class DescribeMaintenanceWindowSchedulePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowSchedule)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowschedulepaginator)
    """

    async def paginate(
        self,
        *,
        WindowId: str = ...,
        Targets: Sequence["TargetTypeDef"] = ...,
        ResourceType: MaintenanceWindowResourceTypeType = ...,
        Filters: Sequence["PatchOrchestratorFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowScheduleResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowSchedule.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowschedulepaginator)
        """


class DescribeMaintenanceWindowTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTargets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowtargetspaginator)
    """

    async def paginate(
        self,
        *,
        WindowId: str,
        Filters: Sequence["MaintenanceWindowFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTargets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowtargetspaginator)
        """


class DescribeMaintenanceWindowTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowtaskspaginator)
    """

    async def paginate(
        self,
        *,
        WindowId: str,
        Filters: Sequence["MaintenanceWindowFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowtaskspaginator)
        """


class DescribeMaintenanceWindowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindows)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["MaintenanceWindowFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindows.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowspaginator)
        """


class DescribeMaintenanceWindowsForTargetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowsfortargetpaginator)
    """

    async def paginate(
        self,
        *,
        Targets: Sequence["TargetTypeDef"],
        ResourceType: MaintenanceWindowResourceTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowsForTargetResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describemaintenancewindowsfortargetpaginator)
        """


class DescribeOpsItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeOpsItems)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeopsitemspaginator)
    """

    async def paginate(
        self,
        *,
        OpsItemFilters: Sequence["OpsItemFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOpsItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeOpsItems.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeopsitemspaginator)
        """


class DescribeParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeParameters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeparameterspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["ParametersFilterTypeDef"] = ...,
        ParameterFilters: Sequence["ParameterStringFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describeparameterspaginator)
        """


class DescribePatchBaselinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchBaselines)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describepatchbaselinespaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["PatchOrchestratorFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePatchBaselinesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchBaselines.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describepatchbaselinespaginator)
        """


class DescribePatchGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describepatchgroupspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["PatchOrchestratorFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePatchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describepatchgroupspaginator)
        """


class DescribePatchPropertiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchProperties)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describepatchpropertiespaginator)
    """

    async def paginate(
        self,
        *,
        OperatingSystem: OperatingSystemType,
        Property: PatchPropertyType,
        PatchSet: PatchSetType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePatchPropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchProperties.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describepatchpropertiespaginator)
        """


class DescribeSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeSessions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describesessionspaginator)
    """

    async def paginate(
        self,
        *,
        State: SessionStateType,
        Filters: Sequence["SessionFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeSessions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#describesessionspaginator)
        """


class GetInventoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventory)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getinventorypaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["InventoryFilterTypeDef"] = ...,
        Aggregators: Sequence["InventoryAggregatorTypeDef"] = ...,
        ResultAttributes: Sequence["ResultAttributeTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetInventoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventory.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getinventorypaginator)
        """


class GetInventorySchemaPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventorySchema)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getinventoryschemapaginator)
    """

    async def paginate(
        self,
        *,
        TypeName: str = ...,
        Aggregator: bool = ...,
        SubType: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetInventorySchemaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventorySchema.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getinventoryschemapaginator)
        """


class GetOpsSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetOpsSummary)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getopssummarypaginator)
    """

    async def paginate(
        self,
        *,
        SyncName: str = ...,
        Filters: Sequence["OpsFilterTypeDef"] = ...,
        Aggregators: Sequence["OpsAggregatorTypeDef"] = ...,
        ResultAttributes: Sequence["OpsResultAttributeTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetOpsSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetOpsSummary.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getopssummarypaginator)
        """


class GetParameterHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParameterHistory)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getparameterhistorypaginator)
    """

    async def paginate(
        self,
        *,
        Name: str,
        WithDecryption: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetParameterHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParameterHistory.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getparameterhistorypaginator)
        """


class GetParametersByPathPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParametersByPath)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getparametersbypathpaginator)
    """

    async def paginate(
        self,
        *,
        Path: str,
        Recursive: bool = ...,
        ParameterFilters: Sequence["ParameterStringFilterTypeDef"] = ...,
        WithDecryption: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetParametersByPathResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParametersByPath.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#getparametersbypathpaginator)
        """


class ListAssociationVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociationVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listassociationversionspaginator)
    """

    async def paginate(
        self, *, AssociationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociationVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listassociationversionspaginator)
        """


class ListAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listassociationspaginator)
    """

    async def paginate(
        self,
        *,
        AssociationFilterList: Sequence["AssociationFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listassociationspaginator)
        """


class ListCommandInvocationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommandInvocations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcommandinvocationspaginator)
    """

    async def paginate(
        self,
        *,
        CommandId: str = ...,
        InstanceId: str = ...,
        Filters: Sequence["CommandFilterTypeDef"] = ...,
        Details: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCommandInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommandInvocations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcommandinvocationspaginator)
        """


class ListCommandsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommands)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcommandspaginator)
    """

    async def paginate(
        self,
        *,
        CommandId: str = ...,
        InstanceId: str = ...,
        Filters: Sequence["CommandFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCommandsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommands.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcommandspaginator)
        """


class ListComplianceItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceItems)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcomplianceitemspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["ComplianceStringFilterTypeDef"] = ...,
        ResourceIds: Sequence[str] = ...,
        ResourceTypes: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComplianceItemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceItems.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcomplianceitemspaginator)
        """


class ListComplianceSummariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceSummaries)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcompliancesummariespaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["ComplianceStringFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceSummaries.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listcompliancesummariespaginator)
        """


class ListDocumentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocumentVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listdocumentversionspaginator)
    """

    async def paginate(
        self, *, Name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDocumentVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocumentVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listdocumentversionspaginator)
        """


class ListDocumentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocuments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listdocumentspaginator)
    """

    async def paginate(
        self,
        *,
        DocumentFilterList: Sequence["DocumentFilterTypeDef"] = ...,
        Filters: Sequence["DocumentKeyValuesFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDocumentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocuments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listdocumentspaginator)
        """


class ListOpsItemEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listopsitemeventspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["OpsItemEventFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOpsItemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listopsitemeventspaginator)
        """


class ListOpsItemRelatedItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemRelatedItems)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listopsitemrelateditemspaginator)
    """

    async def paginate(
        self,
        *,
        OpsItemId: str = ...,
        Filters: Sequence["OpsItemRelatedItemsFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOpsItemRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemRelatedItems.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listopsitemrelateditemspaginator)
        """


class ListOpsMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsMetadata)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listopsmetadatapaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["OpsMetadataFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOpsMetadataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsMetadata.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listopsmetadatapaginator)
        """


class ListResourceComplianceSummariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceComplianceSummaries)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listresourcecompliancesummariespaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["ComplianceStringFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceComplianceSummaries.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listresourcecompliancesummariespaginator)
        """


class ListResourceDataSyncPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceDataSync)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listresourcedatasyncpaginator)
    """

    async def paginate(
        self, *, SyncType: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceDataSyncResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceDataSync.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators.html#listresourcedatasyncpaginator)
        """
