"""
Type annotations for cloudsearchdomain service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearchdomain.client import CloudSearchDomainClient

    session = get_session()
    async with session.create_client("cloudsearchdomain") as client:
        client: CloudSearchDomainClient
    ```
"""
from typing import IO, Any, Dict, Mapping, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import ContentTypeType, QueryParserType
from .type_defs import SearchResponseTypeDef, SuggestResponseTypeDef, UploadDocumentsResponseTypeDef

__all__ = ("CloudSearchDomainClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DocumentServiceException: Type[BotocoreClientError]
    SearchException: Type[BotocoreClientError]


class CloudSearchDomainClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudSearchDomainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html#generate_presigned_url)
        """

    async def search(
        self,
        *,
        query: str,
        cursor: str = ...,
        expr: str = ...,
        facet: str = ...,
        filterQuery: str = ...,
        highlight: str = ...,
        partial: bool = ...,
        queryOptions: str = ...,
        queryParser: QueryParserType = ...,
        returnFields: str = ...,
        size: int = ...,
        sort: str = ...,
        start: int = ...,
        stats: str = ...
    ) -> SearchResponseTypeDef:
        """
        Retrieves a list of documents that match the specified search criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.search)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html#search)
        """

    async def suggest(
        self, *, query: str, suggester: str, size: int = ...
    ) -> SuggestResponseTypeDef:
        """
        Retrieves autocomplete suggestions for a partial query string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.suggest)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html#suggest)
        """

    async def upload_documents(
        self, *, documents: Union[bytes, IO[bytes], StreamingBody], contentType: ContentTypeType
    ) -> UploadDocumentsResponseTypeDef:
        """
        Posts a batch of documents to a search domain for indexing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.upload_documents)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html#upload_documents)
        """

    async def __aenter__(self) -> "CloudSearchDomainClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/client.html)
        """
