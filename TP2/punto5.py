import nltk
from nltk.corpus import brown
import re

nltk.download('brown')

# Cargar el archivo cg73 del corpus Brown
texto = brown.raw('cg73')

# Dividir el texto en oraciones (usando signos de puntuación como separadores)
oraciones = re.split(r'(?<=[.!?])\s+', texto)

# Función para limpiar las etiquetas POS (dejar solo las palabras)
def limpiar_etiquetas(oracion):
    palabras = oracion.split()
    palabras_limpias = [palabra.split('/')[0] for palabra in palabras if '/' in palabra]
    return ' '.join(palabras_limpias)

# Mostrar las primeras 10 oraciones limpias
for i in range(10):
    oracion_limpia = limpiar_etiquetas(oraciones[i])
    print(f"Oración {i + 1}: {oracion_limpia}")


