"""
Type annotations for globalaccelerator service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_globalaccelerator.client import GlobalAcceleratorClient
    from types_aiobotocore_globalaccelerator.paginator import (
        ListAcceleratorsPaginator,
        ListByoipCidrsPaginator,
        ListCustomRoutingAcceleratorsPaginator,
        ListCustomRoutingListenersPaginator,
        ListCustomRoutingPortMappingsPaginator,
        ListCustomRoutingPortMappingsByDestinationPaginator,
        ListEndpointGroupsPaginator,
        ListListenersPaginator,
    )

    session = get_session()
    with session.create_client("globalaccelerator") as client:
        client: GlobalAcceleratorClient

        list_accelerators_paginator: ListAcceleratorsPaginator = client.get_paginator("list_accelerators")
        list_byoip_cidrs_paginator: ListByoipCidrsPaginator = client.get_paginator("list_byoip_cidrs")
        list_custom_routing_accelerators_paginator: ListCustomRoutingAcceleratorsPaginator = client.get_paginator("list_custom_routing_accelerators")
        list_custom_routing_listeners_paginator: ListCustomRoutingListenersPaginator = client.get_paginator("list_custom_routing_listeners")
        list_custom_routing_port_mappings_paginator: ListCustomRoutingPortMappingsPaginator = client.get_paginator("list_custom_routing_port_mappings")
        list_custom_routing_port_mappings_by_destination_paginator: ListCustomRoutingPortMappingsByDestinationPaginator = client.get_paginator("list_custom_routing_port_mappings_by_destination")
        list_endpoint_groups_paginator: ListEndpointGroupsPaginator = client.get_paginator("list_endpoint_groups")
        list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAcceleratorsResponseTypeDef,
    ListByoipCidrsResponseTypeDef,
    ListCustomRoutingAcceleratorsResponseTypeDef,
    ListCustomRoutingListenersResponseTypeDef,
    ListCustomRoutingPortMappingsByDestinationResponseTypeDef,
    ListCustomRoutingPortMappingsResponseTypeDef,
    ListEndpointGroupsResponseTypeDef,
    ListListenersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAcceleratorsPaginator",
    "ListByoipCidrsPaginator",
    "ListCustomRoutingAcceleratorsPaginator",
    "ListCustomRoutingListenersPaginator",
    "ListCustomRoutingPortMappingsPaginator",
    "ListCustomRoutingPortMappingsByDestinationPaginator",
    "ListEndpointGroupsPaginator",
    "ListListenersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAcceleratorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListAccelerators)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listacceleratorspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListAccelerators.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listacceleratorspaginator)
        """


class ListByoipCidrsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListByoipCidrs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listbyoipcidrspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListByoipCidrsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListByoipCidrs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listbyoipcidrspaginator)
        """


class ListCustomRoutingAcceleratorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingAccelerators)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutingacceleratorspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomRoutingAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingAccelerators.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutingacceleratorspaginator)
        """


class ListCustomRoutingListenersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingListeners)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutinglistenerspaginator)
    """

    async def paginate(
        self, *, AcceleratorArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomRoutingListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingListeners.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutinglistenerspaginator)
        """


class ListCustomRoutingPortMappingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutingportmappingspaginator)
    """

    async def paginate(
        self,
        *,
        AcceleratorArn: str,
        EndpointGroupArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomRoutingPortMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutingportmappingspaginator)
        """


class ListCustomRoutingPortMappingsByDestinationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappingsByDestination)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutingportmappingsbydestinationpaginator)
    """

    async def paginate(
        self,
        *,
        EndpointId: str,
        DestinationAddress: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomRoutingPortMappingsByDestinationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappingsByDestination.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listcustomroutingportmappingsbydestinationpaginator)
        """


class ListEndpointGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListEndpointGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listendpointgroupspaginator)
    """

    async def paginate(
        self, *, ListenerArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListEndpointGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listendpointgroupspaginator)
        """


class ListListenersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListListeners)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listlistenerspaginator)
    """

    async def paginate(
        self, *, AcceleratorArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Paginator.ListListeners.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators.html#listlistenerspaginator)
        """
