import allure
import pytest

from api_client import login_user, update_user
from data_generator import generate_user_data


@allure.feature('Изменение данных пользователя')
class TestUserUpdate:
    """Тесты эндпоинта PATCH /auth/user."""

    @allure.title('Изменение поля "{field}" авторизованным пользователем')
    @pytest.mark.parametrize('field', ['name', 'email'])
    def test_update_field_with_auth(self, registered_user, field):
        _, register_response = registered_user
        access_token = register_response['accessToken']
        new_value = generate_user_data()[field]

        response = update_user(access_token, {field: new_value})
        response_data = response.json()

        with allure.step(f'Проверить, что поле "{field}" обновилось'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user'][field] == new_value

    @allure.title('Изменение пароля авторизованным пользователем')
    def test_update_password_with_auth(self, registered_user):
        # пароль не возвращается в теле ответа, поэтому смену проверяем логином
        user_data, register_response = registered_user
        access_token = register_response['accessToken']
        new_password = generate_user_data()['password']

        response = update_user(access_token, {'password': new_password})

        with allure.step('Проверить успешный ответ на смену пароля'):
            assert response.status_code == 200
            assert response.json()['success'] is True

        login_response = login_user({'email': user_data['email'], 'password': new_password})

        with allure.step('Проверить, что вход с новым паролем работает'):
            assert login_response.status_code == 200
            assert login_response.json()['success'] is True

    @allure.title('Изменение поля "{field}" без авторизации')
    @pytest.mark.parametrize('field', ['name', 'email', 'password'])
    def test_update_field_without_auth(self, field):
        response = update_user(None, {field: generate_user_data()[field]})
        response_data = response.json()

        with allure.step('Проверить, что сервер отклонил запрос без авторизации'):
            assert response.status_code == 401
            assert response_data['success'] is False
            assert response_data['message'] == 'You should be authorised'
