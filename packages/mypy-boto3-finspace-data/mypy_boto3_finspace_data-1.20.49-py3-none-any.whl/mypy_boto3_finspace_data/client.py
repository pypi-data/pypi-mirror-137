"""
Type annotations for finspace-data service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace_data.client import FinSpaceDataClient

    session = Session()
    client: FinSpaceDataClient = session.client("finspace-data")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ChangeTypeType, DatasetKindType, locationTypeType
from .paginator import ListChangesetsPaginator, ListDatasetsPaginator, ListDataViewsPaginator
from .type_defs import (
    CreateChangesetResponseTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDataViewResponseTypeDef,
    DatasetOwnerInfoTypeDef,
    DataViewDestinationTypeParamsTypeDef,
    DeleteDatasetResponseTypeDef,
    GetChangesetResponseTypeDef,
    GetDatasetResponseTypeDef,
    GetDataViewResponseTypeDef,
    GetProgrammaticAccessCredentialsResponseTypeDef,
    GetWorkingLocationResponseTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsResponseTypeDef,
    PermissionGroupParamsTypeDef,
    SchemaUnionTypeDef,
    UpdateChangesetResponseTypeDef,
    UpdateDatasetResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("FinSpaceDataClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class FinSpaceDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FinSpaceDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.exceptions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#can_paginate)
        """

    def create_changeset(
        self,
        *,
        datasetId: str,
        changeType: ChangeTypeType,
        sourceParams: Mapping[str, str],
        formatParams: Mapping[str, str],
        clientToken: str = ...
    ) -> CreateChangesetResponseTypeDef:
        """
        Creates a new Changeset in a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_changeset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#create_changeset)
        """

    def create_data_view(
        self,
        *,
        datasetId: str,
        destinationTypeParams: "DataViewDestinationTypeParamsTypeDef",
        clientToken: str = ...,
        autoUpdate: bool = ...,
        sortColumns: Sequence[str] = ...,
        partitionColumns: Sequence[str] = ...,
        asOfTimestamp: int = ...
    ) -> CreateDataViewResponseTypeDef:
        """
        Creates a Dataview for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_data_view)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#create_data_view)
        """

    def create_dataset(
        self,
        *,
        datasetTitle: str,
        kind: DatasetKindType,
        permissionGroupParams: "PermissionGroupParamsTypeDef",
        clientToken: str = ...,
        datasetDescription: str = ...,
        ownerInfo: "DatasetOwnerInfoTypeDef" = ...,
        alias: str = ...,
        schemaDefinition: "SchemaUnionTypeDef" = ...
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_dataset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#create_dataset)
        """

    def delete_dataset(
        self, *, datasetId: str, clientToken: str = ...
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.delete_dataset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#delete_dataset)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#generate_presigned_url)
        """

    def get_changeset(self, *, datasetId: str, changesetId: str) -> GetChangesetResponseTypeDef:
        """
        Get information about a Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_changeset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_changeset)
        """

    def get_data_view(self, *, dataViewId: str, datasetId: str) -> GetDataViewResponseTypeDef:
        """
        Gets information about a Dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_data_view)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_data_view)
        """

    def get_dataset(self, *, datasetId: str) -> GetDatasetResponseTypeDef:
        """
        Returns information about a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_dataset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_dataset)
        """

    def get_programmatic_access_credentials(
        self, *, environmentId: str, durationInMinutes: int = ...
    ) -> GetProgrammaticAccessCredentialsResponseTypeDef:
        """
        Request programmatic credentials to use with FinSpace SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_programmatic_access_credentials)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_programmatic_access_credentials)
        """

    def get_working_location(
        self, *, locationType: locationTypeType = ...
    ) -> GetWorkingLocationResponseTypeDef:
        """
        A temporary Amazon S3 location, where you can copy your files from a source
        location to stage or use as a scratch space in FinSpace notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_working_location)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_working_location)
        """

    def list_changesets(
        self, *, datasetId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListChangesetsResponseTypeDef:
        """
        Lists the FinSpace Changesets for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_changesets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#list_changesets)
        """

    def list_data_views(
        self, *, datasetId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDataViewsResponseTypeDef:
        """
        Lists all available Dataviews for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_data_views)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#list_data_views)
        """

    def list_datasets(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the active Datasets that a user has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_datasets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#list_datasets)
        """

    def update_changeset(
        self,
        *,
        datasetId: str,
        changesetId: str,
        sourceParams: Mapping[str, str],
        formatParams: Mapping[str, str],
        clientToken: str = ...
    ) -> UpdateChangesetResponseTypeDef:
        """
        Updates a FinSpace Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.update_changeset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#update_changeset)
        """

    def update_dataset(
        self,
        *,
        datasetId: str,
        datasetTitle: str,
        kind: DatasetKindType,
        clientToken: str = ...,
        datasetDescription: str = ...,
        alias: str = ...,
        schemaDefinition: "SchemaUnionTypeDef" = ...
    ) -> UpdateDatasetResponseTypeDef:
        """
        Updates a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.update_dataset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#update_dataset)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_changesets"]) -> ListChangesetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_views"]) -> ListDataViewsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client.html#get_paginator)
        """
