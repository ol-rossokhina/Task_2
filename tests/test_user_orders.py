import allure

from tests.api_client import create_order, get_user_orders


@allure.feature('Получение заказов пользователя')
class TestGetUserOrders:
    """Тесты эндпоинта GET /orders (заказы конкретного пользователя)."""

    @allure.title('Получение заказов авторизованным пользователем')
    def test_get_orders_authorized_user(self, registered_user, ingredient_ids):
        _, register_response = registered_user
        access_token = register_response['accessToken']
        create_order(ingredient_ids[:1], access_token)

        response = get_user_orders(access_token)
        response_data = response.json()

        with allure.step('Проверить, что вернулись заказы пользователя'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert isinstance(response_data['orders'], list)
            assert len(response_data['orders']) >= 1

    @allure.title('Получение заказов неавторизованным пользователем')
    def test_get_orders_unauthorized_user(self):
        response = get_user_orders()
        response_data = response.json()

        with allure.step('Проверить, что сервер отклонил запрос без авторизации'):
            assert response.status_code == 401
            assert response_data['success'] is False
            assert response_data['message'] == 'You should be authorised'
