from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin5"},
            {"status": HTTPStatus.OK, "body": {"message": "Role created successfully"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_role(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/roles/create", query_data)
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
    role_name = query_data["name"]
    await make_delete_request(f"/roles/delete/{role_name}")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin12"},
            {
                "status": HTTPStatus.OK,
                "body": {"message": "The Admin12 role has been successfully deleted"},
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_role(
    make_post_request, make_delete_request, query_data, expected_answer
):
    await make_post_request("/roles/create", query_data)
    role_name = query_data["name"]
    response = await make_delete_request(f"/roles/delete/{role_name}")
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
