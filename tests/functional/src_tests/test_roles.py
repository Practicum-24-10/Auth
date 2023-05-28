from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin75fg55f7"},
            {"status": HTTPStatus.CREATED, "name": "Admin75fg55f7"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_role(
    make_post_request, make_delete_request, query_data, expected_answer
):
    response = await make_post_request("/roles/create", query_data)
    assert response["status"] == expected_answer["status"]
    assert response['body']["name"] == expected_answer["name"]
    role_id = response['body']["id"]
    await make_delete_request(f"/roles/delete/{role_id}")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": "Admin66fdcdsv6"},
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
    response = await make_post_request("/roles/create", query_data)
    role_id = response["body"]["id"]
    response = await make_delete_request(f"/roles/delete/{role_id}")
    assert response["status"] == expected_answer["status"]
    assert response["body"] == expected_answer["body"]
