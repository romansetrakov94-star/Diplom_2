import random
import string
import requests
from config import Config


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def register_user_and_return_data():
    email = f"{generate_random_string(8)}@test.com"
    password = generate_random_string(8)
    name = generate_random_string(6)

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(f"{Config.USER_URL}/register", data=payload)
    if response.status_code == 200:
        return {
            "email": email,
            "password": password,
            "name": name,
            "token": response.json().get("accessToken")
        }
    return None


def delete_user(token):
    requests.delete(f"{Config.USER_URL}/user", headers={"Authorization": token})