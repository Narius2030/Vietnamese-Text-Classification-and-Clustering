from sklearn.metrics.pairwise import cosine_similarity
from pyvi import ViTokenizer
import pandas as pd
import numpy as np



def embedding(word_model, question:str, input_gensim:list):
    question_tokens = ViTokenizer.tokenize(question)
    print('After tonkenized:', question_tokens)

    # Word embeddings
    question_embeddings = [word_model.wv[word] for word in question_tokens.split() if word in word_model.wv]

    # Post embeddings
    post_check = input_gensim[:]

    post_embeddings = []
    for post in post_check:
        post_embedding = [word_model.wv[word] for word in post if word in word_model.wv]
        post_embeddings.append(post_embedding)

    return question_embeddings, post_embeddings

# Calculate sentence embeddings by averaging word embeddings
def mean_vector_embedding(word_model, embeddings:list):
    if len(embeddings) == 0:
        return np.zeros(word_model.vector_size)
    return np.mean(embeddings, axis=0)

def mean_embedded_posts(word_model, post_embeddings:list) -> list:
    mean_post_embedding = []
    for post_embedding in post_embeddings:
        mean_post_embedding.append(mean_vector_embedding(word_model, post_embedding))

    return mean_post_embedding

def text_cosine_similarity(mean_sentence_embedding, mean_post_embedding):
    similarity_score = cosine_similarity([mean_sentence_embedding], mean_post_embedding)
    return similarity_score

def find_similarity(similarity_score, data):
    # Convert the list of lists into a numpy array
    np_similarity_score = np.array(similarity_score)
    print('np_similarity_scores', np_similarity_score)
    # Sort the array in ascending order
    sorted_indices = np.argsort(np_similarity_score[0])[::-1]

    # Get the top 5 indices
    top_5_indices = sorted_indices[:5]

    # Print the sorted indices and the top 5 indices
    print("Sorted Indices:", sorted_indices)
    print("Top 5 Indices:", top_5_indices)
    
    return data.loc[top_5_indices.tolist(), :]