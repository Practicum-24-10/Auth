from http import HTTPStatus
from tests.functional.testdata.users import user_agent
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "logout_all": True,
                },
                {
                    "status": HTTPStatus.UNAUTHORIZED,
                    "body": {
                        "message": "Access denied. Token has been revoked."},
                },
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "logout_all": False,
                },
                {"status": HTTPStatus.OK, "body": {"message": "Refresh ok"}},
        ),
    ],
)
@pytestmark
async def test_logout_all_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"
    request_url_logout = "/auth/logout"
    request_url_refresh = "/auth/refresh"
    test_headers = {"User-Agent": user_agent}
    login_data = query_data["login"]
    body_logout = {"logout_all": query_data["logout_all"],
                   "refresh_token": None}
    body_refresh = {"force": False}

    # Act
    first_device = await make_post_request(request_url_login, login_data)
    second_device = await make_post_request(
        request_url_login, params=login_data, headers=test_headers
    )
    first_access = first_device["body"]["access_token"]
    first_refresh = first_device["body"]["refresh_token"]
    second_refresh = second_device["body"]["refresh_token"]
    headers_first = {
        "Authorization": f"Bearer {first_access}",
        "Content-Type": "application/json",
    }
    body_logout["refresh_token"] = first_refresh

    _ = await make_post_request(request_url_logout, params=body_logout,
                                headers=headers_first)
    headers_second = {
        "Authorization": f"Bearer {second_refresh}",
        "Content-Type": "application/json",
        "User-Agent": user_agent,
    }

    response = await make_post_request(request_url_refresh,
                                       params=body_refresh,
                                       headers=headers_second)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    if response["body"]["message"] == "Refresh ok":
        assert response["body"]["access_token"]
        assert response["body"]["refresh_token"]
