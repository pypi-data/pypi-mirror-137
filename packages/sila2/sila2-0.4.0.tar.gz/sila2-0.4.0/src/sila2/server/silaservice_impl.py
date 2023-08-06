from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from sila2.features.silaservice import SiLAServiceBase, UnimplementedFeature
from sila2.framework import FullyQualifiedIdentifier

if TYPE_CHECKING:
    from sila2.server.sila_server import SilaServer


class SiLAServiceImpl(SiLAServiceBase):
    parent_server: SilaServer

    def __init__(self, parent_server: SilaServer):
        self.parent_server = parent_server

    def GetFeatureDefinition(self, FeatureIdentifier: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        if FeatureIdentifier not in (f.fully_qualified_identifier for f in self.parent_server.features.values()):
            raise UnimplementedFeature(f"Feature {FeatureIdentifier} is not implemented by this server")

        return self.parent_server.features[FeatureIdentifier.split("/")[-2]]._feature_definition

    def SetServerName(self, ServerName: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        self.parent_server.server_name = ServerName

    def get_ImplementedFeatures(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> List[str]:
        return [f.fully_qualified_identifier for f in self.parent_server.features.values()]

    def get_ServerName(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return self.parent_server.server_name

    def get_ServerType(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return self.parent_server.server_type

    def get_ServerUUID(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return str(self.parent_server.server_uuid)

    def get_ServerDescription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return self.parent_server.server_description

    def get_ServerVersion(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return self.parent_server.server_version

    def get_ServerVendorURL(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return self.parent_server.server_vendor_url
