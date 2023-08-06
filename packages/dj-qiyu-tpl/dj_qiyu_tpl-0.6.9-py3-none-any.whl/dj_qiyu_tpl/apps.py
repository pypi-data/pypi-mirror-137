from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

__all__ = ["DjQiYuTplConfig"]


class DjQiYuTplConfig(AppConfig):
    name = "dj_qiyu_tpl"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.verbose_name = pgettext_lazy("model", "奇遇科技模版")
