import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import config
from src.models.permissions import Permission, RolesPermissions
from src.models.roles import Role, UsersRole
from src.models.users import User
from tests.functional.testdata.perm_role_user import (
    permissions,
    role_permissions,
    roles,
    user_roles,
)
from tests.functional.testdata.users import persons_data


@pytest.fixture(scope="module")
def session():
    engine = create_engine(
        f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_name}"
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="module")
def pg_write_data(session):
    def inner():
        data = [User(**i) for i in persons_data]
        session.add_all(data)
        session.commit()

        roles_data = [Role(**i) for i in roles]
        session.add_all(roles_data)
        session.commit()

        permission_data = [Permission(**i) for i in permissions]
        session.add_all(permission_data)
        session.commit()

        user_roles_data = [UsersRole(**i) for i in user_roles]
        session.add_all(user_roles_data)
        session.commit()

        role_permissions_data = [RolesPermissions(**i) for i in role_permissions]
        session.add_all(role_permissions_data)
        session.commit()

    return inner


@pytest.fixture(scope="module")
def pg_delete_data(session):
    def inner():
        session.query(RolesPermissions).delete()
        session.commit()

        session.query(UsersRole).delete()
        session.commit()

        session.query(Permission).delete()
        session.commit()

        session.query(User).delete()
        session.commit()

        session.query(Role).delete()
        session.commit()

    return inner


@pytest.fixture(scope="module", autouse=True)
def create_db(pg_write_data, pg_delete_data):
    pg_write_data()
    yield
    pg_delete_data()
