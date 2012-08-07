# vim: ts=4 sw=4 et:
from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django_sanction.util import get_def
from django_sanction.decorators import anonymous_required


class Home(TemplateView):
    template_name = "home.html"

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return TemplateView.dispatch(self, *args, **kwargs)


    def get_context_data(self, **kwargs):
        return {
            "providers": settings.SANCTION_PROVIDERS,
        }


class Profile(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        return {
            "user": self.request.user
        }

