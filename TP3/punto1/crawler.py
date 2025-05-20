import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = 'https://www.infobae.com/deportes'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def is_valid_article(link):
    return link.startswith('/deportes') and '/video' not in link and '?' not in link

def get_full_url(path):
    return urljoin(BASE_URL, path)

def get_initial_articles(limit=30):
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = set()

    for a in soup.find_all('a', href=True):
        href = a['href']
        if is_valid_article(href):
            full_url = get_full_url(href)
            article_links.add(full_url)
        if len(article_links) >= limit:
            break
    return list(article_links)

def get_internal_links(article_url):
    try:
        response = requests.get(article_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if is_valid_article(href):
                links.append(get_full_url(href))
        return links
    except Exception as e:
        print(f"Error with {article_url}: {e}")
        return []

def crawl_articles(article_urls):
    graph_data = {}
    for url in article_urls:
        time.sleep(1)  # Respetar el servidor
        internal_links = get_internal_links(url)
        graph_data[url] = internal_links
    return graph_data
