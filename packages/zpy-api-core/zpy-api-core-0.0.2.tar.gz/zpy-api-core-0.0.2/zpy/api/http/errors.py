from typing import Optional, List

from zpy.api.http.status_codes import HttpStatus


class ZError(Exception):
    """Base Error

    Args:
        Exception ([type]): [description]
    """

    def __init__(
        self, message: str, reason: str, details: Optional[List[str]], *args: object
    ) -> None:
        super().__init__(*args)
        self.reason = reason
        self.message = message
        self.details = details

    def add_detail(self, message: str) -> None:
        if self.details is None:
            self.details = []
        self.details.append(message)


class ZHttpError(ZError):
    """Http Base Error

    Args:
        ZError ([type]): [description]
    """

    def __init__(
        self,
        message: str = None,
        reason: str = None,
        details: Optional[List[str]] = None,
        status: HttpStatus = HttpStatus.INTERNAL_SERVER_ERROR,
        *args: object
    ) -> None:
        super().__init__(message, reason, details, *args)
        self.status = status


class BadRequest(ZHttpError):
    """BadRequest

    Args:
        ZError ([type]): [description]
    """

    def __init__(
        self,
        message: str = None,
        reason: str = None,
        details: Optional[List[str]] = None,
        *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.BAD_REQUEST, *args)


class Unauthorized(ZHttpError):
    """Unauthorized

    Args:
        ZError ([type]): [description]
    """

    def __init__(
        self,
        message: str = None,
        reason: str = None,
        details: Optional[List[str]] = None,
        *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.UNAUTHORIZED, *args)


class NotFound(ZHttpError):
    """BadRequest

    Args:
        ZError ([type]): [description]
    """

    def __init__(
        self,
        message: str = None,
        reason: str = None,
        details: Optional[List[str]] = None,
        *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.NOT_FOUND, *args)
