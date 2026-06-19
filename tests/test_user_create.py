import allure
import requests
from config import Config
from helpers import register_user_and_return_data, delete_user


@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        with allure.step("Регистрация нового пользователя"):
            data = register_user_and_return_data()

        assert data is not None
        assert "token" in data

        # Удаляем пользователя после теста
        delete_user(data["token"])

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_duplicate_user(self, user_data):
        payload = {
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"]
        }
        response = requests.post(f"{Config.USER_URL}/register", data=payload)
        assert response.status_code == 403
        assert "User already exists" in response.json().get("message", "")

    @allure.title("Создание пользователя без email")
    def test_create_user_without_email(self):
        payload = {"password": "pass", "name": "name"}
        response = requests.post(f"{Config.USER_URL}/register", data=payload)
        assert response.status_code == 403

    @allure.title("Создание пользователя без пароля")
    def test_create_user_without_password(self):
        payload = {"email": "test@test.com", "name": "name"}
        response = requests.post(f"{Config.USER_URL}/register", data=payload)
        assert response.status_code == 403
        