from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Application.forms import ItemSearchForm
from Application.service.item_services import get_item, get_last_items_by_user, get_status_by_user_item,\
    get_item_today_by_section, get_item_query, get_item_keywords, get_item_similarity, query_multifield_dict, \
    get_item_recommend, SectionSummaryKeywords, stats_items
from Application.service.section_services import get_sections_by_user
from Application.services import get_pagination


@login_required
def item_view(request, item_id=None):
    like = request.GET.get('like')

    item = get_item(item_id)
    tags = get_item_keywords(item_id, item.get_key_number())
    news = get_item_similarity(item_id, 6)

    status = get_status_by_user_item(request.user.id, item_id)[0]
    status.as_read()

    if like == 'True':
        status.as_like()
    elif like == 'False':
        status.as_unlike()

    return render(request, 'item/item_view.html',
                  {'item': item, 'tags': tags, 'news': news,
                   'status': status})


@login_required
def item_list(request):
    follow = request.GET.get('follow')

    if follow is not None:
        for item_id in request.session.get('news_ids', []):
            status = get_status_by_user_item(request.user.id, item_id)[0]
            status.as_view()

    news = get_pagination(request.GET.get('page'), get_last_items_by_user(request.user.id))
    request.session['news_ids'] = [x['item_id'] for x in news]

    return render(request, 'item/item_list.html', {'news': news})


@login_required
def item_query(request, query):
    queryset = get_item_query(query)
    news = get_pagination(request.GET.get('page'), queryset)
    stats = stats_items(queryset)

    return render(request, 'item/item_query.html', {'news': news, 'query': query, 'stats': stats})


@login_required
def item_recommend(request):
    news = get_pagination(request.GET.get('page'), get_item_recommend(request.user.id))

    return render(request, 'item/item_recommend.html', {'news': news})


@login_required
def item_search(request):
    news = None
    total = 0
    cleaned_data = request.session.get('cleaned_data', None)

    if request.method == 'POST':
        search_form = ItemSearchForm(request.user, request.POST)

        if search_form.is_valid():
            cleaned_data = search_form.cleaned_data
            if cleaned_data['feed']:
                cleaned_data['feed'] = cleaned_data['feed'].title
            request.session['cleaned_data'] = search_form.cleaned_data

        else:
            print(search_form.errors)
    elif cleaned_data:
        search_form = ItemSearchForm(request.user, initial=cleaned_data)
    else:
        search_form = ItemSearchForm(request.user)

    if cleaned_data:
        query = query_multifield_dict(cleaned_data)
        total = len(query)
        news = get_pagination(request.GET.get('page'), query)

    return render(request, 'item/item_search.html', {'news': news, 'form': search_form, 'total': total})


@login_required
def item_summary(request):
    summary_keywords = dict()
    for section in get_sections_by_user(request.user.id):
        section_summary_keywords = SectionSummaryKeywords(section.title)
        for item in get_item_today_by_section(section.id, hours=3):
            keywords = get_item_keywords(item['feeds__items__id'], 8)
            section_summary_keywords.add_keyword(keywords, item['feeds__items__id'], item['feeds__items__title'])

        summary_keywords[section.title] = section_summary_keywords.most_common()

    return render(request, 'item/item_summary.html', {'summary_keywords': summary_keywords})
