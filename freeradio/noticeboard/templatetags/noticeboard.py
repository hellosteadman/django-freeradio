from django.template import Library
from ..settings import SIZES
from ..helpers import fill_area


register = Library()


@register.filter
def partone(notices):
    part = list(fill_area(notices, 16))
    register.start_from = len(part)
    return part


@register.filter
def parttwo(notices):
    return fill_area(notices, 16, register.start_from)


@register.filter
def percentageof(value, of):
    return float(value) / float(of) * 100.0


@register.filter
def multipliedby(value, by):
    return value * by
