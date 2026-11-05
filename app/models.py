from pydantic import BaseModel, Field


class TokenRequest(BaseModel):

    target_token: int = Field(
        gt=0,
        description="Customer's token number"
    )

    average_service_time: float | None = Field(
        default=None,
        gt=0,
        description="Optional average service duration"
    )


class ServiceDurationRequest(BaseModel):

    duration: float = Field(
        gt=0,
        description="Time taken to serve the customer in minutes"
    )