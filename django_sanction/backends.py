# vim: ts=4 sw=4 et:
import inspect

from django.conf import settings

from django_sanction.models import User
from django_sanction.util import get_def


class AuthenticationBackend(object):
    def __init__(self):
        assert(hasattr(settings, "OAUTH2_AUTH_FN"))


    @property
    def user_class(self):
        return self.__get_user_class()

    
    @property
    def __authenticate_fn(self):
        return self.__get_callable_def(settings, "OAUTH2_AUTH_FN")


    @property
    def __get_user_fn(self):
        return self.__get_callable_def(settings, "OAUTH2_GET_USER_FN")


    def __get_callable_def(self, obj, key):
        fn_name = getattr(obj, key)
        f = get_def(fn_name)
        assert(callable(f))
        return f


    def authenticate(self, request=None, provider=None, client=None):
        assert(request is not None)
        assert(provider is not None)
        assert(client is not None)

        user = self.__authenticate_fn(request, provider, client)
        return user 


    def get_user(self, user_id):
        if hasattr(settings, "OAUTH2_GET_USER_FN"):
            return self.__get_user_fn(user_id)
        else:
            return User.objects.get(id=user_id)

    
   
    def __get_user_class(self):
        mod_name = getattr(settings, "OAUTH2_USER_CLASS",
            "django.contrib.auth.models.User")
        c = get_def(mod_name)

        assert(inspect.isclass(c))
        return c



