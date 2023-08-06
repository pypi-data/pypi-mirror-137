from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from sila2.features.lockcontroller import (
    InvalidLockIdentifier,
    LockControllerBase,
    LockControllerFeature,
    LockServer_Responses,
    ServerAlreadyLocked,
    ServerNotLocked,
    UnlockServer_Responses,
)
from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import MetadataInterceptor, SilaServer


@dataclass
class Lock:
    token: str
    timeout_duration: timedelta
    last_usage: datetime = field(default_factory=lambda: datetime.now())

    @property
    def is_expired(self):
        return (datetime.now() - self.timeout_duration) > self.last_usage


class LockControllerImpl(LockControllerBase):
    def __init__(self, parent_server: SilaServer):
        self.parent_server = parent_server
        self.lock: Optional[Lock] = None
        self.parent_server.add_metadata_interceptor(LockControllerInterceptor(self))

    @property
    def is_locked(self) -> bool:
        if self.lock is None:
            return False

        if self.lock.is_expired:
            self.lock = None

        return self.lock is not None

    def get_IsLocked(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> bool:
        return self.is_locked

    def LockServer(
        self, LockIdentifier: str, Timeout: int, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> LockServer_Responses:
        if self.is_locked:
            raise ServerAlreadyLocked

        self.lock = Lock(LockIdentifier, timedelta(seconds=Timeout))

    def UnlockServer(
        self, LockIdentifier: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> UnlockServer_Responses:
        if not self.is_locked:
            raise ServerNotLocked

        if self.lock.token != LockIdentifier:
            raise InvalidLockIdentifier

        self.lock = None

    def get_calls_affected_by_LockIdentifier(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        if not self.is_locked:
            return []

        # lock all other features
        result = []
        for feature in self.parent_server.features.values():
            if feature._identifier not in ["SiLAService", "LockController"]:
                result.append(feature)
        return result


class LockControllerInterceptor(MetadataInterceptor):
    def __init__(self, lockcontroller_impl: LockControllerImpl):
        self.lockidentifier_fqi = LockControllerFeature["LockIdentifier"].fully_qualified_identifier
        super().__init__([self.lockidentifier_fqi])
        self.lockcontroller_impl = lockcontroller_impl

    def intercept(
        self, parameters: Any, metadata: Dict[FullyQualifiedIdentifier, Any], target_call: FullyQualifiedIdentifier
    ) -> None:
        token: str = metadata.pop(self.lockidentifier_fqi)
        if token != self.lockcontroller_impl.lock.token:
            raise InvalidLockIdentifier
