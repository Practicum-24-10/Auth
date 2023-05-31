from tests.functional.testdata.users import user

permissions = [
    {
        "permission": "AccessControle",
        "id": "614009f4-ce36-4f83-9013-325e0ff52ead",
    },
    {
        "permission": "SomePermission",
        "id": "1e0d2b7f-cc0c-4496-8ce1-dd3b463690ab",
    },
    {
        "permission": "SimplePermission",
        "id": "fc096081-fbc6-40b2-9ad0-8d0ae58c89c5",
    },
]


roles = [
    {
        "name": "Admin",
        "id": "6fa459ea-ee8a-3ca4-894e-db77e160355e",
    },
    {
        "name": "Member",
        "id": "5492944e-a38e-422b-a6af-18b9a04f0c5b",
    },
    {
        "name": "SuperAdmin",
        "id": "225054e2-5268-4c4d-853c-4a24085e1f02",
    },
]

role_permissions = [
    {
        "role_id": roles[0]["id"],
        "permission_id": permissions[0]["id"],
    },
    {
        "role_id": roles[1]["id"],
        "permission_id": permissions[1]["id"],
    },
]

user_roles = [
    {
        "user_id": user[0]["id"],
        "role_id": roles[0]["id"],
    },
    {
        "user_id": user[0]["id"],
        "role_id": roles[1]["id"],
    },
]
