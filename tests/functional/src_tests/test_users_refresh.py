from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "usertest", "password": "2wewew34"},
            {"status": HTTPStatus.OK, "body": {"message": "Refresh ok"}},
        )
    ],
)
@pytestmark
async def test_refresh(
    make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"
    body = {"force": False}
    request_url_refresh = "/auth/refresh"

    # Act
    response = await make_post_request(request_url_login, query_data)
    refresh_token = response["body"]["refresh_token"]
    headers = {
        "Authorization": f"Bearer {refresh_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(request_url_refresh, params=body,
                                       headers=headers)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    assert response["body"]["access_token"]
    assert response["body"]["refresh_token"]
