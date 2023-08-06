import os

from django.conf import settings
from django.utils.safestring import mark_safe
from docutils.core import publish_parts

__all__ = ["RstHelper", "RST_CONFIG_DEFAULTS"]

RST_CONFIG_DEFAULTS = {
    "file_insertion_enabled": 0,
    "raw_enabled": 0,
    "_disable_config": 1,
    "language_code": "zh_cn",
    # use link style sheet
    # decrease output html size
    # [increase performance]
    "embed_stylesheet": False,
    "stylesheet_dirs": [
        os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                "../static/dj_qiyu_tpl/vendor/rst",
            )
        )
    ],
}


class RstHelper(object):
    @staticmethod
    def publish_app_doc(code: str, need_script: bool = True) -> str:
        parts = publish_parts(
            code,
            settings=None,
            settings_overrides=RST_CONFIG_DEFAULTS,
            writer_name="html5",
        )
        body = parts["html_body"]
        div = f"<div is='app-doc'>{body}</div>"
        if not need_script:
            return mark_safe(div)

        # 应该使用 django 配置中的 STATIC_URL
        # 否则 static 文件在使用 CDN 的时候会有问题
        static_url = getattr(settings, "STATIC_URL", "/static/")

        return mark_safe(
            f"""\
{div}
<script>globalThis._django_static_url = "{static_url}";</script>
<script src='{static_url}dj_qiyu_tpl/js/app_doc_node.js'></script>\
"""
        )
