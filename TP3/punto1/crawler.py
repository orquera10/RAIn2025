import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = 'https://www.infobae.com/deportes'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

import re
from urllib.parse import urljoin

def is_valid_article(link):
    """
    Verifica si un link apunta a un artículo válido de la sección deportes.
    Acepta URLs absolutas o relativas con fecha en el path y excluye
    galerías, videos y fotos.
    """
    # Limpieza básica: remover parámetros y anchors
    clean_link = link.split('?')[0].split('#')[0]

    # Verifica que el link sea un artículo con fecha
    if (
        re.match(r'^/deportes/\d{4}/\d{2}/\d{2}/', clean_link) or
        re.match(r'^https://www\.infobae\.com/deportes/\d{4}/\d{2}/\d{2}/', clean_link)
    ):
        # Excluir tipos de contenido no deseado
        if not any(x in clean_link for x in ['/galeria-', '/video-', '/fotos-']):
            return True
    return False

def get_full_url(path):
    return urljoin(BASE_URL, path)

FULL_URL_EXCLUDE = 'https://www.infobae.com/deportes/'

def get_initial_articles(limit=30):
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = set()

    for a in soup.find_all('a', href=True):
        href = a['href']
        if is_valid_article(href):
            full_url = get_full_url(href).rstrip('/')
            if full_url != FULL_URL_EXCLUDE.rstrip('/'):
                article_links.add(full_url)
        if len(article_links) >= limit:
            break
    return list(article_links)

def get_internal_links(article_url):
    try:
        response = requests.get(article_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.select('[data-section="deportes"] a, a[href*="/deportes/"]'):
            href = a['href']
            if is_valid_article(href):
                full_url = get_full_url(href).rstrip('/')
                if full_url != FULL_URL_EXCLUDE.rstrip('/'):
                    links.append(full_url)
        return links
    except Exception as e:
        print(f"Error with {article_url}: {e}")
        return []


def crawl_articles(initial_urls):
    graph_data = {}
    visited = set()

    # Procesar los artículos iniciales (nivel 1)
    for url in initial_urls:
        normalized_url = url.rstrip('/')
        if normalized_url in visited:
            continue
        time.sleep(1)
        visited.add(normalized_url)

        internal_links = get_internal_links(normalized_url)
        cleaned_links = [link.rstrip('/') for link in internal_links]

        graph_data[normalized_url] = cleaned_links

    # Ahora agregar esos enlaces nuevos encontrados, pero sin profundizar
    # O sea, para cada enlace interno nuevo no se extraen sus links internos,
    # sólo se agregan como nodos sin links hijos
    new_links = set()
    for links in graph_data.values():
        for link in links:
            if link not in visited:
                new_links.add(link)

    for link in new_links:
        if link not in visited:
            visited.add(link)
            graph_data[link] = []  # No extraemos links internos de estos

    return graph_data




