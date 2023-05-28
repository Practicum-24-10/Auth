from http import HTTPStatus

import pytest

from tests.functional.testdata.roles import roles
from tests.functional.testdata.users import user

user_id = user[0]["id"]
role_id = roles[1]["id"]


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