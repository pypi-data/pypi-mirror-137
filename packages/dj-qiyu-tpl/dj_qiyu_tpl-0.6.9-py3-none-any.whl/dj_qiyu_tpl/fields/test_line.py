from django.forms import CharField, Form

from .custom import CustomFormField
from ..forms import CustomForm


class DemoCharForm(Form):
    char = CharField(
        max_length=100, min_length=10, label="测试", help_text="这是一个测试的字段"
    )  # noqa


class BulmaLineForm(CustomForm):
    char = CustomFormField(
        max_length=100, min_length=10, label="测试", help_text="这是一个测试的字段"
    )


def test_bulma_line_field():
    form = BulmaLineForm(data={"char": "hello world"})
    p = form.as_p()
    print(p)
