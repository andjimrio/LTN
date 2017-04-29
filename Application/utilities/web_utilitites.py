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