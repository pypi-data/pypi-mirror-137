"""
Type annotations for elastic-inference service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elastic_inference.client import ElasticInferenceClient
    from types_aiobotocore_elastic_inference.paginator import (
        DescribeAcceleratorsPaginator,
    )

    session = get_session()
    with session.create_client("elastic-inference") as client:
        client: ElasticInferenceClient

        describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import DescribeAcceleratorsResponseTypeDef, FilterTypeDef, PaginatorConfigTypeDef

__all__ = ("DescribeAcceleratorsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAcceleratorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Paginator.DescribeAccelerators)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/paginators.html#describeacceleratorspaginator)
    """

    async def paginate(
        self,
        *,
        acceleratorIds: Sequence[str] = ...,
        filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Paginator.DescribeAccelerators.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/paginators.html#describeacceleratorspaginator)
        """
