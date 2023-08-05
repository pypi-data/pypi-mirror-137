from django.apps import AppConfig
from django.utils.translation import gettext_lazy

__all__ = ["DjQiYuTplConfig"]


class DjQiYuTplConfig(AppConfig):
    name = "dj_qiyu_tpl"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.verbose_name = gettext_lazy("QiYuTech Template")
