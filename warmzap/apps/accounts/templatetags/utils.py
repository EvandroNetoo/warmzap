from django import template

register = template.Library()


@register.filter(name='removesuffix')
def removesuffix(value: str, suffix: str) -> str:
    return value.removesuffix(suffix)


@register.filter(name='sub')
def sub(minuend, subtrahend):
    return minuend - subtrahend
