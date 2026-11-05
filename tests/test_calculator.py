from app.calculator import calculate_wait_time


def test_normal_wait_time():

    result = calculate_wait_time(10, 15, 6)

    assert result == 30


def test_wait_time_with_skipped_tokens():

    result = calculate_wait_time(
        10,
        15,
        6,
        [12, 13]
    )

    assert result == 18


def test_wait_time_without_skipped_tokens():

    result = calculate_wait_time(
        10,
        15,
        6,
        []
    )

    assert result == 30


def test_wait_time_with_one_skipped_token():

    result = calculate_wait_time(
        10,
        15,
        6,
        [12]
    )

    assert result == 24