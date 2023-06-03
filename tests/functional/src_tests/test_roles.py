from http import HTTPStatus

import pytest

from tests.functional.testdata.perm_role_user import roles

pytestmark = pytest.mark.asyncio


@pytestmark
async def test_get_all_role(make_get_request, make_post_request):
    # Arrange
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_get_request("/roles/all", headers=headers)

    # Assert
    assert response["status"] == HTTPStatus.OK
    assert response["body"] == roles


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin456"},
            {"status": HTTPStatus.CREATED, "name": "Admin456"},
        ),
    ],
)
@pytestmark
async def test_add_role(
    make_post_request, query_data, expected_answer
):
    # Arrange
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_post_request(
        "/roles/create", params=query_data, headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["name"] == expected_answer["name"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"id": roles[2]["id"]},
            {
                "status": HTTPStatus.ACCEPTED,
                "body": {"message": "Role deleted successfully"},
            },
        ),
    ],
)
@pytestmark
async def test_delete_role(
    make_post_request, make_delete_request, query_data, expected_answer
):
    # Arrange
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_delete_request(
        f"/roles/delete/{query_data['id']}", headers=headers
    )

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"id": roles[1]["id"]},
            {"status": HTTPStatus.OK, "name": "NotAdmin"},
        ),
    ],
)
@pytestmark
async def test_update_role(
    make_post_request,
    make_update_request,
    query_data,
    expected_answer,
):
    # Arrange
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_update_request(
        f"/roles/update/{query_data['id']}",
        {"name": expected_answer["name"]},
        headers=headers,
    )

    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["name"] == expected_answer["name"]
