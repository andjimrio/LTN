from collections import Counter
from math import floor, log

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from Application.forms import ItemSearchForm
from Application.utilities.queries_utilities import get_item, get_last_items_by_user, get_status_by_user_item,\
    get_item_today_by_section, get_sections_by_user
from Application.utilities.index_utilities import get_item_keywords, get_item_similarity, get_item_query, \
    get_item_recommend, query_multifield_dict


@login_required
def item_view(request, item_id=None):
    like = request.GET.get('like')

    item = get_item(item_id)
    tags = get_item_keywords(item_id, item.get_key_number())
    news = get_item_similarity(item_id, 6)

    status = get_status_by_user_item(request.user.id, item_id)
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
    actual = request.GET.get('actual')
    page = request.GET.get('page')
    paginator = Paginator(get_last_items_by_user(request.user.id), 20)

    if actual is not None:
        ids = [x['item_id'] for x in paginator.page(actual)]
        for item_id in ids:
            status = get_status_by_user_item(request.user.id, item_id)
            status.as_view()

        if page is not None:
            page = int(page)-1

    try:
        feedes = paginator.page(page)
    except PageNotAnInteger:
        feedes = paginator.page(1)
    except EmptyPage:
        feedes = paginator.page(paginator.num_pages)

    return render(request, 'item/item_list.html', {'feedes': feedes})


@login_required
def item_query(request, query):
    page = request.GET.get('page')
    paginator = Paginator(get_item_query(query), 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'item/item_query.html', {'news': news, 'query': query})


@login_required
def item_recommend(request):
    page = request.GET.get('page')
    paginator = Paginator(get_item_recommend(request.user.id), 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'item/item_recommend.html', {'news': news})


@login_required
def item_search(request):
    page = request.GET.get('page')
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
        print(cleaned_data)
        query = query_multifield_dict(cleaned_data)
        paginator = Paginator(query, 20)

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
            total = len(query)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

    return render(request, 'item/item_search.html', {'news': news, 'form': search_form, 'total': total})


@login_required
def item_summary(request):
    summary_keywords = dict()
    for section in get_sections_by_user(request.user.id):
        section_summary_keywords = SectionSummaryKeywords(section.title)
        for item in get_item_today_by_section(section.id):
            for keyword in get_item_keywords(item['feeds__items__id'], 8):
                section_summary_keywords.add_keyword(keyword, item['feeds__items__id'], item['feeds__items__title'])

        summary_keywords[section.title] = section_summary_keywords.most_common()

    return render(request, 'item/item_summary.html', {'summary_keywords': summary_keywords})


class SectionSummaryKeywords:
    def __init__(self, section_title):
        self.section = section_title
        self.keywords_counters = dict()
        self.counts_counters = Counter()

    def add_keyword(self, keyword, item_id, item_title):
        if keyword in self.keywords_counters:
            self.keywords_counters[keyword].update(item_id, item_title)
        else:
            keyword_counter = KeywordCounter(keyword, item_id, item_title)
            self.keywords_counters[keyword] = keyword_counter

        self.counts_counters[keyword] += 1

    def most_common(self, number=None):
        if not number:
            number = floor(log(len(self.counts_counters)))
        return [self.keywords_counters[keyword[0]] for keyword in self.counts_counters.most_common(number)]

    def __str__(self):
        return "SSK: {} - {}".format(self.section, len(self.keywords_counters))


class KeywordCounter:
    def __init__(self, keyword, item_id, item_title):
        self.keyword = keyword
        self.counts = 1
        self.sample_title = item_title
        self.items = dict()
        self.items[item_id] = item_title

    def update(self, item_id, item_title):
        self.counts += 1
        self.items[item_id] = item_title

    def __str__(self):
        return "KC: {} - {}".format(self.keyword, self.counts)
    pass
