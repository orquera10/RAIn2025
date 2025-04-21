from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer, LancasterStemmer
import pandas as pd


# Leer el archivo .txt
with open("texto2.txt", "r", encoding="utf-8") as archivo:
    texto2 = archivo.read()

# Tokenizador por expresiones regulares (solo palabras alfabéticas)
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(texto2.lower())

# Stopwords
stop_words = set(stopwords.words("english"))
tokens_filtrados = [word for word in tokens if word not in stop_words]

# Stemming
porter = PorterStemmer()
lancaster = LancasterStemmer()
porter_stems = [porter.stem(word) for word in tokens_filtrados]
lancaster_stems = [lancaster.stem(word) for word in tokens_filtrados]

# DataFrame
df = pd.DataFrame({
    'Original': tokens_filtrados,
    'Porter Stemmer': porter_stems,
    'Lancaster Stemmer': lancaster_stems
})
# Mostrar las primeras 30 filas únicas
print(df.drop_duplicates().head(30))