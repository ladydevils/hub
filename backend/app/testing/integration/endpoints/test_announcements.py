from fastapi import status
from app.routers.announcements import *


def create_sample_announcement(db_session):
    announcement = AnnouncementCreate(
        content="Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        expiration_date="01-04-2027",
        expiration_time="11:59 PM",
        pinned=False,
    )

    result = create_announcement(announcement, db_session)
    return result


def test_create_announcement_endpoint(client):
    payload = {
        "content": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "expiration_date": "01-04-2027",
        "expiration_time": "11:59 PM",
        "pinned": False,
    }

    response = client.post("/announcements/", json=payload)

    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f"Unsuccessful request: {response.status_code}"

    # assert isinstance(response.json()["id"], int)


def test_get_announcements_endpoint(client, db_session):
    new_announcement = create_sample_announcement(db_session)
    response = client.get("/announcements/")

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unsuccessful request: {response.status_code}"

    ids = [item["id"] for item in response.json()]
    assert new_announcement.id in ids, f"Announcement ID should be in the response IDs"


def test_get_announcement_form_response_endpoint(client, db_session):
    new_announcement = create_sample_announcement(db_session)
    response = client.get(f"/announcements/{new_announcement.id}")

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unsuccessful request: {response.status_code}"

    assert response.json()["id"] == new_announcement.id


def test_get_announcement_form_response_endpoint_not_found(client):
    announcement_id = -1
    response = client.get(f"/announcements/{announcement_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_announcement_endpoint(client, db_session):
    original_announcement = create_sample_announcement(db_session)

    payload = {
        "content": "UPDATED CONTENT",
        "expiration_date": "02-01-2027",
        "expiration_time": "10:00 AM",
        "pinned": True,
    }

    response = client.patch(f"/announcements/{original_announcement.id}", json=payload)
    updated_announcement = db_session.scalar(
        select(Announcement).where(Announcement.id == original_announcement.id)
    )

    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unsuccessful request: {response.status_code}"

    assert (
        updated_announcement.content == "UPDATED CONTENT"
    ), f"Updated announcement should have the new content"


def test_update_pin_endpoint(client, db_session):
    original_announcement = create_sample_announcement(db_session)

    payload = {"pinned": True}

    response = client.patch(
        f"/announcements/{original_announcement.id}/pin", json=payload
    )
    updated_announcement = db_session.scalar(
        select(Announcement).where(Announcement.id == original_announcement.id)
    )

    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unsuccessful request: {response.status_code}"

    assert updated_announcement.pinned is True, f"Announcement should now be pinned"


def test_remove_announcement_endpoint(client, db_session):
    original_announcement = create_sample_announcement(db_session)

    response = client.patch(f"/announcements/{original_announcement.id}/remove")
    updated_announcement = db_session.scalar(
        select(Announcement).where(Announcement.id == original_announcement.id)
    )

    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unsuccessful request: {response.status_code}"

    assert updated_announcement.expires_at < datetime.now(
        timezone.utc
    ), f"Removed announcement should have an expiration time in the past"
