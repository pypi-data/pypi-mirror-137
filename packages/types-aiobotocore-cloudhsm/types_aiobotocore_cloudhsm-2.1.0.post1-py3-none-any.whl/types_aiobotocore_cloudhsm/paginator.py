"""
Type annotations for cloudhsm service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudhsm.client import CloudHSMClient
    from types_aiobotocore_cloudhsm.paginator import (
        ListHapgsPaginator,
        ListHsmsPaginator,
        ListLunaClientsPaginator,
    )

    session = get_session()
    with session.create_client("cloudhsm") as client:
        client: CloudHSMClient

        list_hapgs_paginator: ListHapgsPaginator = client.get_paginator("list_hapgs")
        list_hsms_paginator: ListHsmsPaginator = client.get_paginator("list_hsms")
        list_luna_clients_paginator: ListLunaClientsPaginator = client.get_paginator("list_luna_clients")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListHapgsResponseTypeDef,
    ListHsmsResponseTypeDef,
    ListLunaClientsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListHapgsPaginator", "ListHsmsPaginator", "ListLunaClientsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListHapgsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Paginator.ListHapgs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html#listhapgspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListHapgsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Paginator.ListHapgs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html#listhapgspaginator)
        """


class ListHsmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Paginator.ListHsms)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html#listhsmspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListHsmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Paginator.ListHsms.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html#listhsmspaginator)
        """


class ListLunaClientsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Paginator.ListLunaClients)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html#listlunaclientspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLunaClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Paginator.ListLunaClients.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators.html#listlunaclientspaginator)
        """
