from nltk.corpus import brown
from nltk.tokenize import regexp_tokenize


# Cargar el archivo cg73 del corpus Brown
texto = brown.raw('cg73')

# Tokenizar el texto en oraciones utilizando expresiones regulares (alternativa a sent_tokenize)
oraciones = regexp_tokenize(texto, pattern=r'\S.+?[.!?]', gaps=False)
# Mostrar las primeras 10 oraciones
for i in range(10):
    print(f"Oración {i + 1}: {oraciones[i]}")