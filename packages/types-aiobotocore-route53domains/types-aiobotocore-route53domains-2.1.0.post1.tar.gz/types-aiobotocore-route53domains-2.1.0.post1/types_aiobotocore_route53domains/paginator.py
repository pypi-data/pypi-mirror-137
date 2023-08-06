"""
Type annotations for route53domains service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53domains.client import Route53DomainsClient
    from types_aiobotocore_route53domains.paginator import (
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        ViewBillingPaginator,
    )

    session = get_session()
    with session.create_client("route53domains") as client:
        client: Route53DomainsClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
        list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
        view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    FilterConditionTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesResponseTypeDef,
    PaginatorConfigTypeDef,
    SortConditionTypeDef,
    ViewBillingResponseTypeDef,
)

__all__ = (
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "ViewBillingPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#listdomainspaginator)
    """

    async def paginate(
        self,
        *,
        FilterConditions: Sequence["FilterConditionTypeDef"] = ...,
        SortCondition: "SortConditionTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#listdomainspaginator)
        """


class ListOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListOperations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#listoperationspaginator)
    """

    async def paginate(
        self,
        *,
        SubmittedSince: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListOperations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#listoperationspaginator)
        """


class ListPricesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListPrices)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#listpricespaginator)
    """

    async def paginate(
        self, *, Tld: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPricesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListPrices.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#listpricespaginator)
        """


class ViewBillingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ViewBilling)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#viewbillingpaginator)
    """

    async def paginate(
        self,
        *,
        Start: Union[datetime, str] = ...,
        End: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ViewBillingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ViewBilling.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators.html#viewbillingpaginator)
        """
