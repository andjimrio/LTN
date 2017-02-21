from whoosh import index
from whoosh.qparser import QueryParser
from os.path import join,dirname,abspath,exists

PROJECT_DIR = dirname(dirname(abspath(__file__)))
INDEX = join(PROJECT_DIR,"LTNews/whoosh_index")

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

def identity(id):
    ix = get_index()
    if ix == False:
        return []
    results = query_search(ix, "ide", str(id))
    first_hit = results[0]
    more_results = [more['ide'] for more in first_hit.more_like_this("article")]
    close_query(ix)

    return more_results


if __name__ == '__main__':
    print(keywords(70))
    print(identity(72))