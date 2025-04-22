# ============================
# 📦 LIBRERÍAS Y DESCARGAS
# ============================
import nltk
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')

from nltk.corpus import brown, stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter
import pandas as pd

# ============================
# A. ELIMINACIÓN DE RUIDO
# ============================

# Cargar el texto del archivo 'cg73'
raw_text = brown.words(fileids='cg73')

# Eliminar puntuación y caracteres no alfabéticos
text_clean = [word for word in raw_text if word.isalpha()]

# ============================
# B. TOKENIZACIÓN
# ============================

# Ya está tokenizado, solo seguimos con la lista limpia
tokens = text_clean

# ============================
# C. NORMALIZACIÓN
# ============================

# Pasar todo a minúsculas
tokens_norm = [word.lower() for word in tokens]

# ============================
# D. ELIMINACIÓN DE STOPWORDS
# ============================

stop_words = set(stopwords.words('english'))
tokens_no_stop = [word for word in tokens_norm if word not in stop_words]

# ============================
# E. TOP 50 PALABRAS FRECUENTES
# ============================

freq_50 = Counter(tokens_no_stop).most_common(50)
print("\nE. 50 palabras más frecuentes (sin stopwords):")
print(freq_50)

# ============================
# F. STEMMING
# ============================

stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(word) for word in tokens_no_stop]
freq_stemmed_50 = Counter(stemmed_tokens).most_common(50)
print("\nF. 50 palabras más frecuentes (Stemming):")
print(freq_stemmed_50)

# ============================
# G. LEMATIZACIÓN
# ============================

lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens_no_stop]
freq_lemmatized_50 = Counter(lemmatized_tokens).most_common(50)
print("\nG. 50 palabras más frecuentes (Lematización):")
print(freq_lemmatized_50)

# ============================
# H. LEMATIZACIÓN CON PoS
# ============================

# Función para mapear etiquetas PoS
def get_wordnet_pos(tag):
    if tag.startswith('V'):
        return wordnet.VERB
    return wordnet.NOUN  # Por defecto

# Etiquetado PoS
pos_tags = nltk.pos_tag(tokens_no_stop)

# Lematización considerando PoS
lemmatized_pos = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags]
freq_lemmatized_pos_50 = Counter(lemmatized_pos).most_common(50)
print("\nH. 50 palabras más frecuentes (Lematización con PoS):")
print(freq_lemmatized_pos_50)

# ============================
# I. TABLA DE PRIMEROS 30 TOKENS
# ============================

data = {
    "Token": tokens_no_stop[:30],
    "Stemming": [stemmer.stem(w) for w in tokens_no_stop[:30]],
    "Lematización": [lemmatizer.lemmatize(w) for w in tokens_no_stop[:30]],
    "Lematización_Pos": [
        lemmatizer.lemmatize(w, get_wordnet_pos(tag))
        for (w, tag) in nltk.pos_tag(tokens_no_stop[:30])
    ]
}

df = pd.DataFrame(data)

print("\nI. Tabla de los primeros 30 tokens con transformaciones:")
print(df)
