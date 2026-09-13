import allure
import pytest

from api_client import delete_user, get_ingredients, register_user
from data_generator import generate_user_data


@pytest.fixture
def registered_user():
    """
    Регистрирует нового пользователя перед тестом и гарантированно удаляет
    его после теста (в т.ч. если тест упал), чтобы не засорять базу
    и не влиять на другие тесты.
    Возвращает кортеж (исходные данные пользователя, тело ответа регистрации).
    """
    with allure.step('Предусловие: создать нового пользователя'):
        user_data = generate_user_data()
        response = register_user(user_data)
        response_data = response.json()

    yield user_data, response_data

    with allure.step('Постусловие: удалить созданного пользователя'):
        access_token = response_data.get('accessToken')
        if access_token:
            delete_user(access_token)


@pytest.fixture
def cleanup_user():
    """
    Постусловие для тестов, которые сами регистрируют пользователя
    (например, тест самого эндпоинта регистрации). Тест кладёт в список
    accessToken созданного пользователя, а удаление выполняется здесь,
    после yield — фикстура вызовет его независимо от исхода теста,
    без try/finally в самом тесте.
    """
    tokens = []

    yield tokens

    for token in tokens:
        if token:
            delete_user(token)


@pytest.fixture(scope='session')
def ingredient_ids():
    """
    Получает реальные id ингредиентов с сервера один раз за сессию.
    Это справочные данные, которые тесты не создают и не удаляют,
    поэтому их не нужно запрашивать заново перед каждым тестом.
    """
    with allure.step('Предусловие: получить список id ингредиентов с сервера'):
        response = get_ingredients()
        ingredients = response.json()['data']

        return [ingredient['_id'] for ingredient in ingredients]
