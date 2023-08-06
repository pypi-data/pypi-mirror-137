"""
Type annotations for waf service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_waf.client import WAFClient
    from types_aiobotocore_waf.paginator import (
        GetRateBasedRuleManagedKeysPaginator,
        ListActivatedRulesInRuleGroupPaginator,
        ListByteMatchSetsPaginator,
        ListGeoMatchSetsPaginator,
        ListIPSetsPaginator,
        ListLoggingConfigurationsPaginator,
        ListRateBasedRulesPaginator,
        ListRegexMatchSetsPaginator,
        ListRegexPatternSetsPaginator,
        ListRuleGroupsPaginator,
        ListRulesPaginator,
        ListSizeConstraintSetsPaginator,
        ListSqlInjectionMatchSetsPaginator,
        ListSubscribedRuleGroupsPaginator,
        ListWebACLsPaginator,
        ListXssMatchSetsPaginator,
    )

    session = get_session()
    with session.create_client("waf") as client:
        client: WAFClient

        get_rate_based_rule_managed_keys_paginator: GetRateBasedRuleManagedKeysPaginator = client.get_paginator("get_rate_based_rule_managed_keys")
        list_activated_rules_in_rule_group_paginator: ListActivatedRulesInRuleGroupPaginator = client.get_paginator("list_activated_rules_in_rule_group")
        list_byte_match_sets_paginator: ListByteMatchSetsPaginator = client.get_paginator("list_byte_match_sets")
        list_geo_match_sets_paginator: ListGeoMatchSetsPaginator = client.get_paginator("list_geo_match_sets")
        list_ip_sets_paginator: ListIPSetsPaginator = client.get_paginator("list_ip_sets")
        list_logging_configurations_paginator: ListLoggingConfigurationsPaginator = client.get_paginator("list_logging_configurations")
        list_rate_based_rules_paginator: ListRateBasedRulesPaginator = client.get_paginator("list_rate_based_rules")
        list_regex_match_sets_paginator: ListRegexMatchSetsPaginator = client.get_paginator("list_regex_match_sets")
        list_regex_pattern_sets_paginator: ListRegexPatternSetsPaginator = client.get_paginator("list_regex_pattern_sets")
        list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_size_constraint_sets_paginator: ListSizeConstraintSetsPaginator = client.get_paginator("list_size_constraint_sets")
        list_sql_injection_match_sets_paginator: ListSqlInjectionMatchSetsPaginator = client.get_paginator("list_sql_injection_match_sets")
        list_subscribed_rule_groups_paginator: ListSubscribedRuleGroupsPaginator = client.get_paginator("list_subscribed_rule_groups")
        list_web_acls_paginator: ListWebACLsPaginator = client.get_paginator("list_web_acls")
        list_xss_match_sets_paginator: ListXssMatchSetsPaginator = client.get_paginator("list_xss_match_sets")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetRateBasedRuleManagedKeysResponseTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetRateBasedRuleManagedKeysPaginator",
    "ListActivatedRulesInRuleGroupPaginator",
    "ListByteMatchSetsPaginator",
    "ListGeoMatchSetsPaginator",
    "ListIPSetsPaginator",
    "ListLoggingConfigurationsPaginator",
    "ListRateBasedRulesPaginator",
    "ListRegexMatchSetsPaginator",
    "ListRegexPatternSetsPaginator",
    "ListRuleGroupsPaginator",
    "ListRulesPaginator",
    "ListSizeConstraintSetsPaginator",
    "ListSqlInjectionMatchSetsPaginator",
    "ListSubscribedRuleGroupsPaginator",
    "ListWebACLsPaginator",
    "ListXssMatchSetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetRateBasedRuleManagedKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.GetRateBasedRuleManagedKeys)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#getratebasedrulemanagedkeyspaginator)
    """

    async def paginate(
        self, *, RuleId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRateBasedRuleManagedKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.GetRateBasedRuleManagedKeys.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#getratebasedrulemanagedkeyspaginator)
        """


class ListActivatedRulesInRuleGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListActivatedRulesInRuleGroup)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listactivatedrulesinrulegrouppaginator)
    """

    async def paginate(
        self, *, RuleGroupId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActivatedRulesInRuleGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListActivatedRulesInRuleGroup.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listactivatedrulesinrulegrouppaginator)
        """


class ListByteMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListByteMatchSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listbytematchsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListByteMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListByteMatchSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listbytematchsetspaginator)
        """


class ListGeoMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListGeoMatchSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listgeomatchsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGeoMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListGeoMatchSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listgeomatchsetspaginator)
        """


class ListIPSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListIPSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listipsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIPSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListIPSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listipsetspaginator)
        """


class ListLoggingConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListLoggingConfigurations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listloggingconfigurationspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLoggingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListLoggingConfigurations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listloggingconfigurationspaginator)
        """


class ListRateBasedRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRateBasedRules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listratebasedrulespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRateBasedRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRateBasedRules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listratebasedrulespaginator)
        """


class ListRegexMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRegexMatchSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listregexmatchsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRegexMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRegexMatchSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listregexmatchsetspaginator)
        """


class ListRegexPatternSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRegexPatternSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listregexpatternsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRegexPatternSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRegexPatternSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listregexpatternsetspaginator)
        """


class ListRuleGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRuleGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listrulegroupspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRuleGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listrulegroupspaginator)
        """


class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listrulespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListRules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listrulespaginator)
        """


class ListSizeConstraintSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListSizeConstraintSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listsizeconstraintsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSizeConstraintSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListSizeConstraintSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listsizeconstraintsetspaginator)
        """


class ListSqlInjectionMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListSqlInjectionMatchSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listsqlinjectionmatchsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSqlInjectionMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListSqlInjectionMatchSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listsqlinjectionmatchsetspaginator)
        """


class ListSubscribedRuleGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListSubscribedRuleGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listsubscribedrulegroupspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSubscribedRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListSubscribedRuleGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listsubscribedrulegroupspaginator)
        """


class ListWebACLsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListWebACLs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listwebaclspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWebACLsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListWebACLs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listwebaclspaginator)
        """


class ListXssMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListXssMatchSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listxssmatchsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListXssMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Paginator.ListXssMatchSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators.html#listxssmatchsetspaginator)
        """
