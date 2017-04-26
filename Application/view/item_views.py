from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from Application.utilities.index_utilities import get_item_keywords,get_item_similarity,get_item_query
from Application.utilities.queries_utilities import get_item,get_last_items_by_user


@login_required
def item_view(request, item_id=None):
    article = get_item(item_id)
    tags = get_item_keywords(item_id)
    news = get_item_similarity(item_id)
    return render(request, 'item/item_view.html', {'article':article, 'tags':tags, 'news':news})

@login_required
def item_list(request):
    page = request.GET.get('page')
    paginator = Paginator(get_last_items_by_user(request.user.id), 20)

    try:
        feedes = paginator.page(page)
    except PageNotAnInteger:
        feedes = paginator.page(1)
    except EmptyPage:
        feedes = paginator.page(paginator.num_pages)

    return render(request, 'item/item_list.html', {'feedes':feedes})



@login_required
def item_query(request,query):
    page = request.GET.get('page')
    paginator = Paginator(get_item_query(query), 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'item/item_query.html', {'news': news, 'query': query})
