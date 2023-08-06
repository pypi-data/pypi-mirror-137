from typing import TYPE_CHECKING

from .authenticationservice_base import AuthenticationServiceBase
from .authenticationservice_errors import AuthenticationFailed, InvalidAccessToken
from .authenticationservice_feature import AuthenticationServiceFeature
from .authenticationservice_types import Login_Responses, Logout_Responses

__all__ = [
    "AuthenticationServiceBase",
    "AuthenticationServiceFeature",
    "Login_Responses",
    "Logout_Responses",
    "AuthenticationFailed",
    "InvalidAccessToken",
]

if TYPE_CHECKING:
    from .authenticationservice_client import AuthenticationServiceClient  # noqa: F401

    __all__.append("AuthenticationServiceClient")
