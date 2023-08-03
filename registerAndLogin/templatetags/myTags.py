from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def filter0Count(countNum):
    if 0 == int(countNum):
        return ''
    else:
        return countNum