"""Заготовка мутации для авторизации через портал https://cbias.ru."""
import re
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional, Type, cast

import graphene
import requests
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from graphene import InputObjectType, Mutation, ObjectType, ResolveInfo
from graphene.types.mutation import MutationOptions
from graphene_django.types import DjangoObjectType, ErrorType
from oauth2_provider.models import AccessToken, Application, RefreshToken

from .types import AuthTokenInfoType
from ..utils import get_object_or_none, random_string


class CbiasAuthOptions(MutationOptions):
    """Опции мутации для авторизации через портал https://cbias.ru."""

    user_type: Optional[DjangoObjectType] = None
    url: Optional[str] = None


class CbiasAuthMutation(Mutation):
    """Описание мутации для авторизации через портал https://cbias.ru."""

    Input: Optional[Type[graphene.InputObjectType]] = None
    Output: Optional[Type[graphene.ObjectType]] = None
    get_user: Optional[Callable[[ResolveInfo, Dict[str, str], Dict[str, str]], Type[get_user_model()]]] = None

    class Meta:
        """Описание мета-параметров функции."""

        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
            cls,
            arguments=None,
            output=None,
            name=None,
            _meta=None,
            user_type: Optional[DjangoObjectType] = None,
            url: Optional[str] = None,
            **options
    ) -> None:
        """Функция инициализации с мета-параметрами."""
        assert url, 'Не задан адрес авторизации'
        assert user_type, 'Не задан тип возвращаемого пользователя'
        if not _meta:
            _meta = CbiasAuthOptions(cls)
        base_name: str = re.sub('Payload$', '', name or cls.__name__)

        input_class = getattr(cls, 'Input', None)
        bases = (InputObjectType,)
        if input_class:
            bases += (input_class,)
        input_fields = {
            'uid': graphene.String(required=True, description='Идентификатор пользователя'),
            'client_id': graphene.String(description='Открытый идентификатор приложения'),
            'client_secret': graphene.String(description='Секретный идентификатор приложения'),
            'grant_type': graphene.String(default_value='password', description='Тип авторизации')
        }

        # Конструируем входной класс
        cls.Input = cast(
            Type[graphene.InputObjectType],
            type(
                f'{base_name}Input',
                bases,
                OrderedDict(input_fields)
            )
        )
        arguments = OrderedDict(payload=cls.Input(required=True))

        output_fields: Dict[str, ObjectType] = {
            'success': graphene.Boolean(required=True, description='Статус операции'),
            'errors': graphene.List(ErrorType, description='Ошибки'),
            'token': graphene.Field(AuthTokenInfoType, description='Информация о токене доступа'),
            'user': graphene.Field(user_type, description='Авторизованный пользователь')
        }
        cls.Output = cast(
            Type[graphene.ObjectType],
            type(
                f'{base_name}Output',
                (graphene.ObjectType,),
                OrderedDict(output_fields)
            )
        )
        output = cls.Output
        super(CbiasAuthMutation, cls).__init_subclass_with_meta__(
            output=output, arguments=arguments, name=name, _meta=_meta, **options
        )
        cls._meta.fields['url'] = url
        cls._meta.fields['user_type'] = user_type

    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, payload: Dict[str, str]) -> ObjectType:
        """Мутация для авторизации.

        :param root: None
        :param info: контекст запроса
        :param payload:
            - uid: Идентификатор пользователя
            - client_id: Открытый идентификатор приложения
            - client_secret: Секретный идентификатор приложения
            - grant_type: Тип авторизации. default = password
        :return:
        """
        user_type: DjangoObjectType = cls._meta.fields['user_type']
        url: str = cls._meta.fields['url'] % payload.get('uid')
        response = requests.get(url)
        if response.status_code != 200:
            return cls.Output(
                success=False,
                errors=[ErrorType('auth', ['Авторизация невозможна: Пользователь не авторизован'])]
            )
        client_id = payload['client_id']
        client_secret = payload['client_secret']
        application: Optional[Application] = get_object_or_none(
            Application,
            client_id=client_id,
            client_secret=client_secret
        )
        if not application:
            return cls.Output(
                success=False,
                errors=[ErrorType('auth', ['Авторизация невозможна: Приложения не найдено'])]
            )

        data: Dict[str, str] = response.json()['data']
        get_user = getattr(cls, 'get_user', None)
        if get_user:
            user: Type[get_user_model()] = get_user(info, payload, data)
        else:
            user_model = user_type._meta.model
            user, created = user_model.objects.get_or_create(
                username=data['login'],
                defaults={
                    'email': data['Email'],
                    'first_name': data['Name'],
                    'last_name': data['Sirname']
                }
            )
        expires_delta: timedelta = timedelta(seconds=36000)
        expires = make_aware(datetime.now() + expires_delta)
        scope: str = 'read write groups'
        refresh_token: RefreshToken = RefreshToken.objects.create(
            user=user,
            token=random_string(20),
            application=application
        )
        access_token: AccessToken = AccessToken.objects.create(
            user=user,
            source_refresh_token=refresh_token,
            token=random_string(64),
            application=application,
            expires=expires,
            scope=scope
        )
        refresh_token.access_token = access_token
        refresh_token.save(update_fields=('access_token',))
        token: AuthTokenInfoType = AuthTokenInfoType(
            access_token=access_token.token,
            expires_in=expires_delta.total_seconds(),
            token_type='Bearer',
            scope=scope,
            refresh_token=refresh_token.token,
            redirect_uris=application.redirect_uris
        )
        return cls.Output(success=True, user=user, token=token)
