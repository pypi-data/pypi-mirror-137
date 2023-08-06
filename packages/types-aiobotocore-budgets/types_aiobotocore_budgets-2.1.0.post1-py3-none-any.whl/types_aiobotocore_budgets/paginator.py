"""
Type annotations for budgets service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_budgets.client import BudgetsClient
    from types_aiobotocore_budgets.paginator import (
        DescribeBudgetActionHistoriesPaginator,
        DescribeBudgetActionsForAccountPaginator,
        DescribeBudgetActionsForBudgetPaginator,
        DescribeBudgetPerformanceHistoryPaginator,
        DescribeBudgetsPaginator,
        DescribeNotificationsForBudgetPaginator,
        DescribeSubscribersForNotificationPaginator,
    )

    session = get_session()
    with session.create_client("budgets") as client:
        client: BudgetsClient

        describe_budget_action_histories_paginator: DescribeBudgetActionHistoriesPaginator = client.get_paginator("describe_budget_action_histories")
        describe_budget_actions_for_account_paginator: DescribeBudgetActionsForAccountPaginator = client.get_paginator("describe_budget_actions_for_account")
        describe_budget_actions_for_budget_paginator: DescribeBudgetActionsForBudgetPaginator = client.get_paginator("describe_budget_actions_for_budget")
        describe_budget_performance_history_paginator: DescribeBudgetPerformanceHistoryPaginator = client.get_paginator("describe_budget_performance_history")
        describe_budgets_paginator: DescribeBudgetsPaginator = client.get_paginator("describe_budgets")
        describe_notifications_for_budget_paginator: DescribeNotificationsForBudgetPaginator = client.get_paginator("describe_notifications_for_budget")
        describe_subscribers_for_notification_paginator: DescribeSubscribersForNotificationPaginator = client.get_paginator("describe_subscribers_for_notification")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeBudgetActionHistoriesResponseTypeDef,
    DescribeBudgetActionsForAccountResponseTypeDef,
    DescribeBudgetActionsForBudgetResponseTypeDef,
    DescribeBudgetPerformanceHistoryResponseTypeDef,
    DescribeBudgetsResponseTypeDef,
    DescribeNotificationsForBudgetResponseTypeDef,
    DescribeSubscribersForNotificationResponseTypeDef,
    NotificationTypeDef,
    PaginatorConfigTypeDef,
    TimePeriodTypeDef,
)

__all__ = (
    "DescribeBudgetActionHistoriesPaginator",
    "DescribeBudgetActionsForAccountPaginator",
    "DescribeBudgetActionsForBudgetPaginator",
    "DescribeBudgetPerformanceHistoryPaginator",
    "DescribeBudgetsPaginator",
    "DescribeNotificationsForBudgetPaginator",
    "DescribeSubscribersForNotificationPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeBudgetActionHistoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionHistories)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetactionhistoriespaginator)
    """

    async def paginate(
        self,
        *,
        AccountId: str,
        BudgetName: str,
        ActionId: str,
        TimePeriod: "TimePeriodTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBudgetActionHistoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionHistories.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetactionhistoriespaginator)
        """


class DescribeBudgetActionsForAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForAccount)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetactionsforaccountpaginator)
    """

    async def paginate(
        self, *, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBudgetActionsForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForAccount.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetactionsforaccountpaginator)
        """


class DescribeBudgetActionsForBudgetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForBudget)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetactionsforbudgetpaginator)
    """

    async def paginate(
        self, *, AccountId: str, BudgetName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBudgetActionsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForBudget.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetactionsforbudgetpaginator)
        """


class DescribeBudgetPerformanceHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetPerformanceHistory)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetperformancehistorypaginator)
    """

    async def paginate(
        self,
        *,
        AccountId: str,
        BudgetName: str,
        TimePeriod: "TimePeriodTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBudgetPerformanceHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetPerformanceHistory.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetperformancehistorypaginator)
        """


class DescribeBudgetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetspaginator)
    """

    async def paginate(
        self, *, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeBudgets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describebudgetspaginator)
        """


class DescribeNotificationsForBudgetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeNotificationsForBudget)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describenotificationsforbudgetpaginator)
    """

    async def paginate(
        self, *, AccountId: str, BudgetName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeNotificationsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeNotificationsForBudget.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describenotificationsforbudgetpaginator)
        """


class DescribeSubscribersForNotificationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeSubscribersForNotification)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describesubscribersfornotificationpaginator)
    """

    async def paginate(
        self,
        *,
        AccountId: str,
        BudgetName: str,
        Notification: "NotificationTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSubscribersForNotificationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Paginator.DescribeSubscribersForNotification.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators.html#describesubscribersfornotificationpaginator)
        """
