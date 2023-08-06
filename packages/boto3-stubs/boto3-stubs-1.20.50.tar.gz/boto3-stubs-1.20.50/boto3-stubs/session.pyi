import sys
from typing import Any, List, Optional, Union, overload

import boto3
import boto3.utils
import botocore.session
from boto3.exceptions import ResourceNotExistsError as ResourceNotExistsError
from boto3.exceptions import UnknownAPIVersionError as UnknownAPIVersionError
from boto3.resources.factory import ResourceFactory
from botocore.client import Config
from botocore.config import Config
from botocore.credentials import Credentials
from botocore.exceptions import DataNotFoundError as DataNotFoundError
from botocore.exceptions import UnknownServiceError as UnknownServiceError
from botocore.loaders import Loader
from botocore.model import ServiceModel as ServiceModel
from botocore.session import Session as BotocoreSession
from mypy_boto3_auditmanager.client import AuditManagerClient
from mypy_boto3_events.client import EventBridgeClient
from mypy_boto3_ssm_incidents.client import SSMIncidentsClient
from mypy_boto3_synthetics.client import SyntheticsClient

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

class Session:
    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        botocore_session: Optional[BotocoreSession] = None,
        profile_name: Optional[str] = None,
    ) -> None:
        self._session: BotocoreSession
        self.resource_factory: ResourceFactory
        self._loader: Loader
    def __repr__(self) -> str: ...
    @property
    def profile_name(self) -> str: ...
    @property
    def region_name(self) -> str: ...
    @property
    def events(self) -> List[Any]: ...
    @property
    def available_profiles(self) -> List[Any]: ...
    def _setup_loader(self) -> None: ...
    def get_available_services(self) -> List[str]: ...
    def get_available_resources(self) -> List[str]: ...
    def get_available_partitions(self) -> List[str]: ...
    def get_available_regions(
        self,
        service_name: str,
        partition_name: str = "aws",
        allow_non_regional: bool = False,
    ) -> List[str]: ...
    def get_credentials(self) -> Credentials: ...
    def _register_default_handlers(self) -> None: ...
    @overload
    def client(
        self,
        service_name: Literal["auditmanager"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AuditManagerClient: ...
    @overload
    def client(
        self,
        service_name: Literal["synthetics"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SyntheticsClient: ...
    @overload
    def client(
        self,
        service_name: Literal["ssm-incidents"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSMIncidentsClient: ...
    @overload
    def client(
        self,
        service_name: Literal["events"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EventBridgeClient: ...
