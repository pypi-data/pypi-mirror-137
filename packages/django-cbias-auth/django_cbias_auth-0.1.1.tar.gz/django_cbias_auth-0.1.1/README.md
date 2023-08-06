# Django-Cbias-Auth
Библиотека для авторизации на портале https://cbuas.ru.

## Установка

```shell
# via pip
pip install django_cbias_auth
# via poetry
poetry add django_cbias_auth
```

## Настройки

В файл `settings.py` добавить:
```python

EXTERNAL_URLS = {
    'auth_cbias': 'www.cbias.ru/sso_app/remote_auth.spf?uid=%uid&ris=%system'
}

```
- %uid - идентификатор пользователя
- %system - идентификатор системы

## Схема

```gql
mutation Auth($uid: String!, $clientId: String!, $clientSecret: String!) {
  auth(payload: { uid: $uid, clientId: $clientId, clientSecret: $clientSecret }) {
    success
    errors {
      field
      messages
      __typename
    }
    __typename
  }
}
```

# Создание приложения

```python
python manage.py createoauthapp 'Авторизация через cbias.ru' 
```