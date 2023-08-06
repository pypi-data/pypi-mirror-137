from datetime import datetime
from typing import Any, Dict, List, Union
from uuid import UUID

from sila2.features.authorizationservice import (
    AuthorizationServiceBase,
    AuthorizationServiceFeature,
    InvalidAccessToken,
)
from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import MetadataInterceptor, SilaServer
from sila2.server.default_feature_implementations.authenticationservice_impl import AccessToken


class AuthorizationServiceImpl(AuthorizationServiceBase):
    parent_server: SilaServer

    def __init__(self, parent_server: SilaServer):
        self.parent_server = parent_server
        self.parent_server.add_metadata_interceptor(AuthorizationServiceInterceptor(parent_server))

    def get_calls_affected_by_AccessToken(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        affected_features = []
        for feature in self.parent_server.features.values():
            if feature._identifier in [
                "SiLAService",
                "AuthorizationService",
                "AuthenticationService",
                "AuthorizationProviderService",
            ]:
                continue
            affected_features.append(feature)
        return affected_features


class AuthorizationServiceInterceptor(MetadataInterceptor):
    access_tokens: Dict[UUID, AccessToken]

    def __init__(self, parent_server: SilaServer):
        self.accesstoken_fqi = AuthorizationServiceFeature["AccessToken"].fully_qualified_identifier
        super().__init__([self.accesstoken_fqi])
        self.access_tokens = parent_server.feature_servicers["AuthenticationService"].implementation.active_tokens

    def intercept(
        self, parameters: Any, metadata: Dict[FullyQualifiedIdentifier, Any], target_call: FullyQualifiedIdentifier
    ) -> None:
        raw_token: str = metadata.pop(self.accesstoken_fqi)

        try:
            token = self.access_tokens[UUID(raw_token)]
        except (KeyError, ValueError):
            raise InvalidAccessToken

        if token.remaining_lifetime.total_seconds() <= 0:
            self.access_tokens.pop(token.token)
            raise InvalidAccessToken

        token.last_usage = datetime.now()
