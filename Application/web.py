from newspaper import Article

def get_article(link):
    article = Article(link, language='es')
    article.download()
    article.parse()
    return article

if __name__ == '__main__':
    LINK_ELPAIS='http://internacional.elpais.com/internacional/2016/12/29/actualidad/1483012496_387362.html'
    article = get_article(LINK_ELPAIS)
    print(article.text)