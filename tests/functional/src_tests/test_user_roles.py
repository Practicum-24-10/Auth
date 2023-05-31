from http import HTTPStatus

import pytest

from tests.functional.testdata.roles import roles
from tests.functional.testdata.users import user

user_id = user[0]["id"]
role_name = roles[0]["name"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": role_name},
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_user_role(make_post_request, query_data, expected_answer):
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(
        f"/users/{user_id}/AddRole", query_data, headers=headers
    )
    assert response["status"] == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": role_name},
            {"status": HTTPStatus.ACCEPTED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_user_role(
    make_delete_request, make_post_request, query_data, expected_answer
):
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_delete_request(
        f"/users/{user_id}/DeleteRole", query_data, headers=headers
    )
    assert response["status"] == expected_answer["status"]
