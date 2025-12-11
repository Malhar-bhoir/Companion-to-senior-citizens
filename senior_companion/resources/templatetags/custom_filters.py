from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """ Allows dictionary lookup using dictionary|get_item:key """
    return dictionary.get(key)

@register.filter(name='replace_underscore')
@stringfilter
def replace_underscore(value):
    """ Replaces underscores with spaces and capitalizes. """
    if isinstance(value, str):
        return value.replace('_', ' ').capitalize()
    return value

# Note: You can now use these filters in any template after adding {% load custom_filters %}