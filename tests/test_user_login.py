import allure
import pytest

from api_client import login_user
from data_generator import generate_user_data


@allure.feature('Логин пользователя')
class TestUserLogin:
    """Тесты эндпоинта POST /auth/login."""

    @allure.title('Логин под существующим пользователем')
    def test_login_existing_user(self, registered_user):
        user_data, _ = registered_user

        response = login_user({'email': user_data['email'], 'password': user_data['password']})
        response_data = response.json()

        with allure.step('Проверить успешный ответ и данные пользователя'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user']['email'] == user_data['email']
            assert response_data['user']['name'] == user_data['name']
            assert 'accessToken' in response_data
            assert 'refreshToken' in response_data

    @allure.title('Логин с неверным полем "{wrong_field}"')
    @pytest.mark.parametrize('wrong_field', ['email', 'password'])
    def test_login_with_invalid_credentials(self, registered_user, wrong_field):
        user_data, _ = registered_user
        with allure.step(f'Подготовить данные с неверным полем "{wrong_field}"'):
            credentials = {'email': user_data['email'], 'password': user_data['password']}
            # подменяем ровно одно поле на заведомо неверное значение
            credentials[wrong_field] = generate_user_data()[wrong_field]

        response = login_user(credentials)
        response_data = response.json()

        with allure.step('Проверить, что сервер отклонил вход'):
            assert response.status_code == 401
            assert response_data['success'] is False
            assert response_data['message'] == 'email or password are incorrect'
