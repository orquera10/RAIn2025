import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from urllib.parse import urljoin
import re

# ↓ solo la primera vez
nltk.download('punkt')
nltk.download('stopwords')

BASE_URL = "https://www.infobae.com/economia/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_noticias_urls(base_url, cantidad=10):
    res = requests.get(base_url, headers=HEADERS)
    soup = BeautifulSoup(res.content, 'html.parser')
    urls = set()

    for a in soup.find_all("a", href=True):
        href = a['href']
        if (
            "/economia/" in href
            and not href.endswith("/economia/")
            and "/economia/divisas" not in href  # <<< filtrado
        ):
            full_url = urljoin(base_url, href.split("?")[0])
            if full_url not in urls:
                urls.add(full_url)
            if len(urls) >= cantidad:
                break
    return list(urls)


def get_info_noticia(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.content, "html.parser")

        titulo = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
        resumen = soup.find("h2").get_text(strip=True) if soup.find("h2") else ""
        
        autor_tag = soup.find("a", class_="author-name")
        autor = autor_tag.get_text(strip=True) if autor_tag else "Desconocido"


        imagenes = [img['src'] for img in soup.find_all("img", src=True)]
        cuerpo = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))

        return {
            "url": url,
            "titulo": titulo,
            "resumen": resumen,
            "autor": autor,
            "imagenes": imagenes,
            "cuerpo": cuerpo
        }
    except Exception as e:
        print(f"Error con {url}: {e}")
        return None

# Tokenización, limpieza y análisis
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto

def procesar_textos(noticias):
    todos_los_textos = " ".join([n["titulo"] + " " + n["resumen"] + " " + n["cuerpo"] for n in noticias])
    limpio = limpiar_texto(todos_los_textos)
    tokens = word_tokenize(limpio, language='spanish')
    return tokens

def analizar_frecuencias(tokens, aplicar_stemming=False):
    stop_words = set(stopwords.words("spanish"))
    tokens_limpios = [t for t in tokens if t not in stop_words and len(t) > 2]

    if aplicar_stemming:
        stemmer = SnowballStemmer("spanish")
        tokens_limpios = [stemmer.stem(t) for t in tokens_limpios]

    return Counter(tokens_limpios).most_common(100)

# ---- MAIN ----
urls = get_noticias_urls(BASE_URL, cantidad=10)
noticias = []
for url in urls:
    info = get_info_noticia(url)
    if info:
        noticias.append(info)


tokens = procesar_textos(noticias)

frecuentes_sin_stem = analizar_frecuencias(tokens, aplicar_stemming=False)
frecuentes_con_stem = analizar_frecuencias(tokens, aplicar_stemming=True)

# Mostrar resultados
print("🔹 100 términos más frecuentes (sin stemming):")
for palabra, freq in frecuentes_sin_stem:
    print(f"{palabra}: {freq}")

print("\n🔸 100 términos más frecuentes (con stemming):")
for palabra, freq in frecuentes_con_stem:
    print(f"{palabra}: {freq}")
