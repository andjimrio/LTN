from bs4 import BeautifulSoup


# Convierte un texto en formato HTML a texto plano
def clean_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.text
