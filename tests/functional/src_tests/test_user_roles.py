from http import HTTPStatus

import pytest

from tests.functional.testdata.perm_role_user import roles
from tests.functional.testdata.users import user

pytestmark = pytest.mark.asyncio

user_id = user[0]["id"]
role_id = roles[2]["id"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"id": role_id},
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
@pytestmark
async def test_add_user_role(make_post_request, query_data, expected_answer):
    # Arrange
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_post_request(
        f"/users/{user_id}/AddRole", query_data, headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"id": role_id},
            {"status": HTTPStatus.ACCEPTED},
        ),
    ],
)
@pytestmark
async def test_delete_user_role(
    make_delete_request, make_post_request, query_data, expected_answer
):
    # Arrange
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_delete_request(
        f"/users/{user_id}/DeleteRole", query_data, headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]
