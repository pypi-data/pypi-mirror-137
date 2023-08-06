"""Описание типов библиотеке авторизации."""

import graphene


class AuthTokenInfoType(graphene.ObjectType):
    """Информация о сгенерированном токене доступа."""

    access_token = graphene.String(description='Токен доступа')
    expires_in = graphene.Int(description='Время жизни токена')
    token_type = graphene.String(description='Тип токена')
    scope = graphene.String(description='Разрешения')
    refresh_token = graphene.String(description='Токен обновления')
    redirect_uris = graphene.String(description='Переадресация при авторизации')
