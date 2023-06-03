from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": "usertest",
                        "new_password": "usertest",
                        "old_password": "2wewew33",
                    },
                },
                {
                    "status": HTTPStatus.BAD_REQUEST,
                    "body": {"message": "This login already exists"},
                },
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": None,
                        "new_password": "usertest",
                        "old_password": "2wewew33",
                    },
                },
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Wrong password"}},
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": None,
                        "new_password": None,
                        "old_password": "2wewew33",
                    },
                },
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": None,
                        "new_password": None,
                        "old_password": None,
                    },
                },
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "No change"}},
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {"password": "1"},
                },
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
        ),
    ],
)
@pytestmark
async def test_bad_change(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"
    request_url_change = "/auth/change"
    login_data = query_data["login"]
    change_data = query_data["change"]

    # Act
    response = await make_post_request(request_url_login, login_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = await make_post_request(
        request_url_change, params=change_data, headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": "new_user_test",
                        "old_password": None,
                        "new_password": None,
                    },
                },
                {"status": HTTPStatus.OK, "body": {"message": "Change ok"}},
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": None,
                        "new_password": "erwqtyurew",
                        "old_password": "2wewew34",
                    },
                },
                {"status": HTTPStatus.OK, "body": {"message": "Change ok"}},
        ),
        (
                {
                    "login": {"username": "usertest", "password": "2wewew34"},
                    "change": {
                        "username": "new_user_test",
                        "new_password": "erwqtyurew",
                        "old_password": "2wewew34",
                    },
                },
                {"status": HTTPStatus.OK, "body": {"message": "Change ok"}},
        ),
    ],
)
@pytestmark
async def test_ok_change(
        make_post_request, make_delete_request, query_data, expected_answer
):
    def get_swipe_data(login: dict, change: dict):
        new_login = login.copy()
        new_change = {}
        for key, value in change.items():
            if value is not None:
                if key == "new_password":
                    new_login["password"] = value
                    new_change["new_password"] = login[
                        "password"]
                if key == "old_password":
                    new_change["old_password"] = change[
                        "new_password"]
                if key == "username":
                    new_change["username"] = login[
                        "username"]
                    new_login["username"] = change[
                        "username"]
            else:
                new_change[key] = None
        return new_login, new_change

    # Arrange
    request_url_login = "/auth/login"
    request_url_change = "/auth/change"
    login_data = query_data["login"]
    change_data = query_data["change"]
    new_login_data, new_change_data = get_swipe_data(login_data,
                                                     change_data)

    # Act
    response = await make_post_request(request_url_login, login_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    _ = await make_post_request(
        request_url_change, params=change_data, headers=headers
    )
    response = await make_post_request(request_url_login, new_login_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(
        request_url_change, params=new_change_data, headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
