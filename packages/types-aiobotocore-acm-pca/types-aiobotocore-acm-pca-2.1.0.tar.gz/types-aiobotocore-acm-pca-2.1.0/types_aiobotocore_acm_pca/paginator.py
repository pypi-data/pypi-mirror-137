"""
Type annotations for acm-pca service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm_pca.client import ACMPCAClient
    from types_aiobotocore_acm_pca.paginator import (
        ListCertificateAuthoritiesPaginator,
        ListPermissionsPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("acm-pca") as client:
        client: ACMPCAClient

        list_certificate_authorities_paginator: ListCertificateAuthoritiesPaginator = client.get_paginator("list_certificate_authorities")
        list_permissions_paginator: ListPermissionsPaginator = client.get_paginator("list_permissions")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ResourceOwnerType
from .type_defs import (
    ListCertificateAuthoritiesResponseTypeDef,
    ListPermissionsResponseTypeDef,
    ListTagsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListCertificateAuthoritiesPaginator", "ListPermissionsPaginator", "ListTagsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCertificateAuthoritiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Paginator.ListCertificateAuthorities)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html#listcertificateauthoritiespaginator)
    """

    async def paginate(
        self,
        *,
        ResourceOwner: ResourceOwnerType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificateAuthoritiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Paginator.ListCertificateAuthorities.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html#listcertificateauthoritiespaginator)
        """


class ListPermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Paginator.ListPermissions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html#listpermissionspaginator)
    """

    async def paginate(
        self, *, CertificateAuthorityArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Paginator.ListPermissions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html#listpermissionspaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html#listtagspaginator)
    """

    async def paginate(
        self, *, CertificateAuthorityArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/paginators.html#listtagspaginator)
        """
