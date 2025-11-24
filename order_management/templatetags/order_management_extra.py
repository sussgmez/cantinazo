from django import template

register = template.Library()


@register.filter
def multiply(value1, value2):
    return value1 * value2


@register.filter
def sort(object_list):

    object_list = object_list.order_by("student__pk") if object_list else None
    return object_list
