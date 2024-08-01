from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class ProtocolTypeDto(Enum):
    """Enumeration for protocol types."""

    RTSP = "rtsp"


class NewSourceDto(BaseModel):
    """
    Model representing a source with various attributes.

    Attributes:
        name (str): Name of the source with a maximum length of 32 characters and specific regex pattern.
        description (Optional[str]): Description of the source with a maximum length of 128 characters and specific regex pattern. Can be null.
        address (str): IPv4 address of the source, validated by a specific regex pattern.
        port (int): Port number of the source, ranging from 1 to 65535.
        username (EmailStr): Email address used as the username for the source.
        password (str): Password for the source, validated by a regex pattern to include specific character requirements.
        protocol (ProtocolType): Protocol type used by the source.
    """

    name: str = Field(..., max_length=32, pattern=r"^[a-zA-Z0-9\s\-]+$")
    description: Optional[str] = Field(
        None, max_length=128, pattern=r"^[a-zA-Z0-9\s\-]+$"
    )
    address: str = Field(
        ...,
        pattern=r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
    )
    port: int = Field(..., ge=1, le=65535)
    username: EmailStr
    password: str = Field(..., min_length=8)
    protocol: ProtocolTypeDto

    @field_validator("password")
    def validate_password(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/`~" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class SourceDto(BaseModel):
    """
    Model representing a source with various attributes.

    Attributes:
        id (str): The source identifier.
        name (str): Name of the source with a maximum length of 32 characters and specific regex pattern.
        description (Optional[str]): Description of the source with a maximum length of 128 characters and specific regex pattern. Can be null.
        address (str): IPv4 address of the source, validated by a specific regex pattern.
        port (int): Port number of the source, ranging from 1 to 65535.
        username (EmailStr): Email address used as the username for the source.
        password (str): Password for the source, validated by a regex pattern to include specific character requirements.
        protocol (ProtocolType): Protocol type used by the source.
    """

    id: UUID
    name: str
    description: str = None
    address: str
    port: int
    username: str
    password: str
    protocol: ProtocolTypeDto
