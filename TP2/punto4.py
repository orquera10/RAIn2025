from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from nltk.corpus import stopwords

# Párrafo original
parrafo = """
Los sistemas recomendadores son herramientas enfocadas a ayudar a los usuarios a 
obtener aquella información que mejor se corresponda con sus intereses y preferencias.
"""

# Tokenizar solo palabras
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(parrafo.lower())

# Eliminar stopwords en español
stopwords_es = set(stopwords.words('spanish'))
tokens_filtrados = [t for t in tokens if t not in stopwords_es]

# Obtener 2-gramas y 3-gramas
bigrams = list(ngrams(tokens_filtrados, 2))
trigrams = list(ngrams(tokens_filtrados, 3))

# Mostrar resultados
print("🔹 2-gramas:")
for bg in bigrams:
    print(" -", bg)

print("\n🔹 3-gramas:")
for tg in trigrams:
    print(" -", tg)

