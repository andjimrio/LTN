from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_pagination(page, query):
    paginator = Paginator(query, 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return news