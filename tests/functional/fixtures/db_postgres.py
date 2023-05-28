import pytest

from src.core.config import config
from src.models.users import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.functional.testdata.users import persons_data


@pytest.fixture(scope="module")
def session():
    engine = create_engine(
        f'postgresql://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_name}')
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

    return inner


@pytest.fixture(scope="module")
def pg_delete_data(session):
    def inner():
        session.query(User).delete()
        session.commit()

    return inner


@pytest.fixture(scope="module", autouse=True)
def create_db(pg_write_data, pg_delete_data):
    pg_write_data()
    yield
    pg_delete_data()
