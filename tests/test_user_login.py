import allure
import requests
from config import Config


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_success(self, user_data):
        payload = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post(f"{Config.USER_URL}/login", data=payload)
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином и паролем")
    def test_login_wrong_credentials(self):
        payload = {"email": "nonexist@test.com", "password": "wrongpass"}
        response = requests.post(f"{Config.USER_URL}/login", data=payload)
        assert response.status_code == 401
        assert "email or password are incorrect" in response.json().get("message", "")