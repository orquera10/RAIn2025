from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pandas as pd

# Leer el archivo .txt
with open("texto1.txt", "r", encoding="utf-8") as archivo:
    texto1 = archivo.read()

# Tokenizar solo palabras
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(texto1.lower())

# Eliminar stopwords
stop_words = set(stopwords.words('spanish'))
tokens_filtrados = [word for word in tokens if word not in stop_words]

# Stemming con Snowball (soporta español)
stemmer = SnowballStemmer('spanish')
stems = [stemmer.stem(word) for word in tokens_filtrados]

# Mostrar comparación
df = pd.DataFrame({
    'Palabra original': tokens_filtrados,
    'Raíz (SnowballStemmer)': stems
})

print(df.drop_duplicates().head(30))  # Mostrar primeras 30 filas distintas
