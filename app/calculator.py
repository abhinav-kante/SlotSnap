def calculate_wait_time(
    current_token: int,
    target_token: int,
    average_service_time: float,
    skipped_tokens: list[int] | None = None
) -> float:

    if skipped_tokens is None:
        skipped_tokens = []

    waiting_slots = target_token - current_token

    for token in skipped_tokens:

        if current_token <= token < target_token:
            waiting_slots -= 1

    estimated_wait = waiting_slots * average_service_time

    return estimated_wait