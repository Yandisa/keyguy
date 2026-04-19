from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter. Usage: "a,b,c"|split:"," """
    return [item.strip() for item in value.split(delimiter)]
