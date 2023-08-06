from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .authenticationservice_types import Login_Responses, Logout_Responses


class AuthenticationServiceBase(FeatureImplementationBase, ABC):

    """
    This Feature provides SiLA Clients with access tokens based on a user identification and password.
    1. the user needs to login with the Login command into the server with a user identification (=user name) and a password
    2. after verification, an Access Token with the Token Lifetime information will be generated and provided by the server.
    3. the user can log-out from the server with the Logout command - a valid Access Token is required to run this command.
    """

    @abstractmethod
    def Login(
        self,
        UserIdentification: str,
        Password: str,
        RequestedServer: str,
        RequestedFeatures: List[str],
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
    ) -> Login_Responses:
        """
        Provides an access token based on user information.


        :param UserIdentification: The user identification string (e.g. a user name)

        :param Password: The password

        :param RequestedServer: The ServerUUID of the server for which an authorization is requested.

        :param RequestedFeatures: The fully qualified identifiers of features that are requested to access. If no feature is provided, this means that all features are requested.

        :param metadata: The SiLA Client Metadata attached to the call

        :return:

            - AccessToken: The token to be used along with accessing a Command or Property on a SiLA Server.

            - TokenLifetime: The lifetime (in seconds) of the provided access token as the maximum validity period after the last SiLA Server
        request.


        """
        pass

    @abstractmethod
    def Logout(self, AccessToken: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Logout_Responses:
        """
        Invalidates the given access token immediately.


        :param AccessToken: The access token to be invalidated.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
