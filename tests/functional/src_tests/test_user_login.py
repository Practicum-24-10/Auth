from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "usertest", "password": "2wewew34"},
            {"status": HTTPStatus.OK, "body": {"message": "Login ok"}},
        ),
        (
            {"username": "1", "password": "1"},
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
        ),
        (
            {"username": "234234231", "password": "1"},
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
        ),
        (
            {"username": "", "password": "134223423"},
            {"status": HTTPStatus.BAD_REQUEST, "body": {"message": "Validation Error"}},
        ),
        (
            {"username": "usertest", "password": "134223423"},
            {
                "status": HTTPStatus.BAD_REQUEST,
                "body": {"message": "Login or password wrong"},
            },
        ),
        (
            {"username": "usertesst", "password": "2wewew34"},
            {
                "status": HTTPStatus.BAD_REQUEST,
                "body": {"message": "Login or password wrong"},
            },
        ),
    ],
)
@pytestmark
async def test_login_user(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/auth/login", query_data)
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    if response["body"]["message"] == "Login ok":
        assert response["body"]["access_token"]
        assert response["body"]["refresh_token"]
