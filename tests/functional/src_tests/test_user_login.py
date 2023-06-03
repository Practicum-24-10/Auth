from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"username": "1", "password": "1"},
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
        ),
        (
                {"username": "234234231", "password": "1"},
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
        ),
        (
                {"username": "", "password": "134223423"},
                {"status": HTTPStatus.BAD_REQUEST,
                 "body": {"message": "Validation Error"}},
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
async def test_login_bad_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"
    # Act
    response = await make_post_request(request_url_login, query_data)
    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"username": "usertest", "password": "2wewew34"},
                {"status": HTTPStatus.OK, "body": {"message": "Login ok"}},
        )
    ],
)
@pytestmark
async def test_login_ok_user(
        make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/login"

    # Act
    response = await make_post_request(request_url_login, query_data)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["message"] == expected_answer["body"]["message"]
    assert response["body"]["access_token"]
    assert response["body"]["refresh_token"]
