"""
Type annotations for support service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_support.client import SupportClient
    from types_aiobotocore_support.paginator import (
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
    )

    session = get_session()
    with session.create_client("support") as client:
        client: SupportClient

        describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
        describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeCasesPaginator", "DescribeCommunicationsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCases)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators.html#describecasespaginator)
    """

    async def paginate(
        self,
        *,
        caseIdList: Sequence[str] = ...,
        displayId: str = ...,
        afterTime: str = ...,
        beforeTime: str = ...,
        includeResolvedCases: bool = ...,
        language: str = ...,
        includeCommunications: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCases.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators.html#describecasespaginator)
        """


class DescribeCommunicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCommunications)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators.html#describecommunicationspaginator)
    """

    async def paginate(
        self,
        *,
        caseId: str,
        beforeTime: str = ...,
        afterTime: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeCommunicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCommunications.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators.html#describecommunicationspaginator)
        """
