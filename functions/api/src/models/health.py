from pydantic import BaseModel


class HealthDto(BaseModel):
    """
    The health data transfer object.
    """

    healthy: bool
