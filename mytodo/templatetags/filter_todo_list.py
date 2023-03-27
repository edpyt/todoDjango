from django import template


register = template.Library()


@register.filter
def get_dict_item(item):
    return dir(item)
