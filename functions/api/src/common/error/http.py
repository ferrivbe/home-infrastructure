from http import HTTPStatus

from fastapi import HTTPException


class HTTPError(HTTPException):
    """
    The custom HTTP error exception extension.
    """

    def __init__(
        self, http_status: int, error_code: str, message: str, detail: any = None
    ):
        """
        Creates a new instance of HTTPError with custom parameters.

        :param http_status: The HTTP status for the response.
        :param error_code: The error code.
        :param message: The error message.
        :param detail: The error detail.
        """
        self.http_status = http_status
        self.error_code = error_code
        self.message = message
        self.detail = detail

        super().__init__(self.http_status, self.detail)


class HTTPNotFoundError(HTTPException):
    """
    The custom HTTP error exception not found extension.
    """

    def __init__(self, error_code: str, message: str, detail: any = None):
        """
        Creates a new instance of HTTPError with custom parameters.

        :param error_code: The error code.
        :param message: The error message.
        :param detail: The error detail.
        """
        self.http_status = HTTPStatus.NOT_FOUND
        self.error_code = error_code
        self.message = message
        self.detail = detail

        super().__init__(self.http_status, self.detail)


class HTTPUnprocessableEntityError(HTTPException):
    """
    The custom HTTP error exception unprocesable entity extension.
    """

    def __init__(self, error_code: str, message: str, detail: any = None):
        """
        Creates a new instance of HTTPError with custom parameters.

        :param error_code: The error code.
        :param message: The error message.
        :param detail: The error detail.
        """
        self.http_status = HTTPStatus.UNPROCESSABLE_ENTITY
        self.error_code = error_code
        self.message = message
        self.detail = detail

        super().__init__(self.http_status, self.detail)


class HTTPInternalServerError(HTTPException):
    """
    The custom HTTP error exception internal server extension.
    """

    def __init__(self, error_code: str, message: str, detail: any = None):
        """
        Creates a new instance of HTTPError with custom parameters.

        :param error_code: The error code.
        :param message: The error message.
        :param detail: The error detail.
        """
        self.http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        self.error_code = error_code
        self.message = message
        self.detail = detail

        super().__init__(self.http_status, self.detail)
