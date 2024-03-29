from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "usertdsdest", "password": "2wewew34"},
            {
                "status": HTTPStatus.OK,
                "body": {"message": "New account was registered"},
            },
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
                "body": {"message": "This login already exists"},
            },
        ),
    ],
)
@pytestmark
async def test_add_user(
    make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    request_url_login = "/auth/signup"

    # Act
    response = await make_post_request(request_url_login, query_data)

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
