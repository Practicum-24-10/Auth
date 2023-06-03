from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"username": "usertest", "password": "2wewew34"},
                {"status": HTTPStatus.OK,
                 "body": {"message": "Login history"}},
        ),
    ],
)
@pytestmark
async def test_login_user(
        make_post_request,
        make_get_request,
        make_delete_request,
        query_data,
        expected_answer,
):
    # Arrange
    request_url_login = "/auth/login"
    request_url_history = "/auth/history"
    params = {"size": 10, "page": 1}

    # Act
    response = await make_post_request(request_url_login, query_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = await make_get_request(request_url_history,
                                      headers=headers, params=params)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    assert len(response["body"]["history"]) >= 1
