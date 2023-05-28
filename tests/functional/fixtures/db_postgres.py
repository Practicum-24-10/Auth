import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import config
from src.models.roles import Role
from src.models.users import User
from tests.functional.testdata.roles import roles
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

    return inner


@pytest.fixture(scope="module")
def pg_delete_data(session):
    def inner():
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
