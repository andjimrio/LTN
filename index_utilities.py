from whoosh import index
from whoosh.qparser import QueryParser
from os.path import join,dirname,abspath

PROJECT_DIR = dirname(abspath(__file__))
INDEX = join(PROJECT_DIR,"LTNews/whoosh_index")

def keywords(id):
    ix = index.open_dir(INDEX)
    parser = QueryParser("ide", ix.schema)
    myquery=parser.parse(str(id))
    with ix.searcher() as searcher:
        results=searcher.search(myquery)
        keywords = [keyword for keyword, score
                in results.key_terms("article", numterms=20)]
    ix.searcher().close()
    return keywords

def identity(id):
    ix = index.open_dir(INDEX)
    parser = QueryParser("ide", ix.schema)
    myquery=parser.parse(str(id))
    with ix.searcher() as searcher:
        results=searcher.search(myquery)
        first_hit = results[0]
        more_results = [more['ide'] for more in first_hit.more_like_this("article")]
    ix.searcher().close()
    return more_results

if __name__ == '__main__':
    print(keywords(70))
    print(identity(10))