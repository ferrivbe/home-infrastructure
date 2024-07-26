from pydantic import BaseModel


class HTTPErrorDto(BaseModel):
    """
    The error detail data transfer object.
    """

    error_code: str = "ExampleErrorCode"
    message: str = "This is a example message."
    detail: dict = {
        "property_a": "This is an example.",
    }
    target: str = "GET|https://example.com/users"
