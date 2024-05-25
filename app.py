import streamlit as st
from gensim.models import word2vec
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from function.preprocessing import NormalizeText
from function.embedding import PatchEmbedding, MeanVectorizer
from sklearn.preprocessing import LabelEncoder


# import h5 model and corpus
with open('./model/text_classify_tokenizer.pkl', 'rb') as f:
    classify_tokenizer = pickle.load(f)

classify_model = load_model('./model/text_classify_model.h5')
word_model = word2vec.Word2Vec.load('./model/word.model')
news = pd.read_csv('./data/vnexpress/csv/cleaned_vnexpress.csv').drop(columns=['Unnamed: 0'])

# define user-defined class
normalizer = NormalizeText(tokenizer=classify_tokenizer, max_length=12731)
pemb = PatchEmbedding(word_model=word_model, stopword_path="./data/vietnamese-stopwords-dash.txt")

# GUI
st.set_page_config(layout="wide")
st.title("Sporting Magazine Looker")

# Processing
text = st.text_input("Context sentence", placeholder="Việt Nam")

if st.button("Search news"):
    temp = normalizer.normalize(text)
    temp = normalizer.create_input(temp)
    prediction = classify_model.predict(temp)
    
    # Identiy class (topic)
    label_encoder = LabelEncoder()
    label_encoder.fit(news['topic'])
    topic_class = label_encoder.inverse_transform([np.argmax(prediction[0])])
    st.text(f'Topic: {topic_class[0]}')
    
    # Find similar objects
    input_gensim = normalizer.create_input_gensim(news, 'tag')
    mvectorize = MeanVectorizer(word_model=word_model)
    question_embeddings = pemb.sentence_embedding(text)
    post_embeddings = pemb.post_embedding(input_gensim, length=len(input_gensim))

    mean_sentence_embedding = mvectorize.mean_vector_embedding(question_embeddings)
    mean_post_embedding = mvectorize.mean_posts_embedding(post_embeddings)
    
    mean_sentence_embedding = mvectorize.mean_vector_embedding(question_embeddings)
    mean_post_embedding = mvectorize.mean_posts_embedding(post_embeddings)
    similarity_score = mvectorize.text_cosine_similarity(mean_sentence_embedding, mean_post_embedding)
    similar_news = mvectorize.find_similarity(similarity_score, news)
    similar_news.drop(columns=['tag','sub-topic'], inplace=True)
    st.write(similar_news)