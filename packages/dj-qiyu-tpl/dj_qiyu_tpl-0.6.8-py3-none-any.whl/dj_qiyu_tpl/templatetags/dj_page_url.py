from urllib.parse import urlencode

from django import template
from django.http import HttpRequest
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def dj_page_url(context: template.RequestContext, page: int) -> str:
    """
    渲染翻页页面的 URL

    例子:
        <a href="{% dj_page_url 2 %}">2</a>
    """

    request = context.request
    assert isinstance(request, HttpRequest)
    get = request.GET.dict()  # noqa
    get["page"] = page  # overwrite page

    url = f"{request.path}?{urlencode(get)}"

    return mark_safe(url)
