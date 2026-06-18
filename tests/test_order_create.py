import allure
import requests
from config import Config


@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, user_token):
        ingredients_response = requests.get(f"{Config.BASE_URL}/api/ingredients")
        ingredients = ingredients_response.json()["data"]
        ids = [ing["_id"] for ing in ingredients[:2]]

        payload = {"ingredients": ids}
        headers = {"Authorization": user_token}
        response = requests.post(Config.ORDERS_URL, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") == True
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients_response = requests.get(f"{Config.BASE_URL}/api/ingredients")
        ingredients = ingredients_response.json()["data"]
        ids = [ing["_id"] for ing in ingredients[:1]]

        payload = {"ingredients": ids}
        response = requests.post(Config.ORDERS_URL, data=payload)
        # Сервер разрешает создавать заказы без авторизации на этом стенде
        assert response.status_code == 200
        assert response.json().get("success") == True
        assert "order" in response.json()

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, user_token):
        payload = {"ingredients": []}
        headers = {"Authorization": user_token}
        response = requests.post(Config.ORDERS_URL, data=payload, headers=headers)
        assert response.status_code == 400
        assert "Ingredient ids must be provided" in response.json().get("message", "")

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_wrong_hash(self, user_token):
        payload = {"ingredients": ["invalidhash123"]}
        headers = {"Authorization": user_token}
        response = requests.post(Config.ORDERS_URL, data=payload, headers=headers)
        assert response.status_code == 500