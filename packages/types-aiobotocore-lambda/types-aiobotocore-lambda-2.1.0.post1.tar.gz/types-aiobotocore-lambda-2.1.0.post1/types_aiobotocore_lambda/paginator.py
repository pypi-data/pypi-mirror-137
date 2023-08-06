"""
Type annotations for lambda service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda.client import LambdaClient
    from types_aiobotocore_lambda.paginator import (
        ListAliasesPaginator,
        ListCodeSigningConfigsPaginator,
        ListEventSourceMappingsPaginator,
        ListFunctionEventInvokeConfigsPaginator,
        ListFunctionsPaginator,
        ListFunctionsByCodeSigningConfigPaginator,
        ListLayerVersionsPaginator,
        ListLayersPaginator,
        ListProvisionedConcurrencyConfigsPaginator,
        ListVersionsByFunctionPaginator,
    )

    session = get_session()
    with session.create_client("lambda") as client:
        client: LambdaClient

        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_code_signing_configs_paginator: ListCodeSigningConfigsPaginator = client.get_paginator("list_code_signing_configs")
        list_event_source_mappings_paginator: ListEventSourceMappingsPaginator = client.get_paginator("list_event_source_mappings")
        list_function_event_invoke_configs_paginator: ListFunctionEventInvokeConfigsPaginator = client.get_paginator("list_function_event_invoke_configs")
        list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
        list_functions_by_code_signing_config_paginator: ListFunctionsByCodeSigningConfigPaginator = client.get_paginator("list_functions_by_code_signing_config")
        list_layer_versions_paginator: ListLayerVersionsPaginator = client.get_paginator("list_layer_versions")
        list_layers_paginator: ListLayersPaginator = client.get_paginator("list_layers")
        list_provisioned_concurrency_configs_paginator: ListProvisionedConcurrencyConfigsPaginator = client.get_paginator("list_provisioned_concurrency_configs")
        list_versions_by_function_paginator: ListVersionsByFunctionPaginator = client.get_paginator("list_versions_by_function")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ArchitectureType, RuntimeType
from .type_defs import (
    ListAliasesResponseTypeDef,
    ListCodeSigningConfigsResponseTypeDef,
    ListEventSourceMappingsResponseTypeDef,
    ListFunctionEventInvokeConfigsResponseTypeDef,
    ListFunctionsByCodeSigningConfigResponseTypeDef,
    ListFunctionsResponseTypeDef,
    ListLayersResponseTypeDef,
    ListLayerVersionsResponseTypeDef,
    ListProvisionedConcurrencyConfigsResponseTypeDef,
    ListVersionsByFunctionResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAliasesPaginator",
    "ListCodeSigningConfigsPaginator",
    "ListEventSourceMappingsPaginator",
    "ListFunctionEventInvokeConfigsPaginator",
    "ListFunctionsPaginator",
    "ListFunctionsByCodeSigningConfigPaginator",
    "ListLayerVersionsPaginator",
    "ListLayersPaginator",
    "ListProvisionedConcurrencyConfigsPaginator",
    "ListVersionsByFunctionPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listaliasespaginator)
    """

    async def paginate(
        self,
        *,
        FunctionName: str,
        FunctionVersion: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listaliasespaginator)
        """


class ListCodeSigningConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListCodeSigningConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listcodesigningconfigspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCodeSigningConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListCodeSigningConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listcodesigningconfigspaginator)
        """


class ListEventSourceMappingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListEventSourceMappings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listeventsourcemappingspaginator)
    """

    async def paginate(
        self,
        *,
        EventSourceArn: str = ...,
        FunctionName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEventSourceMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListEventSourceMappings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listeventsourcemappingspaginator)
        """


class ListFunctionEventInvokeConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListFunctionEventInvokeConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listfunctioneventinvokeconfigspaginator)
    """

    async def paginate(
        self, *, FunctionName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFunctionEventInvokeConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListFunctionEventInvokeConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listfunctioneventinvokeconfigspaginator)
        """


class ListFunctionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListFunctions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listfunctionspaginator)
    """

    async def paginate(
        self,
        *,
        MasterRegion: str = ...,
        FunctionVersion: Literal["ALL"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListFunctions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listfunctionspaginator)
        """


class ListFunctionsByCodeSigningConfigPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListFunctionsByCodeSigningConfig)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listfunctionsbycodesigningconfigpaginator)
    """

    async def paginate(
        self, *, CodeSigningConfigArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFunctionsByCodeSigningConfigResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListFunctionsByCodeSigningConfig.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listfunctionsbycodesigningconfigpaginator)
        """


class ListLayerVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListLayerVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listlayerversionspaginator)
    """

    async def paginate(
        self,
        *,
        LayerName: str,
        CompatibleRuntime: RuntimeType = ...,
        CompatibleArchitecture: ArchitectureType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLayerVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListLayerVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listlayerversionspaginator)
        """


class ListLayersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListLayers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listlayerspaginator)
    """

    async def paginate(
        self,
        *,
        CompatibleRuntime: RuntimeType = ...,
        CompatibleArchitecture: ArchitectureType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLayersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListLayers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listlayerspaginator)
        """


class ListProvisionedConcurrencyConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListProvisionedConcurrencyConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listprovisionedconcurrencyconfigspaginator)
    """

    async def paginate(
        self, *, FunctionName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisionedConcurrencyConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListProvisionedConcurrencyConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listprovisionedconcurrencyconfigspaginator)
        """


class ListVersionsByFunctionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListVersionsByFunction)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listversionsbyfunctionpaginator)
    """

    async def paginate(
        self, *, FunctionName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListVersionsByFunctionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Paginator.ListVersionsByFunction.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators.html#listversionsbyfunctionpaginator)
        """
