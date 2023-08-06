"""
Type annotations for appstream service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appstream.client import AppStreamClient
    from types_aiobotocore_appstream.paginator import (
        DescribeDirectoryConfigsPaginator,
        DescribeFleetsPaginator,
        DescribeImageBuildersPaginator,
        DescribeImagesPaginator,
        DescribeSessionsPaginator,
        DescribeStacksPaginator,
        DescribeUserStackAssociationsPaginator,
        DescribeUsersPaginator,
        ListAssociatedFleetsPaginator,
        ListAssociatedStacksPaginator,
    )

    session = get_session()
    with session.create_client("appstream") as client:
        client: AppStreamClient

        describe_directory_configs_paginator: DescribeDirectoryConfigsPaginator = client.get_paginator("describe_directory_configs")
        describe_fleets_paginator: DescribeFleetsPaginator = client.get_paginator("describe_fleets")
        describe_image_builders_paginator: DescribeImageBuildersPaginator = client.get_paginator("describe_image_builders")
        describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
        describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
        describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
        describe_user_stack_associations_paginator: DescribeUserStackAssociationsPaginator = client.get_paginator("describe_user_stack_associations")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
        list_associated_fleets_paginator: ListAssociatedFleetsPaginator = client.get_paginator("list_associated_fleets")
        list_associated_stacks_paginator: ListAssociatedStacksPaginator = client.get_paginator("list_associated_stacks")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import AuthenticationTypeType, VisibilityTypeType
from .type_defs import (
    DescribeDirectoryConfigsResultTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksResultTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeDirectoryConfigsPaginator",
    "DescribeFleetsPaginator",
    "DescribeImageBuildersPaginator",
    "DescribeImagesPaginator",
    "DescribeSessionsPaginator",
    "DescribeStacksPaginator",
    "DescribeUserStackAssociationsPaginator",
    "DescribeUsersPaginator",
    "ListAssociatedFleetsPaginator",
    "ListAssociatedStacksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeDirectoryConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeDirectoryConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describedirectoryconfigspaginator)
    """

    async def paginate(
        self, *, DirectoryNames: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDirectoryConfigsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeDirectoryConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describedirectoryconfigspaginator)
        """


class DescribeFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeFleets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describefleetspaginator)
    """

    async def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeFleets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describefleetspaginator)
        """


class DescribeImageBuildersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeImageBuilders)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeimagebuilderspaginator)
    """

    async def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeImageBuildersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeImageBuilders.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeimagebuilderspaginator)
        """


class DescribeImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeImages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeimagespaginator)
    """

    async def paginate(
        self,
        *,
        Names: Sequence[str] = ...,
        Arns: Sequence[str] = ...,
        Type: VisibilityTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeImages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeimagespaginator)
        """


class DescribeSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeSessions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describesessionspaginator)
    """

    async def paginate(
        self,
        *,
        StackName: str,
        FleetName: str,
        UserId: str = ...,
        AuthenticationType: AuthenticationTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeSessions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describesessionspaginator)
        """


class DescribeStacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeStacks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describestackspaginator)
    """

    async def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeStacks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describestackspaginator)
        """


class DescribeUserStackAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeUserStackAssociations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeuserstackassociationspaginator)
    """

    async def paginate(
        self,
        *,
        StackName: str = ...,
        UserName: str = ...,
        AuthenticationType: AuthenticationTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeUserStackAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeUserStackAssociations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeuserstackassociationspaginator)
        """


class DescribeUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeUsers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeuserspaginator)
    """

    async def paginate(
        self,
        *,
        AuthenticationType: AuthenticationTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#describeuserspaginator)
        """


class ListAssociatedFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.ListAssociatedFleets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#listassociatedfleetspaginator)
    """

    async def paginate(
        self, *, StackName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.ListAssociatedFleets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#listassociatedfleetspaginator)
        """


class ListAssociatedStacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.ListAssociatedStacks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#listassociatedstackspaginator)
    """

    async def paginate(
        self, *, FleetName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Paginator.ListAssociatedStacks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators.html#listassociatedstackspaginator)
        """
