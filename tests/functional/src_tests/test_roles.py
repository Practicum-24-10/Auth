from http import HTTPStatus

import pytest

from tests.functional.testdata.roles import roles


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin456"},
            {"status": HTTPStatus.CREATED, "name": "Admin456"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_role(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request(
        "/roles/create", params=query_data, headers=headers
    )
    assert response["status"] == expected_answer["status"]
    assert response["body"]["name"] == expected_answer["name"]
    role_id = response["body"]["id"]
    await make_delete_request(f"/roles/delete/{role_id}", headers=headers)


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin456"},
            {
                "status": HTTPStatus.ACCEPTED,
                "body": {"message": "Role deleted successfully"},
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_role(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request("/roles/create", query_data, headers=headers)
    role_id = response["body"]["id"]
    response = await make_delete_request(f"/roles/delete/{role_id}", headers=headers)
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin456"},
            {"status": HTTPStatus.OK, "name": "NotAdmin"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_role(
    make_post_request,
    make_delete_request,
    make_update_request,
    query_data,
    expected_answer,
):
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_post_request("/roles/create", query_data, headers=headers)
    role_id = response["body"]["id"]
    response = await make_update_request(
        f"/roles/update/{role_id}", {"name": "NotAdmin"}, headers=headers
    )
    assert response["status"] == expected_answer["status"]
    assert response["body"]["name"] == expected_answer["name"]
    await make_delete_request(f"/roles/delete/{role_id}", headers=headers)


@pytest.mark.asyncio
async def test_get_all_role(make_get_request, make_post_request):
    response = await make_post_request(
        "/auth/login", {"username": "usertest", "password": "2wewew34"}
    )
    access_token = response["body"]["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = await make_get_request("/roles/all", headers=headers)
    assert response["status"] == HTTPStatus.OK
    assert response["body"] == roles
