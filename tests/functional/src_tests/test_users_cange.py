from http import HTTPStatus

import pytest


# @pytest.mark.parametrize(
#     "query_data, expected_answer",
#     [
#         (
#                 {'username': 'user13', 'password': '234'},
#                 {"status": HTTPStatus.OK,
#                  "body": {
#                      "message": "New account was registered successfully"}},
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_add_user(
#         make_post_request, make_delete_request, query_data, expected_answer
# ):
#     response = await make_post_request("/auth/signup", query_data)
#     assert response["status"] == expected_answer["status"]
#     assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {'login': {'username': 'usertest', 'password': '2wewew34'},
                 'change': {'username': 'usertest'}},
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {
                     "message": "This login already exists"}},
        ),
        (
                {'login': {'username': 'usertest', 'password': '2wewew34'},
                 'change': {}},
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {
                     "message": "No change"}},
        ),
        (
                {'login': {'username': 'usertest', 'password': '2wewew34'},
                 'change': {'password': '1'}},
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {
                     "message": "Validation Error"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_bad_change(
        make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data['login'])
    access_token = response["body"]['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = await make_post_request("/auth/change",
                                       params=query_data['change'],
                                       headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {'login': {'username': 'usertest', 'password': '2wewew34'},
                 'change': {'username': 'new_user_test', 'password': None}},
                {"status": HTTPStatus.OK,
                 "body": {
                     "message": "Change ok"}},
        ),
        (
                {'login': {'username': 'usertest', 'password': '2wewew34'},
                 'change': {'username': None, 'password': 'erwqtyurew'}},
                {"status": HTTPStatus.OK,
                 "body": {
                     "message": "Change ok"}},
        ),
        (
                {'login': {'username': 'usertest', 'password': '2wewew34'},
                 'change': {'username': 'new_user_test',
                            'password': 'erwqtyurew'}},
                {"status": HTTPStatus.OK,
                 "body": {
                     "message": "Change ok"}},
        )
    ],
)
@pytest.mark.asyncio
async def test_ok_change(
        make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data['login'])
    access_token = response["body"]['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = await make_post_request("/auth/change",
                                       params=query_data['change'],
                                       headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
    new_login_data = query_data['login'].copy()
    new_change_data = {}
    for key, value in query_data['change'].items():
        if value is not None:
            new_login_data[key] = value
            new_change_data[key] = query_data['login'][key]
        else:
            new_change_data[key] = None
    response = await make_post_request("/auth/login", new_login_data)
    access_token = response["body"]['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = await make_post_request("/auth/change",
                                       params=new_change_data,
                                       headers=headers)
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
