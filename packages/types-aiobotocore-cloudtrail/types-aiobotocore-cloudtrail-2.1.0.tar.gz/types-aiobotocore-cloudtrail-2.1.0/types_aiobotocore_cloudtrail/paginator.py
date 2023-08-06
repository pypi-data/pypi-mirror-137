"""
Type annotations for cloudtrail service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudtrail.client import CloudTrailClient
    from types_aiobotocore_cloudtrail.paginator import (
        ListPublicKeysPaginator,
        ListTagsPaginator,
        ListTrailsPaginator,
        LookupEventsPaginator,
    )

    session = get_session()
    with session.create_client("cloudtrail") as client:
        client: CloudTrailClient

        list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_trails_paginator: ListTrailsPaginator = client.get_paginator("list_trails")
        lookup_events_paginator: LookupEventsPaginator = client.get_paginator("lookup_events")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListPublicKeysResponseTypeDef,
    ListTagsResponseTypeDef,
    ListTrailsResponseTypeDef,
    LookupAttributeTypeDef,
    LookupEventsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListPublicKeysPaginator",
    "ListTagsPaginator",
    "ListTrailsPaginator",
    "LookupEventsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListPublicKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.ListPublicKeys)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#listpublickeyspaginator)
    """

    async def paginate(
        self,
        *,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.ListPublicKeys.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#listpublickeyspaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#listtagspaginator)
    """

    async def paginate(
        self, *, ResourceIdList: Sequence[str], PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#listtagspaginator)
        """


class ListTrailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.ListTrails)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#listtrailspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.ListTrails.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#listtrailspaginator)
        """


class LookupEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.LookupEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#lookupeventspaginator)
    """

    async def paginate(
        self,
        *,
        LookupAttributes: Sequence["LookupAttributeTypeDef"] = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        EventCategory: Literal["insight"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[LookupEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Paginator.LookupEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators.html#lookupeventspaginator)
        """
