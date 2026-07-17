import pytest
from helpers import register_user_and_return_data, delete_user


@pytest.fixture
def user_data():
    data = register_user_and_return_data()
    yield data
    if data and data.get("token"):
        delete_user(data["token"])


@pytest.fixture
def user_token(user_data):
    return user_data["token"]