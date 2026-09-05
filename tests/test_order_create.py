import allure

from tests.api_client import create_order

# Синтаксически валидный, но не существующий на сервере id ингредиента
INVALID_INGREDIENT_HASH = 'a' * 24


@allure.feature('Создание заказа')
class TestOrderCreate:
    """
    Тесты эндпоинта POST /orders.

    Сценарии "с авторизацией" и "с ингредиентами" объединены в одном тесте
    (test_create_order_with_auth), а "без авторизации" — с ингредиентами
    в другом (test_create_order_without_auth): по документации наличие
    авторизации не меняет формат ответа при успешном создании заказа,
    поэтому раздельные тесты дублировали бы друг друга.
    """

    @allure.title('Создание заказа авторизованным пользователем')
    def test_create_order_with_auth(self, registered_user, ingredient_ids):
        _, register_response = registered_user
        access_token = register_response['accessToken']

        response = create_order(ingredient_ids[:2], access_token)
        response_data = response.json()

        with allure.step('Проверить, что заказ успешно создан'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert 'number' in response_data['order']
            assert response_data['name']

    @allure.title('Создание заказа неавторизованным пользователем')
    def test_create_order_without_auth(self, ingredient_ids):
        response = create_order(ingredient_ids[:2])
        response_data = response.json()

        with allure.step('Проверить, что заказ успешно создан без авторизации'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert 'number' in response_data['order']

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, registered_user):
        _, register_response = registered_user
        access_token = register_response['accessToken']

        response = create_order([], access_token)
        response_data = response.json()

        with allure.step('Проверить, что сервер вернул ошибку об отсутствии ингредиентов'):
            assert response.status_code == 400
            assert response_data['success'] is False
            assert response_data['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа с несуществующим id ингредиента')
    def test_create_order_with_invalid_ingredient_hash(self, registered_user):
        _, register_response = registered_user
        access_token = register_response['accessToken']

        response = create_order([INVALID_INGREDIENT_HASH], access_token)

        # по документации ожидается 500, но реальный сервер отвечает 400 —
        # тест ориентируется на документацию API
        with allure.step('Проверить, что сервер вернул ошибку'):
            assert response.status_code == 500
