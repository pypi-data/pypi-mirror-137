"""Тесты для проверки работоспособности вспомогательных функций."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..utils import get_object_or_none, random_string


class UtilTestCase(TestCase):
    """Класс тестирования и проверки работоспособности вспомогательных функций."""

    def test_random_string_length(self) -> None:
        """Тестирование функции random_string."""
        self.assertEqual(len(random_string()), 30)
        self.assertEqual(len(random_string(100)), 100)
        self.assertEqual(len(random_string(0)), 30)
        self.assertEqual(len(random_string(-1)), 30)

    def test_random_string_type(self) -> None:
        """Проверка типа генерации."""
        self.assertEqual(type(random_string()), str)


class GetObjectOrNoneTestCase(TestCase):
    """Тестирование утилиты для получения объекта."""

    def setUp(self) -> None:
        """Устанавливаем настройки для проведения тестирования."""
        self.user = get_user_model().objects.create(
            username='admin',
            email='test@test.ru',
            first_name='FirstName',
            last_name='LastName'
        )
        self.user.set_password('1234')
        self.user.save(update_fields=('password',))

    def test_get_object_or_none(self) -> None:
        """Тестируем получение создания пользователя."""
        exists_user_email = get_object_or_none(get_user_model(), email='test@test.ru')
        self.assertEqual(self.user, exists_user_email)
        exists_user_username = get_object_or_none(get_user_model(), username='admin')
        self.assertEqual(self.user, exists_user_username)
        empty_user = get_object_or_none(get_user_model(), username='admin_')
        self.assertIsNone(empty_user)

    def tearDown(self) -> None:
        """Очистка модели после завершения тестирования."""
        self.user.delete()
