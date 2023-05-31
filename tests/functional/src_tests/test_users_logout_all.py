from http import HTTPStatus
from tests.functional.testdata.users import user_agent
import pytest


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
@pytest.mark.asyncio
async def test_logout_all_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    test_headers = {
        "User-Agent": user_agent
    }
    first_device = await make_post_request("/auth/login", query_data["login"])
    second_device = await make_post_request(
        "/auth/login", params=query_data["login"], headers=test_headers
    )
    first_access = first_device["body"]["access_token"]
    first_refresh = first_device["body"]["refresh_token"]
    second_refresh = second_device["body"]["refresh_token"]
    headers = {
        "Authorization": f"Bearer {first_access}",
        "Content-Type": "application/json",
    }
    body = {"logout_all": query_data["logout_all"],
            "refresh_token": first_refresh}

    response = await make_post_request("/auth/logout", params=body,
                                       headers=headers)
    assert response["status"] == HTTPStatus.OK
    assert response["body"] == {"message": "Logout ok"}
    # for access, refresh in many_tokens:
    headers = {
        "Authorization": f"Bearer {second_refresh}",
        "Content-Type": "application/json",
        "User-Agent": user_agent,
    }
    body = {"force": False}
    response = await make_post_request("/auth/refresh", params=body,
                                       headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    if response["body"]["message"] == "Refresh ok":
        assert response["body"]["access_token"]
        assert response["body"]["refresh_token"]
