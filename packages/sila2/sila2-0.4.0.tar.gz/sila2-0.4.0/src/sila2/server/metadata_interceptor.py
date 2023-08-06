from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable

from sila2.framework.fully_qualified_identifier import FullyQualifiedIdentifier


class MetadataInterceptor(ABC):
    def __init__(self, required_metadata: Iterable[FullyQualifiedIdentifier]) -> None:
        self.required_metadata = frozenset(required_metadata)

    @abstractmethod
    def intercept(
        self, parameters: Any, metadata: Dict[FullyQualifiedIdentifier, Any], target_call: FullyQualifiedIdentifier
    ) -> None:
        pass
