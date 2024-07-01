from typing import Any

from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, detail: str = None, **kwargs: dict[str, Any]) -> None:
        if detail is None:
            detail = self.DETAIL
        super().__init__(status_code=self.STATUS_CODE, detail=detail, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class InstanceNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Instance not found"


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


