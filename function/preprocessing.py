import pandas as pd
import os
import string
import numpy as np
from tqdm import tqdm
from pyvi import ViTokenizer
from tensorflow.keras import preprocessing
import sys
sys.path.append("./src/dtprocess")
import cleandt


class ConvertText():
    def __init__(self) -> None:
        pass
    
    def get_info(self, topic, processed_news):
        temp = processed_news[processed_news.topic == topic]
        return temp['article_id'].to_list(), temp['tag'].to_list()
    
    def load_data(self, path):
        ## Import data from raw folder to dataframe
        CRAWL_FOLDER = path
        vnexpress = []

        for filename in os.listdir(CRAWL_FOLDER):
            with open(f'{CRAWL_FOLDER}/{filename}', 'r') as file:
                news = file.readlines()
                vnexpress += cleandt.convert_dict(news, 'content')
        news = pd.DataFrame(columns=['content','url','topic', 'sub-topic', 'image', 'title','description'])
        
        for new in vnexpress:
            news.loc[len(news)] = pd.Series(new)
        news = news.reset_index().rename(columns={'index':'article_id'})
        return news
        
    def dump_files(self, processed_news, path):
        """Dump each tag to a text file
        """
        processed_news.to_csv(f'{path}/csv/cleaned_vnexpress.csv')
        
        PROCESSED_FOLDER = f'{path}/processed_news'
        for topic in tqdm(os.listdir(PROCESSED_FOLDER)):
            articles_ids, tags = self.get_info(topic, processed_news)
            # print(articles_ids)
            for id, tag in zip(articles_ids, tags):
                with open(f'{PROCESSED_FOLDER}/{topic}/{id}.txt', "w", encoding="utf-8") as file:
                    file.write(tag)

    def transform_texts(self, data):
        """Transform the raw data to usable text
        """
        ## Select necessary columns
        processed_news = data[['article_id','content','topic','sub-topic','title','description','url']]

        ## Find null values and processing
        processed_news.fillna('', inplace=True)
        ## Merge columns into a single `tag` column
        processed_news['tag'] = processed_news['content'] + processed_news['title'] + processed_news['description']
        processed_news = processed_news.drop(columns=['content','description'])

        ## Tokenize the Vietnamese words
        processed_news['tag'] = processed_news['tag'].apply(lambda x: x.lower())
        processed_news['tag'] = processed_news['tag'].apply(lambda x: cleandt.remove_punctuation(x))
        processed_news['tag'] = processed_news['tag'].apply(lambda x: ViTokenizer.tokenize(x))
        return processed_news
    
class NormalizeText():
    def __init__(self, max_length:int=None, tokenizer=None) -> None:
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def word_separation(self, sentences:list) -> list:
        return [sen.split() for sen in sentences]
    
    def normalize(self, doc, stopword=0) -> list:
        doc = ViTokenizer.tokenize(doc)
        doc = doc.lower() # lower
        
        if stopword==1:
            doc = cleandt.remove_stopword(doc, './data/vietnamese-stopwords-dash.txt')
        
        tokens = doc.split() # split into words
        table = str.maketrans('', '', string.punctuation.replace("_", "")) # remove all punctuations
        tokens = [w.translate(table) for w in tokens]
        tokens = [word for word in tokens if word]
        return tokens
    
    def create_sequences(self, data) -> list:
        papers = data['tag'].tolist()
        sequences = []
        for seq in tqdm(papers):
            tokens = self.normalize(seq)
            line = ' '.join(tokens)
            sequences.append(line)
        return sequences
    
    def create_input_gensim(self, data, colname:str) -> list:
        sequences = data[colname].to_list()
        input_gensim = []
        for sen in sequences:
            try:
                input_gensim.append(sen.split())
            except Exception as ex:
                pass
        return input_gensim
    
    def create_input(self, sequences:list):
        sequence_digit = self.tokenizer.texts_to_sequences(sequences)
        input_sequences = np.array(preprocessing.sequence.pad_sequences(sequence_digit, maxlen=self.max_length, padding='pre'))
        return input_sequences
    