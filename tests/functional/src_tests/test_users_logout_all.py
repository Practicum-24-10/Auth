from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {'username': 'usertest', 'password': '2wewew34'},
                {"status": HTTPStatus.OK,
                 "body": {
                     "message": "Logout ok"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_logout_all_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data)
    access_token = response["body"]['access_token']
    refresh_token = response["body"]['refresh_token']
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {'logout_all': True,
            'refresh_token': refresh_token}
    many_tokens = []
    for task in range(5):
        test_response = await make_post_request("/auth/login", query_data)
        many_tokens.append((test_response["body"]['access_token'],
                            test_response["body"]['refresh_token']))

    response = await make_post_request("/auth/logout", params=body,
                                       headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
    for access, refresh in many_tokens:
        headers = {
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/json"
        }
        body = {'logout_all': False,
                'refresh_token': refresh}
        response = await make_post_request("/auth/logout", params=body,
                                           headers=headers)
        assert response["status"] == HTTPStatus.UNAUTHORIZED
        assert response["body"]['message'] == 'Access denied. Token has been revoked.'

#
# @pytest.mark.parametrize(
#     "query_data, expected_answer",
#     [
#         (
#                 {'logout_all': True,
#                  'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTE4MDMzOCwianRpIjoiNmYyYmQ0ZTctMDJkOS00MTU0LTlkMjktNjVkNjY3ZGM4MzQwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJlOTQ3MDk2Ni0yY2Y3LTQ4NzctYjY0ZC03Nzc2NGVmZTkwYzkiLCJuYmYiOjE2ODUxODAzMzgsImV4cCI6MTY4Nzc3MjMzOCwicGVybWlzc2lvbnMiOlsidnVwIiwidmlwIl0sImlzX3N1cGVydXNlciI6ZmFsc2UsInByX3V1aWQiOiIzOTBlZTY1MC05ZjhiLTQzZjAtOWU3Ny1lNTZmNWFjNDJlODcifQ.D3NFDFFxdAvhRgcJO9os5UfqWtR3Y5_b_9I-u-cHMzY'},
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
#     headers = {
#         "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTE4MDMzOCwianRpIjoiMTExMWUzZjUtMjU0Yy00NDY3LWExNGEtOWVjZjMzMzA2MmU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU5NDcwOTY2LTJjZjctNDg3Ny1iNjRkLTc3NzY0ZWZlOTBjOSIsIm5iZiI6MTY4NTE4MDMzOCwiZXhwIjoxNjg1MTgzOTM4LCJwZXJtaXNzaW9ucyI6WyJ2dXAiLCJ2aXAiXSwiaXNfc3VwZXJ1c2VyIjpmYWxzZSwicHJfdXVpZCI6IjM5MGVlNjUwLTlmOGItNDNmMC05ZTc3LWU1NmY1YWM0MmU4NyJ9.O80GLg9WnoPV1LVq2I0A3wKABOOj5BKvJuzThezS_cE",
#         "Content-Type": "application/json"
#     }
#     response = await make_post_request("/auth/logout", params=query_data,
#                                        headers=headers)
#     assert response["status"] == expected_answer["status"]
#     assert response["body"] == expected_answer["body"]
#
#     #
#     # ```
#     # import requests
#     #
#     # ACCESS_TOKEN = "valid_access_token"
#     # REFRESH_TOKEN = "valid_refresh_token"
#     #
#     # headers = {
#     #     "Authorization": f"Bearer {REFRESH_TOKEN}",
#     #     "Content-Type": "application/json"
#     # }
#     #
#     # response = requests.post("http://example.com/refresh", headers=headers)
#     #
#     # if response.status_code == requests.codes.ok:
#     #     new_access_token = response.json()["access_token"]
#     #     print(f"New access token: {new_access_token}")
#     # else:
#     #     print("Token refresh failed")
#     # ```
# #
# # @pytest.mark.parametrize(
# #     "query_data, expected_answer",
# #     [
# #         (
# #                 {'username': 'user13', 'password': '234'},
# #                 {"status": HTTPStatus.OK,
# #                  "body": {"message": "Login ok"}},
# #         ),
# #     ],
# # )
# # @pytest.mark.asyncio
# # async def test_login_user(
# #         make_post_request, make_delete_request, query_data, expected_answer
# # ):
# #     response = await make_post_request("/auth/login", query_data)
# #     assert response["status"] == expected_answer["status"]
# #     assert response["body"] == expected_answer["body"]
