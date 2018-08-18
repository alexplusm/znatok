from django import template
import re

register = template.Library()

buffer_hide_number = ['1.34.1-a',
                      '1.34.1-b',
                      '1.34.1-a',
                      '1.34.2-a',
                      '1.34.2-b',
                      '1.34.3-a',
                      '5.15.2_A',
                      '5.15.2_B',
                      '5.15.2_C',
                      '5.15.2_D',
                      '5.15.3_A',
                      '5.15.3_B',
                      '5.15.4_A',
                      '5.15.7_A',
                      '6.9.1_A',
                      '6.9.1_B',
                      '6.9.1_C',
                      '6.9.1_D',
                      '6.9.2_A',
                      '6.9.2_B',
                      '6.10.1_A',
                      '6.10.1_B',
                      '6.10.1_C',
                      '6.10.1_D',
                      '6.10.2_A',
                      '6.11_A',
                      '6.12_B',
                      '6.14.1_D',
                      '6.14.2_A',
                      '6.14.2_B']


@register.simple_tag
def sign_number(img_src):
    # TODO: можно лучше но я довн
    name = re.findall(r'\d+\.\d+.+', img_src)[0].replace('.png', '')
    mod_name = '_'
    if name in buffer_hide_number:
        return ''
    if name[len(name) - 2] == '-' or name[len(name) - 2] == '_':
        mod_name = re.sub('[_\-bcdeABCDE]', '', name)
    if mod_name[len(mod_name) - 1] == 'v':
        return re.sub('[_v]', '', mod_name) + '\n(временный)'
    if len(mod_name) > 1:
        return mod_name
    return name
