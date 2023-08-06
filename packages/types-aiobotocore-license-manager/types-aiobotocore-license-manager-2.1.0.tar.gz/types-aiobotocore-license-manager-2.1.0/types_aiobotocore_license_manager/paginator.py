"""
Type annotations for license-manager service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_license_manager.client import LicenseManagerClient
    from types_aiobotocore_license_manager.paginator import (
        ListAssociationsForLicenseConfigurationPaginator,
        ListLicenseConfigurationsPaginator,
        ListLicenseSpecificationsForResourcePaginator,
        ListResourceInventoryPaginator,
        ListUsageForLicenseConfigurationPaginator,
    )

    session = get_session()
    with session.create_client("license-manager") as client:
        client: LicenseManagerClient

        list_associations_for_license_configuration_paginator: ListAssociationsForLicenseConfigurationPaginator = client.get_paginator("list_associations_for_license_configuration")
        list_license_configurations_paginator: ListLicenseConfigurationsPaginator = client.get_paginator("list_license_configurations")
        list_license_specifications_for_resource_paginator: ListLicenseSpecificationsForResourcePaginator = client.get_paginator("list_license_specifications_for_resource")
        list_resource_inventory_paginator: ListResourceInventoryPaginator = client.get_paginator("list_resource_inventory")
        list_usage_for_license_configuration_paginator: ListUsageForLicenseConfigurationPaginator = client.get_paginator("list_usage_for_license_configuration")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    FilterTypeDef,
    InventoryFilterTypeDef,
    ListAssociationsForLicenseConfigurationResponseTypeDef,
    ListLicenseConfigurationsResponseTypeDef,
    ListLicenseSpecificationsForResourceResponseTypeDef,
    ListResourceInventoryResponseTypeDef,
    ListUsageForLicenseConfigurationResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAssociationsForLicenseConfigurationPaginator",
    "ListLicenseConfigurationsPaginator",
    "ListLicenseSpecificationsForResourcePaginator",
    "ListResourceInventoryPaginator",
    "ListUsageForLicenseConfigurationPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssociationsForLicenseConfigurationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListAssociationsForLicenseConfiguration)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listassociationsforlicenseconfigurationpaginator)
    """

    async def paginate(
        self, *, LicenseConfigurationArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociationsForLicenseConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListAssociationsForLicenseConfiguration.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listassociationsforlicenseconfigurationpaginator)
        """


class ListLicenseConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListLicenseConfigurations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listlicenseconfigurationspaginator)
    """

    async def paginate(
        self,
        *,
        LicenseConfigurationArns: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLicenseConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListLicenseConfigurations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listlicenseconfigurationspaginator)
        """


class ListLicenseSpecificationsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListLicenseSpecificationsForResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listlicensespecificationsforresourcepaginator)
    """

    async def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLicenseSpecificationsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListLicenseSpecificationsForResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listlicensespecificationsforresourcepaginator)
        """


class ListResourceInventoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListResourceInventory)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listresourceinventorypaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["InventoryFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceInventoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListResourceInventory.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listresourceinventorypaginator)
        """


class ListUsageForLicenseConfigurationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListUsageForLicenseConfiguration)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listusageforlicenseconfigurationpaginator)
    """

    async def paginate(
        self,
        *,
        LicenseConfigurationArn: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsageForLicenseConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Paginator.ListUsageForLicenseConfiguration.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators.html#listusageforlicenseconfigurationpaginator)
        """
