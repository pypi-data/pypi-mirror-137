from typing import TYPE_CHECKING

from .authorizationservice_base import AuthorizationServiceBase
from .authorizationservice_errors import InvalidAccessToken
from .authorizationservice_feature import AuthorizationServiceFeature

__all__ = [
    "AuthorizationServiceBase",
    "AuthorizationServiceFeature",
    "InvalidAccessToken",
]

if TYPE_CHECKING:
    from .authorizationservice_client import AuthorizationServiceClient  # noqa: F401

    __all__.append("AuthorizationServiceClient")
