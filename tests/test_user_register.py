import allure
import pytest

from tests.api_client import register_user
from tests.data_generator import generate_user_data


@allure.feature('Регистрация пользователя')
class TestUserRegister:
    """Тесты эндпоинта POST /auth/register."""

    @allure.title('Регистрация уникального пользователя')
    def test_register_unique_user(self, cleanup_user):
        user_data = generate_user_data()

        response = register_user(user_data)
        response_data = response.json()
        cleanup_user.append(response_data.get('accessToken'))

        with allure.step('Проверить, что пользователь успешно создан'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user']['email'] == user_data['email']
            assert response_data['user']['name'] == user_data['name']
            assert 'accessToken' in response_data
            assert 'refreshToken' in response_data

    @allure.title('Повторная регистрация уже существующего пользователя')
    def test_register_existing_user(self, registered_user):
        user_data, _ = registered_user

        response = register_user(user_data)
        response_data = response.json()

        with allure.step('Проверить, что сервер отклонил повторную регистрацию'):
            assert response.status_code == 403
            assert response_data['success'] is False
            assert response_data['message'] == 'User already exists'

    @allure.title('Регистрация без обязательного поля "{missing_field}"')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_without_required_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]

        response = register_user(user_data)
        response_data = response.json()

        # пользователь не создаётся, поэтому удалять после теста нечего
        with allure.step('Проверить, что сервер вернул ошибку валидации'):
            assert response.status_code == 403
            assert response_data['success'] is False
            assert response_data['message'] == 'Email, password and name are required fields'
