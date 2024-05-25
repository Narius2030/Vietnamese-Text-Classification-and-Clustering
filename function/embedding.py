from sklearn.metrics.pairwise import cosine_similarity
from pyvi import ViTokenizer
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import sys
sys.path.append("./src/dtprocess")
import cleandt



class PatchEmbedding():
    def __init__(self, word_model, stopword_path=None) -> None:
        self.word_model = word_model
        self.stopword_path = stopword_path
    
    def sentence_embedding(self, sentence:str):
        # question_tokens = cleandt.remove_punctuation(sentence)
        question_tokens = ViTokenizer.tokenize(sentence)
        question_tokens = cleandt.remove_stopword(question_tokens, self.stopword_path)
        print('After tonkenized:', question_tokens)

        # sentence embeddings
        question_embeddings = [self.word_model.wv[word] for word in question_tokens.split() if word in self.word_model.wv]
        return question_embeddings

    def post_embedding(self, input_gensim:list, length=None):
        if length is None:
            length = len(input_gensim)
        
        post_check = input_gensim[:length]

        post_embeddings = []
        for post in post_check:
            post_embedding = [self.word_model.wv[word] for word in post if word in self.word_model.wv]
            post_embeddings.append(post_embedding)
        return post_embeddings
    
    def word_scatterplot(self, words=None, sample=0):
        if words == None:
            if sample > 0:
                words = np.random.choice(list(self.word_model.vocab.keys()), sample)
            else:
                words = [word for word in self.word_model.wv.vocab]
            
        word_vectors = np.array([self.word_model.wv[w] for w in words])
        
        twodim = PCA().fit_transform(word_vectors)[:,:2]
        
        fig = plt.figure(figsize=(6,5))
        plt.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c='r')
        for word, (x,y) in zip(words, twodim):
            plt.text(x+0.05, y-0.50, word)
        return fig


class MeanVectorizer(PatchEmbedding):
    def __init__(self, word_model, stopword_path=None) -> None:
        super().__init__(word_model, stopword_path)
        pass
    
    # Calculate sentence embeddings by averaging word embeddings
    def mean_vector_embedding(self, embeddings):
        if len(embeddings) == 0:
            return np.zeros(self.word_model.vector_size)
        return np.mean(embeddings, axis=0)

    def mean_posts_embedding(self, post_embeddings) -> list:
        mean_post_embedding = []
        for post_embedding in post_embeddings:
            mean_post_embedding.append(self.mean_vector_embedding(post_embedding))
        return mean_post_embedding

    def flatten_mean_embedding(self, post_embeddings):
        mean_text_embeddings = []
        for emebbed in tqdm(post_embeddings):
            temp = np.mean(emebbed, axis=1)
            mean_text_embeddings.append(list(temp))
        return mean_text_embeddings

    def text_cosine_similarity(self, mean_sentence_embedding, mean_post_embedding):
        similarity_score = cosine_similarity([mean_sentence_embedding], mean_post_embedding)
        return similarity_score

    def find_similarity(self, similarity_score, data):
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