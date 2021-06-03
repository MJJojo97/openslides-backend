from typing import Protocol

from ...services.auth.interface import AuthenticationService
from ...services.datastore.interface import DatastoreService
from ...services.media.interface import MediaService


class Services(Protocol):  # pragma: no cover
    """
    Interface for service container used for dependency injection.
    """

    def authentication(self) -> AuthenticationService:
        pass

    def datastore(self) -> DatastoreService:
        pass

    def media(self) -> MediaService:
        pass
