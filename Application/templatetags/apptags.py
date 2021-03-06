from django import template
from random import sample

from Application.utilities.web_utilitites import clean_html, reconvert_html
from Application.service.item_services import get_status_by_user_item

register = template.Library()
colors = [
        "#F44336",
        "#E91E63",
        "#9C27B0",
        "#673AB7",
        "#3F51B5",
        "#2196F3",
        "#03A9F4",
        "#00BCD4",
        "#009688",
        "#4CAF50",
        "#8BC34A",
        "#CDDC39",
        "#FFEB3B",
        "#FFC107",
        "#FF9800",
        "#FF5722",
        "#795548",
        "#9E9E9E",
        "#607D8B"
    ]


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data[key]


@register.simple_tag
def pretty_text(text):
    return reconvert_html(text)


@register.simple_tag
def reduce_text(text):
    return clean_html(text)[:150]


@register.simple_tag
def reduce_title(text):
    return text[:50] + "..."


@register.simple_tag
def list_colors(number):
    color = ""

    voted = sample(colors, number)
    for v in voted:
        color += "'{}',".format(v)

    return color


@register.simple_tag
def random_color():
    voted = sample(colors, 1)
    return voted[0]


@register.inclusion_tag('tags/card.html')
def show_card(user_id, title, image, pubDate, description, color_primary, item_id, newspaper=None, feed_id=None):
    if item_id is None:
        return {'error': True}
    else:
        status = get_status_by_user_item(user_id, item_id)[0]
        if status.like:
            color = "green lighten-4"
        elif status.saves:
            color = "blue-grey lighten-4"
        elif status.view:
            color = "grey lighten-4"
        else:
            color = ""

        return {'title': title,
                'image': image,
                'pubDate': pubDate,
                'description': description,
                'item_id': item_id,
                'color_primary': color_primary,
                'newspaper': newspaper if newspaper else "",
                'feed_id': feed_id if newspaper else "",
                'error': False,
                'color': color}


@register.inclusion_tag('tags/pagination.html')
def show_pagination(news, color_primary):
    return {'news': news, 'color_primary': color_primary}
