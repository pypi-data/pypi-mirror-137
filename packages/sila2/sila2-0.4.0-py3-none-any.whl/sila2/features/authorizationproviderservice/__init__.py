from typing import TYPE_CHECKING

from .authorizationproviderservice_base import AuthorizationProviderServiceBase
from .authorizationproviderservice_errors import AuthorizationFailed, InvalidAccessToken
from .authorizationproviderservice_feature import AuthorizationProviderServiceFeature
from .authorizationproviderservice_types import Verify_Responses

__all__ = [
    "AuthorizationProviderServiceBase",
    "AuthorizationProviderServiceFeature",
    "Verify_Responses",
    "AuthorizationFailed",
    "InvalidAccessToken",
]

if TYPE_CHECKING:
    from .authorizationproviderservice_client import AuthorizationProviderServiceClient  # noqa: F401

    __all__.append("AuthorizationProviderServiceClient")
