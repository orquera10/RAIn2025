import nltk

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

# Leer el archivo .txt
with open("texto1.txt", "r", encoding="utf-8") as archivo:
    texto1 = archivo.read()

# Tokenizador que sólo agarra palabras (evita signos de puntuación)
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(texto1.lower())

# Stopwords en español
stop_words = set(stopwords.words('spanish'))
tokens_limpios = [t for t in tokens if t not in stop_words]

# Frecuencia de términos
frecuencia = FreqDist(tokens_limpios)

# Mostrar las 20 palabras más frecuentes
print("Términos más frecuentes:")
for palabra, freq in frecuencia.most_common(20):
    print(f"{palabra}: {freq}")

# Gráfico de barras
plt.figure(figsize=(12, 6))
frecuencia.plot(20, title="Top 20 términos más frecuentes (sin stop-words)", cumulative=False)
plt.xlabel("Palabras")
plt.ylabel("Frecuencia")
plt.grid(axis='y')
plt.show()
