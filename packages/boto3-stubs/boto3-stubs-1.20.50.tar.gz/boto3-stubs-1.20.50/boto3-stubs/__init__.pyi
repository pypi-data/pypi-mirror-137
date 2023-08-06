import importlib.util
import logging
import sys
from typing import Any, Optional, Union, overload

import boto3.session as session
from boto3.session import Session
from botocore.config import Config
from mypy_boto3_auditmanager.client import AuditManagerClient
from mypy_boto3_events.client import EventBridgeClient
from mypy_boto3_ssm_incidents.client import SSMIncidentsClient
from mypy_boto3_synthetics.client import SyntheticsClient

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
__all__ = (
    "DEFAULT_SESSION",
    "NullHandler",
    "Session",
    "client",
    "resource",
    "session",
    "set_stream_logger",
    "setup_default_session",
)

__author__: str
__version__: str

DEFAULT_SESSION: Optional[Session] = None

def setup_default_session(
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    region_name: str = None,
    botocore_session: str = None,
    profile_name: str = None,
) -> Session: ...
def set_stream_logger(
    name: str = "boto3", level: int = logging.DEBUG, format_string: Optional[str] = None
) -> None: ...
def _get_default_session() -> Session: ...

class NullHandler(logging.Handler):
    def emit(self, record: Any) -> Any: ...

@overload
def client(
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
