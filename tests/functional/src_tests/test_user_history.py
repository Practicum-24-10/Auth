from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "usertest", "password": "2wewew34"},
            {"status": HTTPStatus.OK, "body": {"message": "Login history"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_login_user(
    make_post_request,
    make_get_request,
    make_delete_request,
    query_data,
    expected_answer,
):
    response = await make_post_request("/auth/login", query_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_get_request("/auth/history", headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    assert len(response["body"]["history"]) >= 1
