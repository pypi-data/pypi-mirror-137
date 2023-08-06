from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .authorizationproviderservice_types import Verify_Responses


class AuthorizationProviderServiceBase(FeatureImplementationBase, ABC):

    """
    This Feature provides SiLA Servers with the ability to check a given access token.
    """

    @abstractmethod
    def Verify(
        self,
        AccessToken: str,
        RequestedServer: str,
        RequestedFeature: str,
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
    ) -> Verify_Responses:
        """
        Verifies that a given token is valid for the requested server.


        :param AccessToken: The token to be used along with accessing a Command or Property on a SiLA Server.

        :param RequestedServer: The server for which an authorization is requested.

        :param RequestedFeature: The feature that is requested to access.

        :param metadata: The SiLA Client Metadata attached to the call

        :return:

            - TokenLifetime: The lifetime of the provided access token as the maximum validity period after the last SiLA Server request.


        """
        pass
