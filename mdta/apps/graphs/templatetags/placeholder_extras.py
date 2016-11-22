from django import template

register = template.Library()


@register.simple_tag
def placeholder_format(key, name):
    data = ''
    if key == 'NoInput_1':
        data = name + '_NI1'
    elif key == 'NoInput_2':
        data = name + '_NI2'
    elif key == 'NoMatch_1':
        data = name + '_NM1'
    elif key == 'NoMatch_2':
        data = name + '_NM2'

    return data
