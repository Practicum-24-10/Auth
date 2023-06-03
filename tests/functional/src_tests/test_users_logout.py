from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"username": "usertest", "password": "2wewew34"},
                {"status": HTTPStatus.OK, "body": {"message": "Logout ok"}},
        ),
    ],
)
@pytestmark
async def test_logout_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    body = {"logout_all": False, "refresh_token": None}
    request_url_login = "/auth/login"
    request_url_logout = "/auth/logout"

    # Act
    response = await make_post_request(request_url_login, query_data)
    access_token = response["body"]["access_token"]
    refresh_token = response["body"]["refresh_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body["refresh_token"] = refresh_token
    response = await make_post_request(request_url_logout, params=body,
                                       headers=headers)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"username": "usertest", "password": "2wewew34"},
                {"status": HTTPStatus.UNAUTHORIZED, "body": {
                    "message": "Access denied. Token has been revoked."}},
        ),
    ],
)
@pytestmark
async def test_refresh_after_logout_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    body_logout = {"logout_all": False, "refresh_token": None}
    body_refresh = {"force": False}
    request_url_login = "/auth/login"
    request_url_logout = "/auth/logout"
    request_url_refresh = "/auth/refresh"

    # Act
    response = await make_post_request(request_url_login, query_data)
    access_token = response["body"]["access_token"]
    refresh_token = response["body"]["refresh_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body_logout["refresh_token"] = refresh_token
    _ = await make_post_request(request_url_logout, params=body_logout,
                                headers=headers)
    headers = {
        "Authorization": f"Bearer {refresh_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(request_url_refresh,
                                       params=body_refresh, headers=headers)

    # Assert
    assert response["status"] == HTTPStatus.UNAUTHORIZED
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"username": "usertest", "password": "2wewew34"},
                {
                    "status": HTTPStatus.BAD_REQUEST,
                    "body": {"message": "Bad refresh token"},
                },
        ),
    ],
)
@pytestmark
async def test_logout_user_bad_refresh_token(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"
    request_url_logout = "/auth/logout"
    body = {"logout_all": False, "refresh_token": "refresh_token"}

    # Act
    response = await make_post_request(request_url_login, query_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = await make_post_request(request_url_logout, params=body,
                                       headers=headers)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "body": {"logout_all": False},
                },
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "body": {"refresh_token": "refresh_token"},
                },
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
        ),
    ],
)
@pytestmark
async def test_logout_validation(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"
    request_url_logout = "/auth/logout"
    login_data = query_data["login"]
    body_logout = query_data["body"]

    # Act
    response = await make_post_request(request_url_login, login_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(
        request_url_logout, params=body_logout, headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
