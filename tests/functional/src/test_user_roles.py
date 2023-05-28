from http import HTTPStatus

import pytest

#  Временное решение для получения айди юзера и роли
user_id = "d1c7d9bd-cf4f-4e60-99c0-85a2c4de35c6"
role_id = "73a8ec75-3aea-47c4-816a-ce4a40b04ab8"


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_id": role_id},
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_user_role(make_post_request, query_data, expected_answer):
    response = await make_post_request(f"/users/{user_id}/AddRole", query_data)
    assert response["status"] == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_id": role_id},
            {"status": HTTPStatus.ACCEPTED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_user_role(make_delete_request, query_data, expected_answer):
    response = await make_delete_request(f"/users/{user_id}/DeleteRole", query_data)
    assert response["status"] == expected_answer["status"]
