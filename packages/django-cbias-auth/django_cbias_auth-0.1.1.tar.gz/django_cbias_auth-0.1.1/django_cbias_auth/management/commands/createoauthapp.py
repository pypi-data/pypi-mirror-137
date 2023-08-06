"""Команда создания приложения для авторизации на портале https://cbias.ru."""
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from oauth2_provider.generators import generate_client_id, generate_client_secret
from oauth2_provider.models import get_application_model

Application = get_application_model()


class Command(BaseCommand):
    """Создание приложения."""

    help: str = 'Создание OAuth приложения' # noqa

    def add_arguments(self, parser) -> None:
        """Разбор аргументов командной строки."""
        parser.add_argument(
            'name',
            type=str,
            help='Название приложения'
        )
        parser.add_argument(
            '--client_type',
            type=str,
            help='Тип клиента',
            default='confidential'
        )
        parser.add_argument(
            '--authorization_grant_type',
            type=str,
            help='Способ авторизации пользователя',
            default='password'
        )
        parser.add_argument(
            '--user_id',
            type=int,
            help='Пользователь, который создал приложение'
        )

    def handle(self, *args, **options) -> None:
        """Непосредственное выполнение команды."""
        applications_fields = [field.name for field in Application._meta.fields]
        application_data = {key: value for key, value in options.items() if key in applications_fields}
        application_data.update({
            'client_id': generate_client_id(),
            'client_secret': generate_client_secret()
        })
        app = Application(**application_data)
        try:
            app.full_clean()
        except ValidationError as exc:
            errors = '\n '.join(
                ['- ' + err_key + ': ' + str(err_value) for err_key, err_value in exc.message_dict.items()]
            )
            self.stdout.write(self.style.ERROR(f'Проверьте следующие ошибки:\n {errors}'))
        else:
            app.save()
            self.stdout.write(self.style.SUCCESS('Новое приложение создано'))
            self.stdout.write(f'\tclient_id = {app.client_id}')
            self.stdout.write(f'\tclient_secret = {app.client_secret}')
