from http import HTTPStatus

import pytest


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
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Wrong password"}},
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
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
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
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "No change"}},
        ),
        (
            {
                "login": {"username": "usertest", "password": "2wewew34"},
                "change": {"password": "1"},
            },
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_bad_change(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data["login"])
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = await make_post_request(
        "/auth/change", params=query_data["change"], headers=headers
    )
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
@pytest.mark.asyncio
async def test_ok_change(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data["login"])
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = await make_post_request(
        "/auth/change", params=query_data["change"], headers=headers
    )
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
    new_login_data = query_data["login"].copy()
    new_change_data = {}
    for key, value in query_data["change"].items():
        if value is not None:
            if key == "new_password":
                new_login_data["password"] = value
                new_change_data["new_password"] = query_data["login"]["password"]
            if key == "old_password":
                new_change_data["old_password"] = query_data["change"]["new_password"]
            if key == "username":
                new_change_data["username"] = query_data["login"]["username"]
                new_login_data["username"] = query_data["change"]["username"]
        else:
            new_change_data[key] = None
    response = await make_post_request("/auth/login", new_login_data)
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(
        "/auth/change", params=new_change_data, headers=headers
    )
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
    #
    # ```
    # import requests
    #
    # ACCESS_TOKEN = "valid_access_token"
    # REFRESH_TOKEN = "valid_refresh_token"
    #
    # headers = {
    #     "Authorization": f"Bearer {REFRESH_TOKEN}",
    #     "Content-Type": "application/json"
    # }
    #
    # response = requests.post("http://example.com/refresh", headers=headers)
    #
    # if response.status_code == requests.codes.ok:
    #     new_access_token = response.json()["access_token"]
    #     print(f"New access token: {new_access_token}")
    # else:
    #     print("Token refresh failed")
    # ```


#
# @pytest.mark.parametrize(
#     "query_data, expected_answer",
#     [
#         (
#                 {'username': 'user13', 'password': '234'},
#                 {"status": HTTPStatus.OK,
#                  "body": {"message": "Login ok"}},
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_login_user(
#         make_post_request, make_delete_request, query_data, expected_answer
# ):
#     response = await make_post_request("/auth/login", query_data)
#     assert response["status"] == expected_answer["status"]
#     assert response["body"] == expected_answer["body"]
