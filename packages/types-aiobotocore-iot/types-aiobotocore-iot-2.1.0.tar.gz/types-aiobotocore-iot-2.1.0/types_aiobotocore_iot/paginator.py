"""
Type annotations for iot service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot.client import IoTClient
    from types_aiobotocore_iot.paginator import (
        GetBehaviorModelTrainingSummariesPaginator,
        ListActiveViolationsPaginator,
        ListAttachedPoliciesPaginator,
        ListAuditFindingsPaginator,
        ListAuditMitigationActionsExecutionsPaginator,
        ListAuditMitigationActionsTasksPaginator,
        ListAuditSuppressionsPaginator,
        ListAuditTasksPaginator,
        ListAuthorizersPaginator,
        ListBillingGroupsPaginator,
        ListCACertificatesPaginator,
        ListCertificatesPaginator,
        ListCertificatesByCAPaginator,
        ListCustomMetricsPaginator,
        ListDetectMitigationActionsExecutionsPaginator,
        ListDetectMitigationActionsTasksPaginator,
        ListDimensionsPaginator,
        ListDomainConfigurationsPaginator,
        ListFleetMetricsPaginator,
        ListIndicesPaginator,
        ListJobExecutionsForJobPaginator,
        ListJobExecutionsForThingPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListMitigationActionsPaginator,
        ListOTAUpdatesPaginator,
        ListOutgoingCertificatesPaginator,
        ListPoliciesPaginator,
        ListPolicyPrincipalsPaginator,
        ListPrincipalPoliciesPaginator,
        ListPrincipalThingsPaginator,
        ListProvisioningTemplateVersionsPaginator,
        ListProvisioningTemplatesPaginator,
        ListRoleAliasesPaginator,
        ListScheduledAuditsPaginator,
        ListSecurityProfilesPaginator,
        ListSecurityProfilesForTargetPaginator,
        ListStreamsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
        ListTargetsForSecurityProfilePaginator,
        ListThingGroupsPaginator,
        ListThingGroupsForThingPaginator,
        ListThingPrincipalsPaginator,
        ListThingRegistrationTaskReportsPaginator,
        ListThingRegistrationTasksPaginator,
        ListThingTypesPaginator,
        ListThingsPaginator,
        ListThingsInBillingGroupPaginator,
        ListThingsInThingGroupPaginator,
        ListTopicRuleDestinationsPaginator,
        ListTopicRulesPaginator,
        ListV2LoggingLevelsPaginator,
        ListViolationEventsPaginator,
    )

    session = get_session()
    with session.create_client("iot") as client:
        client: IoTClient

        get_behavior_model_training_summaries_paginator: GetBehaviorModelTrainingSummariesPaginator = client.get_paginator("get_behavior_model_training_summaries")
        list_active_violations_paginator: ListActiveViolationsPaginator = client.get_paginator("list_active_violations")
        list_attached_policies_paginator: ListAttachedPoliciesPaginator = client.get_paginator("list_attached_policies")
        list_audit_findings_paginator: ListAuditFindingsPaginator = client.get_paginator("list_audit_findings")
        list_audit_mitigation_actions_executions_paginator: ListAuditMitigationActionsExecutionsPaginator = client.get_paginator("list_audit_mitigation_actions_executions")
        list_audit_mitigation_actions_tasks_paginator: ListAuditMitigationActionsTasksPaginator = client.get_paginator("list_audit_mitigation_actions_tasks")
        list_audit_suppressions_paginator: ListAuditSuppressionsPaginator = client.get_paginator("list_audit_suppressions")
        list_audit_tasks_paginator: ListAuditTasksPaginator = client.get_paginator("list_audit_tasks")
        list_authorizers_paginator: ListAuthorizersPaginator = client.get_paginator("list_authorizers")
        list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
        list_ca_certificates_paginator: ListCACertificatesPaginator = client.get_paginator("list_ca_certificates")
        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
        list_certificates_by_ca_paginator: ListCertificatesByCAPaginator = client.get_paginator("list_certificates_by_ca")
        list_custom_metrics_paginator: ListCustomMetricsPaginator = client.get_paginator("list_custom_metrics")
        list_detect_mitigation_actions_executions_paginator: ListDetectMitigationActionsExecutionsPaginator = client.get_paginator("list_detect_mitigation_actions_executions")
        list_detect_mitigation_actions_tasks_paginator: ListDetectMitigationActionsTasksPaginator = client.get_paginator("list_detect_mitigation_actions_tasks")
        list_dimensions_paginator: ListDimensionsPaginator = client.get_paginator("list_dimensions")
        list_domain_configurations_paginator: ListDomainConfigurationsPaginator = client.get_paginator("list_domain_configurations")
        list_fleet_metrics_paginator: ListFleetMetricsPaginator = client.get_paginator("list_fleet_metrics")
        list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
        list_job_executions_for_job_paginator: ListJobExecutionsForJobPaginator = client.get_paginator("list_job_executions_for_job")
        list_job_executions_for_thing_paginator: ListJobExecutionsForThingPaginator = client.get_paginator("list_job_executions_for_thing")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_mitigation_actions_paginator: ListMitigationActionsPaginator = client.get_paginator("list_mitigation_actions")
        list_ota_updates_paginator: ListOTAUpdatesPaginator = client.get_paginator("list_ota_updates")
        list_outgoing_certificates_paginator: ListOutgoingCertificatesPaginator = client.get_paginator("list_outgoing_certificates")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_principals_paginator: ListPolicyPrincipalsPaginator = client.get_paginator("list_policy_principals")
        list_principal_policies_paginator: ListPrincipalPoliciesPaginator = client.get_paginator("list_principal_policies")
        list_principal_things_paginator: ListPrincipalThingsPaginator = client.get_paginator("list_principal_things")
        list_provisioning_template_versions_paginator: ListProvisioningTemplateVersionsPaginator = client.get_paginator("list_provisioning_template_versions")
        list_provisioning_templates_paginator: ListProvisioningTemplatesPaginator = client.get_paginator("list_provisioning_templates")
        list_role_aliases_paginator: ListRoleAliasesPaginator = client.get_paginator("list_role_aliases")
        list_scheduled_audits_paginator: ListScheduledAuditsPaginator = client.get_paginator("list_scheduled_audits")
        list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
        list_security_profiles_for_target_paginator: ListSecurityProfilesForTargetPaginator = client.get_paginator("list_security_profiles_for_target")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
        list_targets_for_security_profile_paginator: ListTargetsForSecurityProfilePaginator = client.get_paginator("list_targets_for_security_profile")
        list_thing_groups_paginator: ListThingGroupsPaginator = client.get_paginator("list_thing_groups")
        list_thing_groups_for_thing_paginator: ListThingGroupsForThingPaginator = client.get_paginator("list_thing_groups_for_thing")
        list_thing_principals_paginator: ListThingPrincipalsPaginator = client.get_paginator("list_thing_principals")
        list_thing_registration_task_reports_paginator: ListThingRegistrationTaskReportsPaginator = client.get_paginator("list_thing_registration_task_reports")
        list_thing_registration_tasks_paginator: ListThingRegistrationTasksPaginator = client.get_paginator("list_thing_registration_tasks")
        list_thing_types_paginator: ListThingTypesPaginator = client.get_paginator("list_thing_types")
        list_things_paginator: ListThingsPaginator = client.get_paginator("list_things")
        list_things_in_billing_group_paginator: ListThingsInBillingGroupPaginator = client.get_paginator("list_things_in_billing_group")
        list_things_in_thing_group_paginator: ListThingsInThingGroupPaginator = client.get_paginator("list_things_in_thing_group")
        list_topic_rule_destinations_paginator: ListTopicRuleDestinationsPaginator = client.get_paginator("list_topic_rule_destinations")
        list_topic_rules_paginator: ListTopicRulesPaginator = client.get_paginator("list_topic_rules")
        list_v2_logging_levels_paginator: ListV2LoggingLevelsPaginator = client.get_paginator("list_v2_logging_levels")
        list_violation_events_paginator: ListViolationEventsPaginator = client.get_paginator("list_violation_events")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    AuditMitigationActionsExecutionStatusType,
    AuditMitigationActionsTaskStatusType,
    AuditTaskStatusType,
    AuditTaskTypeType,
    AuthorizerStatusType,
    BehaviorCriteriaTypeType,
    JobExecutionStatusType,
    JobStatusType,
    LogTargetTypeType,
    MitigationActionTypeType,
    OTAUpdateStatusType,
    ReportTypeType,
    ServiceTypeType,
    StatusType,
    TargetSelectionType,
    VerificationStateType,
)
from .type_defs import (
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsResponseTypeDef,
    PaginatorConfigTypeDef,
    ResourceIdentifierTypeDef,
)

__all__ = (
    "GetBehaviorModelTrainingSummariesPaginator",
    "ListActiveViolationsPaginator",
    "ListAttachedPoliciesPaginator",
    "ListAuditFindingsPaginator",
    "ListAuditMitigationActionsExecutionsPaginator",
    "ListAuditMitigationActionsTasksPaginator",
    "ListAuditSuppressionsPaginator",
    "ListAuditTasksPaginator",
    "ListAuthorizersPaginator",
    "ListBillingGroupsPaginator",
    "ListCACertificatesPaginator",
    "ListCertificatesPaginator",
    "ListCertificatesByCAPaginator",
    "ListCustomMetricsPaginator",
    "ListDetectMitigationActionsExecutionsPaginator",
    "ListDetectMitigationActionsTasksPaginator",
    "ListDimensionsPaginator",
    "ListDomainConfigurationsPaginator",
    "ListFleetMetricsPaginator",
    "ListIndicesPaginator",
    "ListJobExecutionsForJobPaginator",
    "ListJobExecutionsForThingPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListMitigationActionsPaginator",
    "ListOTAUpdatesPaginator",
    "ListOutgoingCertificatesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyPrincipalsPaginator",
    "ListPrincipalPoliciesPaginator",
    "ListPrincipalThingsPaginator",
    "ListProvisioningTemplateVersionsPaginator",
    "ListProvisioningTemplatesPaginator",
    "ListRoleAliasesPaginator",
    "ListScheduledAuditsPaginator",
    "ListSecurityProfilesPaginator",
    "ListSecurityProfilesForTargetPaginator",
    "ListStreamsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
    "ListTargetsForSecurityProfilePaginator",
    "ListThingGroupsPaginator",
    "ListThingGroupsForThingPaginator",
    "ListThingPrincipalsPaginator",
    "ListThingRegistrationTaskReportsPaginator",
    "ListThingRegistrationTasksPaginator",
    "ListThingTypesPaginator",
    "ListThingsPaginator",
    "ListThingsInBillingGroupPaginator",
    "ListThingsInThingGroupPaginator",
    "ListTopicRuleDestinationsPaginator",
    "ListTopicRulesPaginator",
    "ListV2LoggingLevelsPaginator",
    "ListViolationEventsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetBehaviorModelTrainingSummariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.GetBehaviorModelTrainingSummaries)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#getbehaviormodeltrainingsummariespaginator)
    """

    async def paginate(
        self, *, securityProfileName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBehaviorModelTrainingSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.GetBehaviorModelTrainingSummaries.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#getbehaviormodeltrainingsummariespaginator)
        """


class ListActiveViolationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListActiveViolations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listactiveviolationspaginator)
    """

    async def paginate(
        self,
        *,
        thingName: str = ...,
        securityProfileName: str = ...,
        behaviorCriteriaType: BehaviorCriteriaTypeType = ...,
        listSuppressedAlerts: bool = ...,
        verificationState: VerificationStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActiveViolationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListActiveViolations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listactiveviolationspaginator)
        """


class ListAttachedPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAttachedPolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listattachedpoliciespaginator)
    """

    async def paginate(
        self, *, target: str, recursive: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttachedPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAttachedPolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listattachedpoliciespaginator)
        """


class ListAuditFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditFindings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditfindingspaginator)
    """

    async def paginate(
        self,
        *,
        taskId: str = ...,
        checkName: str = ...,
        resourceIdentifier: "ResourceIdentifierTypeDef" = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        listSuppressedFindings: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditFindings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditfindingspaginator)
        """


class ListAuditMitigationActionsExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditmitigationactionsexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        taskId: str,
        findingId: str,
        actionStatus: AuditMitigationActionsExecutionStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditmitigationactionsexecutionspaginator)
        """


class ListAuditMitigationActionsTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditmitigationactionstaskspaginator)
    """

    async def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        auditTaskId: str = ...,
        findingId: str = ...,
        taskStatus: AuditMitigationActionsTaskStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditmitigationactionstaskspaginator)
        """


class ListAuditSuppressionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditSuppressions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditsuppressionspaginator)
    """

    async def paginate(
        self,
        *,
        checkName: str = ...,
        resourceIdentifier: "ResourceIdentifierTypeDef" = ...,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditSuppressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditSuppressions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauditsuppressionspaginator)
        """


class ListAuditTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listaudittaskspaginator)
    """

    async def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        taskType: AuditTaskTypeType = ...,
        taskStatus: AuditTaskStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuditTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuditTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listaudittaskspaginator)
        """


class ListAuthorizersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuthorizers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauthorizerspaginator)
    """

    async def paginate(
        self,
        *,
        ascendingOrder: bool = ...,
        status: AuthorizerStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListAuthorizers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listauthorizerspaginator)
        """


class ListBillingGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListBillingGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listbillinggroupspaginator)
    """

    async def paginate(
        self, *, namePrefixFilter: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBillingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListBillingGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listbillinggroupspaginator)
        """


class ListCACertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCACertificates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcacertificatespaginator)
    """

    async def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCACertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCACertificates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcacertificatespaginator)
        """


class ListCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcertificatespaginator)
    """

    async def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcertificatespaginator)
        """


class ListCertificatesByCAPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificatesByCA)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcertificatesbycapaginator)
    """

    async def paginate(
        self,
        *,
        caCertificateId: str,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificatesByCAResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCertificatesByCA.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcertificatesbycapaginator)
        """


class ListCustomMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCustomMetrics)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcustommetricspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListCustomMetrics.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listcustommetricspaginator)
        """


class ListDetectMitigationActionsExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdetectmitigationactionsexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        taskId: str = ...,
        violationId: str = ...,
        thingName: str = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDetectMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdetectmitigationactionsexecutionspaginator)
        """


class ListDetectMitigationActionsTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdetectmitigationactionstaskspaginator)
    """

    async def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDetectMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdetectmitigationactionstaskspaginator)
        """


class ListDimensionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDimensions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdimensionspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDimensionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDimensions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdimensionspaginator)
        """


class ListDomainConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDomainConfigurations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdomainconfigurationspaginator)
    """

    async def paginate(
        self, *, serviceType: ServiceTypeType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDomainConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListDomainConfigurations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listdomainconfigurationspaginator)
        """


class ListFleetMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListFleetMetrics)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listfleetmetricspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFleetMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListFleetMetrics.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listfleetmetricspaginator)
        """


class ListIndicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListIndices)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listindicespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListIndices.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listindicespaginator)
        """


class ListJobExecutionsForJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForJob)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobexecutionsforjobpaginator)
    """

    async def paginate(
        self,
        *,
        jobId: str,
        status: JobExecutionStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobExecutionsForJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForJob.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobexecutionsforjobpaginator)
        """


class ListJobExecutionsForThingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForThing)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobexecutionsforthingpaginator)
    """

    async def paginate(
        self,
        *,
        thingName: str,
        status: JobExecutionStatusType = ...,
        namespaceId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobExecutionsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForThing.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobexecutionsforthingpaginator)
        """


class ListJobTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobTemplates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobtemplatespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobtemplatespaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobspaginator)
    """

    async def paginate(
        self,
        *,
        status: JobStatusType = ...,
        targetSelection: TargetSelectionType = ...,
        thingGroupName: str = ...,
        thingGroupId: str = ...,
        namespaceId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listjobspaginator)
        """


class ListMitigationActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListMitigationActions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listmitigationactionspaginator)
    """

    async def paginate(
        self,
        *,
        actionType: MitigationActionTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMitigationActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListMitigationActions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listmitigationactionspaginator)
        """


class ListOTAUpdatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOTAUpdates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listotaupdatespaginator)
    """

    async def paginate(
        self,
        *,
        otaUpdateStatus: OTAUpdateStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOTAUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOTAUpdates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listotaupdatespaginator)
        """


class ListOutgoingCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOutgoingCertificates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listoutgoingcertificatespaginator)
    """

    async def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOutgoingCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListOutgoingCertificates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listoutgoingcertificatespaginator)
        """


class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listpoliciespaginator)
    """

    async def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listpoliciespaginator)
        """


class ListPolicyPrincipalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicyPrincipals)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listpolicyprincipalspaginator)
    """

    async def paginate(
        self,
        *,
        policyName: str,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPolicyPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPolicyPrincipals.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listpolicyprincipalspaginator)
        """


class ListPrincipalPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalPolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprincipalpoliciespaginator)
    """

    async def paginate(
        self,
        *,
        principal: str,
        ascendingOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPrincipalPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalPolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprincipalpoliciespaginator)
        """


class ListPrincipalThingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalThings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprincipalthingspaginator)
    """

    async def paginate(
        self, *, principal: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPrincipalThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListPrincipalThings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprincipalthingspaginator)
        """


class ListProvisioningTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplateVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprovisioningtemplateversionspaginator)
    """

    async def paginate(
        self, *, templateName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisioningTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplateVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprovisioningtemplateversionspaginator)
        """


class ListProvisioningTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprovisioningtemplatespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisioningTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listprovisioningtemplatespaginator)
        """


class ListRoleAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListRoleAliases)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listrolealiasespaginator)
    """

    async def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRoleAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListRoleAliases.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listrolealiasespaginator)
        """


class ListScheduledAuditsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListScheduledAudits)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listscheduledauditspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListScheduledAuditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListScheduledAudits.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listscheduledauditspaginator)
        """


class ListSecurityProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfiles)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listsecurityprofilespaginator)
    """

    async def paginate(
        self,
        *,
        dimensionName: str = ...,
        metricName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfiles.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listsecurityprofilespaginator)
        """


class ListSecurityProfilesForTargetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfilesForTarget)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listsecurityprofilesfortargetpaginator)
    """

    async def paginate(
        self,
        *,
        securityProfileTargetArn: str,
        recursive: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityProfilesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListSecurityProfilesForTarget.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listsecurityprofilesfortargetpaginator)
        """


class ListStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListStreams)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#liststreamspaginator)
    """

    async def paginate(
        self, *, ascendingOrder: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListStreams.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#liststreamspaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtagsforresourcepaginator)
    """

    async def paginate(
        self, *, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtagsforresourcepaginator)
        """


class ListTargetsForPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForPolicy)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtargetsforpolicypaginator)
    """

    async def paginate(
        self, *, policyName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForPolicy.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtargetsforpolicypaginator)
        """


class ListTargetsForSecurityProfilePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForSecurityProfile)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtargetsforsecurityprofilepaginator)
    """

    async def paginate(
        self, *, securityProfileName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetsForSecurityProfileResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTargetsForSecurityProfile.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtargetsforsecurityprofilepaginator)
        """


class ListThingGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthinggroupspaginator)
    """

    async def paginate(
        self,
        *,
        parentGroup: str = ...,
        namePrefixFilter: str = ...,
        recursive: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthinggroupspaginator)
        """


class ListThingGroupsForThingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroupsForThing)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthinggroupsforthingpaginator)
    """

    async def paginate(
        self, *, thingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingGroupsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingGroupsForThing.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthinggroupsforthingpaginator)
        """


class ListThingPrincipalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingPrincipals)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingprincipalspaginator)
    """

    async def paginate(
        self, *, thingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingPrincipals.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingprincipalspaginator)
        """


class ListThingRegistrationTaskReportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTaskReports)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingregistrationtaskreportspaginator)
    """

    async def paginate(
        self,
        *,
        taskId: str,
        reportType: ReportTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingRegistrationTaskReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTaskReports.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingregistrationtaskreportspaginator)
        """


class ListThingRegistrationTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingregistrationtaskspaginator)
    """

    async def paginate(
        self, *, status: StatusType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingRegistrationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingregistrationtaskspaginator)
        """


class ListThingTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingTypes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingtypespaginator)
    """

    async def paginate(
        self, *, thingTypeName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingTypes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingtypespaginator)
        """


class ListThingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingspaginator)
    """

    async def paginate(
        self,
        *,
        attributeName: str = ...,
        attributeValue: str = ...,
        thingTypeName: str = ...,
        usePrefixAttributeValue: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingspaginator)
        """


class ListThingsInBillingGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInBillingGroup)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingsinbillinggrouppaginator)
    """

    async def paginate(
        self, *, billingGroupName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingsInBillingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInBillingGroup.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingsinbillinggrouppaginator)
        """


class ListThingsInThingGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInThingGroup)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingsinthinggrouppaginator)
    """

    async def paginate(
        self,
        *,
        thingGroupName: str,
        recursive: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThingsInThingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListThingsInThingGroup.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listthingsinthinggrouppaginator)
        """


class ListTopicRuleDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRuleDestinations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtopicruledestinationspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTopicRuleDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRuleDestinations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtopicruledestinationspaginator)
        """


class ListTopicRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtopicrulespaginator)
    """

    async def paginate(
        self,
        *,
        topic: str = ...,
        ruleDisabled: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTopicRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListTopicRules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listtopicrulespaginator)
        """


class ListV2LoggingLevelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListV2LoggingLevels)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listv2logginglevelspaginator)
    """

    async def paginate(
        self, *, targetType: LogTargetTypeType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListV2LoggingLevelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListV2LoggingLevels.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listv2logginglevelspaginator)
        """


class ListViolationEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListViolationEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listviolationeventspaginator)
    """

    async def paginate(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        thingName: str = ...,
        securityProfileName: str = ...,
        behaviorCriteriaType: BehaviorCriteriaTypeType = ...,
        listSuppressedAlerts: bool = ...,
        verificationState: VerificationStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListViolationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Paginator.ListViolationEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators.html#listviolationeventspaginator)
        """
