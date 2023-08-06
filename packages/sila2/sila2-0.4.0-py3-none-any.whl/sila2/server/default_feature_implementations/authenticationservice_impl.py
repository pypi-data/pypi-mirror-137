import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
from uuid import UUID

from sila2.features.authenticationservice import (
    AuthenticationFailed,
    AuthenticationServiceBase,
    InvalidAccessToken,
    Login_Responses,
    Logout_Responses,
)
from sila2.framework import FullyQualifiedIdentifier
from sila2.server import SilaServer


@dataclass
class AccessToken:
    token: UUID
    features: Tuple[FullyQualifiedIdentifier]
    lifetime_period: timedelta
    last_usage: datetime

    @property
    def remaining_lifetime(self) -> timedelta:
        return self.lifetime_period - (datetime.now() - self.last_usage)


class AuthenticationServiceImpl(AuthenticationServiceBase):
    def __init__(self, parent_server: SilaServer):
        self.parent_server = parent_server
        self.active_tokens: Dict[UUID, AccessToken] = {}

    def Login(
        self,
        UserIdentification: str,
        Password: str,
        RequestedServer: str,
        RequestedFeatures: List[str],
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Login_Responses:
        if UUID(RequestedServer) != self.parent_server.server_uuid:
            raise AuthenticationFailed

        # TODO: adapt to your needs
        if (UserIdentification, Password) != ("admin", "admin"):
            raise AuthenticationFailed

        server_feature_ids = {f.fully_qualified_identifier for f in self.parent_server.features.values()}
        for feature_id in RequestedFeatures:
            if FullyQualifiedIdentifier(feature_id) not in server_feature_ids:
                raise AuthenticationFailed

        token = AccessToken(uuid.uuid4(), tuple(server_feature_ids), timedelta(seconds=60 * 60), datetime.now())
        self.active_tokens[token.token] = token
        return Login_Responses(str(token.token), int(token.remaining_lifetime.total_seconds()))

    def Logout(self, AccessToken: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Logout_Responses:
        try:
            token = self.active_tokens.pop(UUID(AccessToken))
        except (KeyError, ValueError):  # unknown token or no UUID
            raise InvalidAccessToken

        if token.remaining_lifetime.total_seconds() <= 0:
            self.active_tokens.pop(token.token)
            raise InvalidAccessToken
