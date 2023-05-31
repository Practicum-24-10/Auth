from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "usertest", "password": "2wewew34"},
            {"status": HTTPStatus.OK, "body": {"message": "Logout ok"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_logout_user(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data)
    access_token = response["body"]["access_token"]
    refresh_token = response["body"]["refresh_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body = {"logout_all": False, "refresh_token": refresh_token}
    response = await make_post_request("/auth/logout", params=body, headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
    headers = {
        "Authorization": f"Bearer {refresh_token}",
        "Content-Type": "application/json",
    }
    body = {"force": False}
    response = await make_post_request("/auth/refresh", params=body, headers=headers)
    assert response["status"] == HTTPStatus.UNAUTHORIZED
    assert response["body"] == {"message": "Access denied. Token has been revoked."}


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
@pytest.mark.asyncio
async def test_logout_user_bad_refresh_token(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body = {"logout_all": False, "refresh_token": "refresh_token"}
    response = await make_post_request("/auth/logout", params=body, headers=headers)
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
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
        ),
        (
            {
                "login": {"username": "usertest", "password": "2wewew34"},
                "body": {"refresh_token": "refresh_token"},
            },
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_logout_validation(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data["login"])
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(
        "/auth/logout", params=query_data["body"], headers=headers
    )
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
