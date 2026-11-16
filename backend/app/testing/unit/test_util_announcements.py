import pytest

from datetime import datetime, timedelta, timezone
from app.core.timezone import LOCAL_TZ

from app.utils.util_announcements import *


@pytest.mark.parametrize(
    "expiration_date, expiration_time, expected_expires_at",
    [
        (
            "12-20-2026",
            "9:00 PM",
            datetime(2026, 12, 20, 21, 0, 0, tzinfo=LOCAL_TZ),
        ),
        (
            "12-27-2026",
            "11:59 PM",
            datetime(2026, 12, 27, 23, 59, 0, tzinfo=LOCAL_TZ),
        ),
    ],
)
def test_format_expired_time(expiration_date, expiration_time, expected_expires_at):
    result = format_expired_time(expiration_date, expiration_time)

    assert (
        result == expected_expires_at
    ), f"Expected expiration datetime {expected_expires_at}, got {result}"


@pytest.mark.parametrize(
    "expiration_date, expiration_time",
    [
        # bad date input
        (
            "2026-12-20",
            "9:00 PM",
        ),
        # bad time input
        (
            "12-20-2026",
            "21:00",
        ),
    ],
)
def test_format_expired_time_bad_input(expiration_date, expiration_time):
    with pytest.raises(ValueError):
        format_expired_time(expiration_date, expiration_time)


@pytest.mark.parametrize(
    "offset, expected",
    [
        (timedelta(seconds=10), "just now"),
        (timedelta(minutes=1), "1 minute ago"),
        (timedelta(minutes=57), "57 minutes ago"),
        (timedelta(hours=1), "1 hour ago"),
        (timedelta(hours=17), "17 hours ago"),
        (timedelta(hours=36), "1 day ago"),
        (timedelta(days=1), "1 day ago"),
        (timedelta(days=6), "6 days ago"),
        (timedelta(weeks=1), "1 week ago"),
        (timedelta(weeks=2), "2 weeks ago"),
        (timedelta(days=36), "1 month ago"),
        (timedelta(days=100), "3 months ago"),
    ],
)
def test_get_relative_time(offset, expected):
    dt = datetime.now(timezone.utc) - offset
    result = get_relative_time(dt)

    assert result == expected, f"Expected '{expected}', got '{result}'"
