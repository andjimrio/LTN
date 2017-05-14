from bs4 import BeautifulSoup


# Convierte un texto en formato HTML a texto plano
def clean_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.text


def extract_img_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    imgs = []
    for img in soup.findAll("img"):
        imgs.append(img['src'])

    return imgs[0]


def reconvert_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    first_img = soup.find('img')
    if first_img:
        first_img['src'] = ''

    for img in soup.findAll("img"):
        img['class'] = img.get('class', []) + ['responsive-img']

    for p in soup.findAll("p"):
        p['class'] = p.get('class', []) + ['justify']

    for div in soup.findAll("div"):
        div['class'] = div.get('class', []) + ['center']

    return soup.prettify("utf-8")
