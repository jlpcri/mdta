from django import template

register = template.Library()


@register.simple_tag
def placeholder_format(key, name):
    data = ''
    # name = '{prompt}'
    if key == 'NoInput_1':
        data = name + 'NI1'
    elif key == 'NoInput_2':
        data = name + 'NI2'
    elif key == 'NoMatch_1':
        data = name + 'NM1'
    elif key == 'NoMatch_2':
        data = name + 'NM2'
    elif key == 'OnFailGoTo':
        data = '{nodeName}'

    return data
