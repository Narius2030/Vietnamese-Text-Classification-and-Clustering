import tensorflow as tf
from pyvi import ViTokenizer
import string
import numpy as np



def clean_document(doc):
    doc = ViTokenizer.tokenize(doc) #Pyvi Vitokenizer library
    doc = doc.lower() #Lower
    tokens = doc.split() #Split in_to words
    table = str.maketrans('', '', string.punctuation.replace("_", "")) #Remove all punctuation
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]

    return tokens

def preprocess_input(doc, tokenizer):
    tokens = clean_document(doc)
    tokens = tokenizer.texts_to_sequences(tokens)

    for digit in tokens:
        if not digit:
            raise Exception("Từ vựng không tồn tại trong kho")

    tokens = tf.keras.preprocessing.sequence.pad_sequences([tokens], maxlen=50, truncating='pre')
    return np.reshape(tokens, (1,50))

def top_n_words(tokenizer, model, text_input, top_n=3):
    tokens = preprocess_input(text_input)
    predictions = model.predict(tokens)[0]

    # Lấy top k dự đoán cao nhất
    top_indices = np.argpartition(predictions, -top_n)[-top_n:]

    top_words = []
    for index in top_indices:
        for word, idx in tokenizer.word_index.items():
            if idx == index:
                top_words.append(word)
                break

    return top_words

def generate_sentences(tokenizer, model, text_input, n_words):
    tokens = preprocess_input(text_input, tokenizer)
    generated_sentences = []
    for _ in range(n_words):
        next_digit = np.argmax(model.predict(tokens, verbose=0))
        tokens = np.append(tokens, next_digit)
        tokens = np.delete(tokens, 0)
        tokens = np.reshape(tokens, (1, 50))

    # Mapping to text
    tokens = np.reshape(tokens, (50))
    # print(tokens)
    out_word = []
    for token in tokens:
        for word, index in tokenizer.word_index.items():
            if index == token:
                out_word.append(word)
                break

    return ' '.join(out_word)