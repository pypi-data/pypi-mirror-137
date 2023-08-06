"""Описание схемы авторизации через портал https://cbias.ru."""

import graphene
from django.conf import settings
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from .mutations import CbiasAuthMutation


class UserType(DjangoObjectType):
    """Описание пользовательского типа."""

    class Meta:
        """Описание модели."""

        model = get_user_model()


class Query(graphene.ObjectType):
    """Пример запроса на сервер."""

    hello = graphene.String(default_value='hello, world!')


class AuthMutation(CbiasAuthMutation):
    """Описание параметров мутации для авторизации через https://cbias.ru."""

    class Meta:
        """Описание мета данных для настройки авторизационной мутации."""

        user_type = UserType
        url = settings.EXTERNAL_URLS.get('cbias')
        description = 'Авторизация через портал https://cbias.ru'


class Mutation(graphene.ObjectType):
    """Мутации для авторизации."""

    auth = AuthMutation.Field()
