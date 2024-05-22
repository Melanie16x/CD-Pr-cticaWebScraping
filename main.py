import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.mercadolibre.com.ar/c/autos-motos-y-otros#menu=categories'

def get_links(soup):
    return [a['href'] for a in soup.find_all('a', href=True)]

def get_content(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        page_soup = BeautifulSoup(response.text, 'html.parser')
        h1 = [str(tag) for tag in page_soup.find_all('h1')]
        p = [str(tag) for tag in page_soup.find_all('p')]

        return h1 + p
    except requests.exceptions.RequestException as e:
        print(f"No se puede acceder a {url}: {e}")
        return []

def main(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = get_links(soup)

    data = {}

    for link in links:
        print(f"Procesando {link}")
        content = get_content(link)
        data[link] = content

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent= 4)

if __name__ == '__main__':
    main(url)