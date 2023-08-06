# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_cbias_auth',
 'django_cbias_auth.management.commands',
 'django_cbias_auth.schema',
 'django_cbias_auth.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4,<5',
 'django-oauth-toolkit>=1.7.0,<2.0.0',
 'graphene-django>=2.15.0,<3.0.0',
 'graphene==2.1.9',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'django-cbias-auth',
    'version': '0.1.1',
    'description': 'Auth library via https://cbias.ru',
    'long_description': "# Django-Cbias-Auth\nБиблиотека для авторизации на портале https://cbuas.ru.\n\n## Установка\n\n```shell\n# via pip\npip install django_cbias_auth\n# via poetry\npoetry add django_cbias_auth\n```\n\n## Настройки\n\nВ файл `settings.py` добавить:\n```python\n\nEXTERNAL_URLS = {\n    'auth_cbias': 'www.cbias.ru/sso_app/remote_auth.spf?uid=%uid&ris=%system'\n}\n\n```\n- %uid - идентификатор пользователя\n- %system - идентификатор системы\n\n## Схема\n\n```gql\nmutation Auth($uid: String!, $clientId: String!, $clientSecret: String!) {\n  auth(payload: { uid: $uid, clientId: $clientId, clientSecret: $clientSecret }) {\n    success\n    errors {\n      field\n      messages\n      __typename\n    }\n    __typename\n  }\n}\n```\n\n# Создание приложения\n\n```python\npython manage.py createoauthapp 'Авторизация через cbias.ru' \n```",
    'author': 'devind-team',
    'author_email': 'team@devind.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/django-cbias-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.9,<4.0.0',
}


setup(**setup_kwargs)
