"""
Type annotations for wisdom service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_wisdom.client import ConnectWisdomServiceClient
    from mypy_boto3_wisdom.paginator import (
        ListAssistantAssociationsPaginator,
        ListAssistantsPaginator,
        ListContentsPaginator,
        ListKnowledgeBasesPaginator,
        QueryAssistantPaginator,
        SearchContentPaginator,
        SearchSessionsPaginator,
    )

    session = Session()
    client: ConnectWisdomServiceClient = session.client("wisdom")

    list_assistant_associations_paginator: ListAssistantAssociationsPaginator = client.get_paginator("list_assistant_associations")
    list_assistants_paginator: ListAssistantsPaginator = client.get_paginator("list_assistants")
    list_contents_paginator: ListContentsPaginator = client.get_paginator("list_contents")
    list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
    query_assistant_paginator: QueryAssistantPaginator = client.get_paginator("query_assistant")
    search_content_paginator: SearchContentPaginator = client.get_paginator("search_content")
    search_sessions_paginator: SearchSessionsPaginator = client.get_paginator("search_sessions")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentsResponseTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    PaginatorConfigTypeDef,
    QueryAssistantResponseTypeDef,
    SearchContentResponseTypeDef,
    SearchExpressionTypeDef,
    SearchSessionsResponseTypeDef,
)

__all__ = (
    "ListAssistantAssociationsPaginator",
    "ListAssistantsPaginator",
    "ListContentsPaginator",
    "ListKnowledgeBasesPaginator",
    "QueryAssistantPaginator",
    "SearchContentPaginator",
    "SearchSessionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssistantAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListAssistantAssociations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listassistantassociationspaginator)
    """

    def paginate(
        self, *, assistantId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssistantAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListAssistantAssociations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listassistantassociationspaginator)
        """


class ListAssistantsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListAssistants)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listassistantspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssistantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListAssistants.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listassistantspaginator)
        """


class ListContentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListContents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listcontentspaginator)
    """

    def paginate(
        self, *, knowledgeBaseId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListContents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listcontentspaginator)
        """


class ListKnowledgeBasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListKnowledgeBases)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listknowledgebasespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.ListKnowledgeBases.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#listknowledgebasespaginator)
        """


class QueryAssistantPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.QueryAssistant)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#queryassistantpaginator)
    """

    def paginate(
        self, *, assistantId: str, queryText: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[QueryAssistantResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.QueryAssistant.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#queryassistantpaginator)
        """


class SearchContentPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.SearchContent)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#searchcontentpaginator)
    """

    def paginate(
        self,
        *,
        knowledgeBaseId: str,
        searchExpression: "SearchExpressionTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.SearchContent.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#searchcontentpaginator)
        """


class SearchSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.SearchSessions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#searchsessionspaginator)
    """

    def paginate(
        self,
        *,
        assistantId: str,
        searchExpression: "SearchExpressionTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Paginator.SearchSessions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_wisdom/paginators.html#searchsessionspaginator)
        """
