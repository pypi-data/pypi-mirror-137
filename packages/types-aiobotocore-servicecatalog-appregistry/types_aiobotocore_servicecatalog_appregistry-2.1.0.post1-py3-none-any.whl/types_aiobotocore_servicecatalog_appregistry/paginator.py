"""
Type annotations for servicecatalog-appregistry service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_servicecatalog_appregistry.client import AppRegistryClient
    from types_aiobotocore_servicecatalog_appregistry.paginator import (
        ListApplicationsPaginator,
        ListAssociatedAttributeGroupsPaginator,
        ListAssociatedResourcesPaginator,
        ListAttributeGroupsPaginator,
    )

    session = get_session()
    with session.create_client("servicecatalog-appregistry") as client:
        client: AppRegistryClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_associated_attribute_groups_paginator: ListAssociatedAttributeGroupsPaginator = client.get_paginator("list_associated_attribute_groups")
        list_associated_resources_paginator: ListAssociatedResourcesPaginator = client.get_paginator("list_associated_resources")
        list_attribute_groups_paginator: ListAttributeGroupsPaginator = client.get_paginator("list_attribute_groups")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationsResponseTypeDef,
    ListAssociatedAttributeGroupsResponseTypeDef,
    ListAssociatedResourcesResponseTypeDef,
    ListAttributeGroupsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListApplicationsPaginator",
    "ListAssociatedAttributeGroupsPaginator",
    "ListAssociatedResourcesPaginator",
    "ListAttributeGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listapplicationspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listapplicationspaginator)
        """


class ListAssociatedAttributeGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedAttributeGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listassociatedattributegroupspaginator)
    """

    async def paginate(
        self, *, application: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedAttributeGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listassociatedattributegroupspaginator)
        """


class ListAssociatedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listassociatedresourcespaginator)
    """

    async def paginate(
        self, *, application: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listassociatedresourcespaginator)
        """


class ListAttributeGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAttributeGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listattributegroupspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAttributeGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators.html#listattributegroupspaginator)
        """
