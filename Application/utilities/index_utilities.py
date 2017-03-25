from whoosh import index
from whoosh.qparser import QueryParser
from os.path import join,dirname,abspath,exists
from haystack.query import SearchQuerySet

from Application.utilities.queries_utilities import exists_feeds_title_by_user

PROJECT_DIR = dirname(dirname(dirname(abspath(__file__))))
INDEX = join(PROJECT_DIR,"LTNews","whoosh_index")

def get_index():
    if not exists(INDEX):
        ix = False
    else:
        ix = index.open_dir(INDEX)
    return ix

def query_search(ix,field,search):
    query = QueryParser(field, ix.schema).parse(search)
    results = ix.searcher().search(query)
    return results

def close_query(ix):
    ix.searcher().close()
    pass

def keywords(id):
    ix = get_index()
    if ix == False:
        return []
    results = query_search(ix, "ide", str(id))
    keywords = [keyword for keyword, score
                in results.key_terms("article", numterms=20)]
    close_query(ix)

    return keywords

def identity(item,user_id):
    more_results_set = SearchQuerySet().more_like_this(item).all()
    more_results = [new.object for new in more_results_set if exists_feeds_title_by_user(user_id,new.object.feed.id)]

    return more_results


if __name__ == '__main__':
    print(keywords(70))
    print(identity(72))