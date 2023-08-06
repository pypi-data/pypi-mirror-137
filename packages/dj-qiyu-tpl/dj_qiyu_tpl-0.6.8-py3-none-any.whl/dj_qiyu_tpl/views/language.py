from django.conf import settings
from django.http import HttpRequest
from django.views.generic import RedirectView

__all__ = ["ChangeLanguageView"]


class ChangeLanguageView(RedirectView):
    """
    User Switch language
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # get the target language, if not exists use default
        language = kwargs.get("language", settings.LANGUAGE_CODE)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response

    def get_redirect_url(self, *args, **kwargs):
        url1 = kwargs.get("next", None)
        if url1 is not None:
            return url1

        request: HttpRequest = self.request
        url2 = request.META.get("HTTP_REFERER", None)
        if url2 is not None:
            return url2

        return "/"
