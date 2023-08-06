"""
Type annotations for s3control service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3control.client import S3ControlClient
    from types_aiobotocore_s3control.paginator import (
        ListAccessPointsForObjectLambdaPaginator,
    )

    session = get_session()
    with session.create_client("s3control") as client:
        client: S3ControlClient

        list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListAccessPointsForObjectLambdaResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListAccessPointsForObjectLambdaPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessPointsForObjectLambdaPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators.html#listaccesspointsforobjectlambdapaginator)
    """

    async def paginate(
        self, *, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccessPointsForObjectLambdaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators.html#listaccesspointsforobjectlambdapaginator)
        """
