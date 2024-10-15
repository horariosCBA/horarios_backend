# Importar la clase PorterStemmer del módulo nltk.stem para realizar el stemming (reducción de palabras a su raíz)
from nltk.stem.porter import PorterStemmer
import nltk
import numpy as np  # Biblioteca para operaciones numéricas con arreglos/matrices
# Descargar el paquete 'punkt_tab' de nltk, necesario para la tokenización
nltk.download('punkt_tab')

# Crear una instancia del stemmer, que será usada para reducir palabras a su forma base o raíz
stemmer = PorterStemmer()

# Función para tokenizar una oración, es decir, dividirla en una lista de palabras individuales


def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Función para aplicar stemming a una palabra. Convierte la palabra a minúsculas y luego la reduce a su raíz


def stem(word):
    return stemmer.stem(word.lower())

# Función para crear una bolsa de palabras (bag of words)
# Recibe una oración tokenizada y una lista de todas las palabras posibles ('all_words')


def bag_of_words(tokenized_sentence, all_words):
    # Aplicar stemming a cada palabra en la oración tokenizada
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    # Crear un vector de ceros del tamaño de 'all_words', donde cada posición representa si una palabra está presente o no
    bag = np.zeros(len(all_words), dtype=np.float32)
    # Marcar con un 1.0 las posiciones donde las palabras de 'all_words' están presentes en la oración tokenizada
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:  # Si la palabra de 'all_words' está en la oración tokenizada
            bag[idx] = 1.0  # Marcar la posición con un 1.0
    return bag  # Devolver el vector de bolsa de palabras
