"""Тесты связанные с проверкой работоспособности команд."""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from oauth2_provider.models import get_application_model

from ..utils import get_object_or_none


class CommandTestCase(TestCase):
    """Класс для проверки запуска команд."""

    def setUp(self) -> None:
        """Создаем приложение."""
        self.app_name = 'app'
        out = StringIO()
        call_command('createoauthapp', self.app_name, stdout=out)
        self.out = out

    def test_command_out(self) -> None:
        """Проверяем формат вывода информации."""
        self.assertIn('Новое приложение создано', self.out.getvalue())
        self.assertIn('client_id', self.out.getvalue())
        self.assertIn('client_secret', self.out.getvalue())

    def test_created_application(self) -> None:
        """Ищем приложение."""
        application = get_object_or_none(get_application_model(), name=self.app_name)
        self.assertIsNotNone(application)

    def tearDown(self) -> None:
        """Действия после завершения теста."""
        get_application_model().objects.all().delete()
