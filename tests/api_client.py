from typing import List, Optional

import allure
import requests

from tests.endpoints import INGREDIENTS_URL, LOGIN_URL, ORDERS_URL, REGISTER_URL, USER_URL


def _auth_headers(access_token: Optional[str]) -> dict:
    return {'Authorization': access_token} if access_token else {}


def register_user(user_data: dict) -> requests.Response:
    email = user_data.get('email', '<без email>')
    with allure.step(f'Зарегистрировать пользователя {email}'):
        return requests.post(REGISTER_URL, json=user_data)


def login_user(credentials: dict) -> requests.Response:
    email = credentials.get('email', '<без email>')
    with allure.step(f'Авторизоваться под пользователем {email}'):
        return requests.post(LOGIN_URL, json=credentials)


@allure.step('Удалить пользователя')
def delete_user(access_token: Optional[str]) -> requests.Response:
    return requests.delete(USER_URL, headers=_auth_headers(access_token))


@allure.step('Обновить данные пользователя: {data}')
def update_user(access_token: Optional[str], data: dict) -> requests.Response:
    return requests.patch(USER_URL, json=data, headers=_auth_headers(access_token))


@allure.step('Получить список доступных ингредиентов')
def get_ingredients() -> requests.Response:
    return requests.get(INGREDIENTS_URL)


@allure.step('Создать заказ с ингредиентами {ingredient_ids}')
def create_order(ingredient_ids: List[str], access_token: Optional[str] = None) -> requests.Response:
    return requests.post(ORDERS_URL, json={'ingredients': ingredient_ids}, headers=_auth_headers(access_token))


@allure.step('Получить заказы пользователя')
def get_user_orders(access_token: Optional[str] = None) -> requests.Response:
    return requests.get(ORDERS_URL, headers=_auth_headers(access_token))
