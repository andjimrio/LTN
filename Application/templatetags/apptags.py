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


@register.simple_tag
def reduce_text(text):
    if len(text)>150:
        return text[:text.find('.')+1]
    else:
        return text


@register.simple_tag
def reduce_title(text):
    return text[:50] + "..."


@register.inclusion_tag('tags/card.html')
def show_card(title, image, pubDate, description, color_primary, item_id, newspaper=None, feed_id=None):
    return {'title':title,
            'image':image,
            'pubDate':pubDate,
            'description':description,
            'item_id':item_id,
            'color_primary':color_primary,
            'newspaper':newspaper if newspaper != None else "",
            'feed_id':feed_id if newspaper != None else ""}

@register.inclusion_tag('tags/pagination.html')
def show_pagination(news,color_primary):
    return {'news':news,'color_primary':color_primary}