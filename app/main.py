from fastapi import FastAPI, HTTPException

from app.models import TokenRequest, ServiceDurationRequest
from app.calculator import calculate_wait_time
from app import services


app = FastAPI(
    title="SlotSnap",
    description="Smart Token Wait-Time Estimator",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Welcome to SlotSnap!",
        "status": "Application is running"
    }


@app.get("/current-token")
def get_current_token():

    return {
        "current_token": services.current_served_token
    }


@app.put("/update-token/{new_token}")
def update_current_token(new_token: int):

    if new_token <= 0:
        raise HTTPException(
            status_code=400,
            detail="Token number must be greater than zero"
        )

    if new_token <= services.current_served_token:
        raise HTTPException(
            status_code=400,
            detail="New token must be greater than current token"
        )

    services.current_served_token = new_token

    return {
        "message": "Current token updated successfully",
        "current_token": services.current_served_token
    }


@app.post("/service-duration")
def record_service_duration(request: ServiceDurationRequest):

    services.service_durations.append(request.duration)

    return {
        "message": "Service duration recorded successfully",
        "recorded_duration": request.duration,
        "total_records": len(services.service_durations)
    }


@app.get("/average-service-time")
def get_average_service_time():

    if len(services.service_durations) == 0:
        raise HTTPException(
            status_code=404,
            detail="No service duration records available"
        )

    total_time = sum(services.service_durations)

    total_customers = len(services.service_durations)

    average_time = total_time / total_customers

    return {
        "total_customers": total_customers,
        "average_service_time": round(average_time, 2)
    }
@app.post("/skip-token/{token_number}")
def skip_token(token_number: int):

    if token_number <= services.current_served_token:
        raise HTTPException(
            status_code=400,
            detail="Cannot skip a token that has already been served"
        )

    if token_number in services.skipped_tokens:
        raise HTTPException(
            status_code=400,
            detail="This token has already been skipped"
        )

    services.skipped_tokens.append(token_number)

    return {
        "message": "Token skipped successfully",
        "skipped_token": token_number,
        "all_skipped_tokens": services.skipped_tokens
    }


@app.post("/estimate")
def estimate_wait_time(request: TokenRequest):

    if request.target_token <= services.current_served_token:
        raise HTTPException(
            status_code=400,
            detail="Target token must be greater than current token"
        )

    if services.service_durations:

        average_time = (
            sum(services.service_durations)
            / len(services.service_durations)
        )

        average_source = "Historical service durations"

    elif request.average_service_time is not None:

        average_time = request.average_service_time

        average_source = "Manually provided average"

    else:

        raise HTTPException(
            status_code=400,
            detail="No historical data available. Please provide average_service_time."
        )

    estimated_wait = calculate_wait_time(
        services.current_served_token,
        request.target_token,
        average_time,
        services.skipped_tokens
    )

    return {
        "current_token": services.current_served_token,
        "target_token": request.target_token,
        "average_service_time": round(average_time, 2),
        "average_source": average_source,
        "skipped_tokens": services.skipped_tokens,
        "estimated_wait_minutes": round(estimated_wait, 2)
    }