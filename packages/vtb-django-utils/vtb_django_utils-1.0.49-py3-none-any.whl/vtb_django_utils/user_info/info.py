import contextvars  # noqa
from datetime import datetime
from typing import Union, Any

from django.contrib.auth import get_user_model

from vtb_django_utils.drf.auth import KeycloakUser
from vtb_django_utils.user_info.consts import USER_MODEL_KEY
from vtb_django_utils.utils.consts import DATETIME_SHORT_FORMAT
from vtb_django_utils.utils.db import get_model_field_names

_user_info = contextvars.ContextVar('user_info', default={})

user_class = get_user_model()
user_model_fields = get_model_field_names(user_class, exclude=('password', 'last_login'))
keycloak_class_fields = ('id', 'email', 'first_name', 'last_name', 'username')


def get_user_info():
    return _user_info.get() or {}


def set_user_info(request):
    if user := getattr(request, 'user', None):
        if isinstance(user, KeycloakUser):
            value = _get_user_info(user, keycloak_class_fields)
            value[USER_MODEL_KEY] = KeycloakUser.__name__
        elif isinstance(user, user_class):
            value = _get_user_info(user, user_model_fields)
            value[USER_MODEL_KEY] = user_class.__name__
        else:
            value = None
        if value:
            _user_info.set(value)


def _format_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.strftime(DATETIME_SHORT_FORMAT)
    return value


def _get_user_info(user: object, fields: Union[list, tuple]) -> dict:
    return {field_name: _format_value(getattr(user, field_name)) for field_name in fields if hasattr(user, field_name)}
