import string
from django.template import Library

register = Library()


@register.filter(name='digit_to_alpha')
def digit_to_alpha(value: int) -> str:
    return string.ascii_lowercase[value]
