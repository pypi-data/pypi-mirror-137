# This file is type hint for Django Template
#
# You need use this PyCharm plugin for proper work:
# https://plugins.jetbrains.com/plugin/18232-typed-django-template
#

from typing import Union, List

from django.core.paginator import Page

page: Page

page_range: List[Union[int, Ellipsis]]

query: str  # URL other query except page & page_size
