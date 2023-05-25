from pydantic import BaseSettings


class TestSettings(BaseSettings):
    db_name: str = 'auth_db'
    db_user: str = 'auth_user'
    db_password: str = '123qwe'

    service_url: str = 'http://127.0.0.1:5000/api/v1'


test_settings = TestSettings()
