import uuid


def generate_user_data() -> dict:
    """
    Генерирует уникальные данные пользователя для регистрации/логина.
    uuid4 гарантирует уникальность email между запусками тестов,
    поэтому тесты не конфликтуют друг с другом и не зависят от порядка запуска.
    """
    unique_id = uuid.uuid4().hex[:12]

    return {
        'email': f'stellar-test-{unique_id}@yandex.ru',
        'password': f'Pass-{unique_id}',
        'name': f'TestUser{unique_id}',
    }
