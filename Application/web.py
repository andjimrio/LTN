from urllib.request import urlopen
from bs4 import BeautifulSoup
from newspaper import Article

def read_web(link):
    web = urlopen(link)
    html_doc = web.read()
    return html_doc

def read_all_text(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return "\n".join(ps.getText() for ps in soup.find_all('p'))

def get_images(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    article = soup.find('article')
    if article == None:
        article = soup
    return [img['src'] for img in article.find_all('img') if 'http' in img['src']]

def read_main_content(link):
    html = read_web(link)
    web = read_all_text(html)
    image = get_images(html)[0] if len(get_images(html)) > 0 else ""
    print(get_images(html))
    return web,image

def get_article(link):
    article = Article(link, language='es')
    article.download()
    article.parse()
    return article

if __name__ == '__main__':
    LINK_ELPAIS='http://internacional.elpais.com/internacional/2016/12/29/actualidad/1483012496_387362.html'
    article = get_article(LINK_ELPAIS)
    print(article.text)