"""
Type annotations for apigatewayv2 service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apigatewayv2.client import ApiGatewayV2Client
    from types_aiobotocore_apigatewayv2.paginator import (
        GetApisPaginator,
        GetAuthorizersPaginator,
        GetDeploymentsPaginator,
        GetDomainNamesPaginator,
        GetIntegrationResponsesPaginator,
        GetIntegrationsPaginator,
        GetModelsPaginator,
        GetRouteResponsesPaginator,
        GetRoutesPaginator,
        GetStagesPaginator,
    )

    session = get_session()
    with session.create_client("apigatewayv2") as client:
        client: ApiGatewayV2Client

        get_apis_paginator: GetApisPaginator = client.get_paginator("get_apis")
        get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
        get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
        get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
        get_integration_responses_paginator: GetIntegrationResponsesPaginator = client.get_paginator("get_integration_responses")
        get_integrations_paginator: GetIntegrationsPaginator = client.get_paginator("get_integrations")
        get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
        get_route_responses_paginator: GetRouteResponsesPaginator = client.get_paginator("get_route_responses")
        get_routes_paginator: GetRoutesPaginator = client.get_paginator("get_routes")
        get_stages_paginator: GetStagesPaginator = client.get_paginator("get_stages")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetApisResponseTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelsResponseTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRoutesResponseTypeDef,
    GetStagesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetApisPaginator",
    "GetAuthorizersPaginator",
    "GetDeploymentsPaginator",
    "GetDomainNamesPaginator",
    "GetIntegrationResponsesPaginator",
    "GetIntegrationsPaginator",
    "GetModelsPaginator",
    "GetRouteResponsesPaginator",
    "GetRoutesPaginator",
    "GetStagesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetApisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getapispaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getapispaginator)
        """


class GetAuthorizersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getauthorizerspaginator)
    """

    async def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getauthorizerspaginator)
        """


class GetDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getdeploymentspaginator)
    """

    async def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getdeploymentspaginator)
        """


class GetDomainNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getdomainnamespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getdomainnamespaginator)
        """


class GetIntegrationResponsesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getintegrationresponsespaginator)
    """

    async def paginate(
        self, *, ApiId: str, IntegrationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetIntegrationResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getintegrationresponsespaginator)
        """


class GetIntegrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getintegrationspaginator)
    """

    async def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getintegrationspaginator)
        """


class GetModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getmodelspaginator)
    """

    async def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getmodelspaginator)
        """


class GetRouteResponsesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getrouteresponsespaginator)
    """

    async def paginate(
        self, *, ApiId: str, RouteId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRouteResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getrouteresponsespaginator)
        """


class GetRoutesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getroutespaginator)
    """

    async def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getroutespaginator)
        """


class GetStagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getstagespaginator)
    """

    async def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetStagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators.html#getstagespaginator)
        """
