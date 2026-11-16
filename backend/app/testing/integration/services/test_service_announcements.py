import pytest

from datetime import datetime
from app.core.timezone import LOCAL_TZ

from app.models.announcement import Announcement
from app.routers.announcements import AnnouncementCreate, PinUpdate

from app.utils.util_announcements import format_expired_time
from app.services.service_announcements import *


@pytest.mark.parametrize(
    "content, expiration_date, expiration_time, pinned",
    [
        (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "12-22-2026",
            "09:00 PM",
            False,
        ),
        (
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "01-04-2027",
            "11:59 PM",
            True,
        ),
    ],
)
def test_create_announcement(
    content, expiration_date, expiration_time, pinned, db_session: Session
):
    announcement = AnnouncementCreate(
        content=content,
        expiration_date=expiration_date,
        expiration_time=expiration_time,
        pinned=pinned,
    )

    result = create_announcement(announcement, db_session)

    new_announcement = db_session.scalar(
        select(Announcement).where(Announcement.id == result.id)
    )

    assert new_announcement is not None, f"Announcement must be Announcements table"


@pytest.mark.parametrize(
    "content, expiration_date, expiration_time, pinned",
    [
        (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "bad date",
            "09:00 PM",
            False,
        ),
        (
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "01-04-2027",
            "bad time",
            True,
        ),
    ],
)
def test_create_announcement_bad_input(
    content, expiration_date, expiration_time, pinned, db_session: Session
):
    announcement = AnnouncementCreate(
        content=content,
        expiration_date=expiration_date,
        expiration_time=expiration_time,
        pinned=pinned,
    )

    with pytest.raises(HTTPException) as e:
        create_announcement(announcement, db_session)

    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_get_announcements(db_session: Session):
    announcement1 = AnnouncementCreate(
        content="announcement example 1",
        expiration_date="12-31-2030",
        expiration_time="10:00 PM",
        pinned=False,
    )
    announcement2 = AnnouncementCreate(
        content="announcement example 2",
        expiration_date="11-30-2030",
        expiration_time="05:00 PM",
        pinned=True,
    )
    announcement3 = AnnouncementCreate(
        content="announcement example 3",
        expiration_date="12-20-2030",
        expiration_time="11:59 PM",
        pinned=False,
    )
    announcement4 = AnnouncementCreate(
        content="announcement example 4",
        expiration_date="12-28-2030",
        expiration_time="03:00 PM",
        pinned=True,
    )

    expected_ids = []

    for i, announcement in enumerate(
        [announcement1, announcement2, announcement3, announcement4]
    ):
        a = create_announcement(announcement, db_session)
        a.created_time = datetime.now(
            timezone.utc
        )  # updating create_time so that all announcements don't have the same time from being in the same db session
        db_session.commit()
        expected_ids.append(a.id)

    results = get_announcements(db_session)
    result_ids = [result["id"] for result in results]
    expected_ids.reverse()

    assert (
        result_ids == expected_ids
    ), f"Must retrieval pinned announcements first and announcements must be sorted by creation time"


@pytest.mark.parametrize(
    "content, expiration_date, expiration_time, pinned",
    [
        (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "12-22-2026",
            "09:00 PM",
            False,
        ),
    ],
)
def test_get_announcement_form_response(
    content, expiration_date, expiration_time, pinned, db_session: Session
):
    announcement = AnnouncementCreate(
        content=content,
        expiration_date=expiration_date,
        expiration_time=expiration_time,
        pinned=pinned,
    )

    created_announcement = create_announcement(announcement, db_session)

    results = get_announcement_form_response(
        created_announcement.id, db_session
    )  # converts data from db back format for client
    assert (
        results["expiration_date"] == expiration_date
    ), f"Expected {expiration_date}, got {results["expiration_date"] }"
    assert (
        results["expiration_time"] == expiration_time
    ), f"Expected {expiration_time}, got {results["expiration_time"] }"


def test_get_announcement_form_response_not_found(db_session: Session):
    with pytest.raises(HTTPException) as e:
        get_announcement_form_response(9999, db_session)

    assert e.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "content, expiration_date, expiration_time, pinned, updated_content, updated_expiration_date, updated_expiration_time, updated_pinned",
    [
        (
            # creation values
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "12-22-2026",
            "09:00 PM",
            False,
            # updated values
            "Work, work, work, work, work, work. He said me haffi. Work, work, work, work, work, work. He see me do mi. Dirt, dirt, dirt, dirt, dirt, dirt. So me put in.Work, work, work, work, work, work.",
            "12-22-2026",
            "09:00 PM",
            False,
        ),
        (
            # creation values
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "01-04-2027",
            "11:59 PM",
            False,
            # updated values
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "01-01-2027",
            "10:00 AM",
            False,
        ),
        (
            # creation values
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "12-30-2026",
            "11:59 PM",
            False,
            # updated values
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "12-30-2026",
            "11:59 PM",
            True,
        ),
        (
            # creation values
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "12-30-2026",
            "11:59 PM",
            True,
            # updated values
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "01-01-2027",
            "11:59 PM",
            False,
        ),
    ],
)
def test_update_announcement(
    content,
    expiration_date,
    expiration_time,
    pinned,
    updated_content,
    updated_expiration_date,
    updated_expiration_time,
    updated_pinned,
    db_session: Session,
):
    announcement = AnnouncementCreate(
        content=content,
        expiration_date=expiration_date,
        expiration_time=expiration_time,
        pinned=pinned,
    )

    updated_announcement_data = AnnouncementCreate(
        content=updated_content,
        expiration_date=updated_expiration_date,
        expiration_time=updated_expiration_time,
        pinned=updated_pinned,
    )

    created_announcement = create_announcement(announcement, db_session)
    update_announcement(created_announcement.id, updated_announcement_data, db_session)
    updated_announcement = db_session.scalar(
        select(Announcement).where(Announcement.id == created_announcement.id)
    )

    expected_expires_at = format_expired_time(
        updated_announcement_data.expiration_date,
        updated_announcement_data.expiration_time,
    )

    assert (
        updated_announcement.content == updated_announcement_data.content
    ), f"Updated announcement content should be {updated_announcement_data.content}, got {updated_announcement.content}"

    assert (
        updated_announcement.expires_at == expected_expires_at
    ), f"Updated announcement expiration datetime should be {expected_expires_at}, got {updated_announcement.expires_at}"

    assert (
        updated_announcement.pinned == updated_announcement_data.pinned
    ), f"Updated announcement pinned should be {updated_announcement_data.pinned}, got {updated_announcement.pinned}"


@pytest.mark.parametrize(
    "content, expiration_date, expiration_time, pinned, updated_pinned",
    [
        (
            # creation values
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "12-22-2026",
            "09:00 PM",
            False,
            # updated value
            True,
        ),
        (
            # creation values
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "01-04-2027",
            "11:59 PM",
            True,
            # updated value
            False,
        ),
    ],
)
def test_update_pin(
    content,
    expiration_date,
    expiration_time,
    pinned,
    updated_pinned,
    db_session: Session,
):
    announcement = AnnouncementCreate(
        content=content,
        expiration_date=expiration_date,
        expiration_time=expiration_time,
        pinned=pinned,
    )

    pin = PinUpdate(pinned=updated_pinned)

    created_announcement = create_announcement(announcement, db_session)
    update_pin(created_announcement.id, pin, db_session)
    updated_announcement = db_session.scalar(
        select(Announcement).where(Announcement.id == created_announcement.id)
    )

    assert (
        updated_announcement.pinned == updated_pinned
    ), f"Expected pinned={updated_pinned}, got {updated_announcement.pinned}"

    assert (
        updated_announcement.content == content
    ), "update_pin should not modify the announcement's content"

    assert updated_announcement.expires_at == format_expired_time(
        expiration_date, expiration_time
    ), "update_pin should not modify the announcement's content"


def test_remove_announcement(db_session):
    announcement = AnnouncementCreate(
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        expiration_date="12-22-2026",
        expiration_time="09:00 PM",
        pinned=False,
    )

    created_announcement = create_announcement(announcement, db_session)
    remove_announcement(created_announcement.id, db_session)

    now = datetime.now(timezone.utc)

    removed_announcement = db_session.scalar(
        select(Announcement).where(
            Announcement.id == created_announcement.id,
            Announcement.expires_at > now,
        )
    )

    assert (
        removed_announcement is None
    ), "Removed announcement should not match query for expiration datetime > now"
