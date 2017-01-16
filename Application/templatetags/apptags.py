from django import template

register = template.Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data[key]
    pass

@register.simple_tag
def pretty_text(text):
    dict = {"\n":"<br/>"}
    for k,v in dict.items():
        text = text.replace(k,v)
    return text