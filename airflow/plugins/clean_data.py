import pandas as pd
import os
import re
import string
from tqdm import tqdm
from data_scrape.dtprocess import cleandt
from pyvi import ViTokenizer

ROOT_PATH = '/mnt/d/Programming/Vietnamese-Text-Generator'

def remove_punctuation(comment):
    # Create a translation table
    translator = str.maketrans('', '', string.punctuation)
    # Remove punctuation
    new_string = comment.translate(translator)
    # Remove redudant space and break sign
    new_string = re.sub('[\n ]+', ' ', new_string)
    # Remove emoji icon
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                            "]+", flags=re.UNICODE)
    new_string = re.sub(emoji_pattern, '', new_string)
    return new_string

def get_info(topic, processed_news):
    temp = processed_news[processed_news.topic == topic]
    return temp['article_id'].to_list(), temp['tag'].to_list()

def transform_load():
    """Transform the raw data to usable text
    """
    ## Import data from raw folder to dataframe
    CRAWL_FOLDER = f'{ROOT_PATH}/data/scraped_data/raw'
    vnexpress = []

    for filename in os.listdir(CRAWL_FOLDER):

        with open(f'{CRAWL_FOLDER}/{filename}', 'r') as file:
            news = file.readlines()
            vnexpress += cleandt.convert_dict(news, 'content')
            
    news = pd.DataFrame(columns=['content','url','topic', 'sub-topic', 'image', 'title','description'])

    for new in vnexpress:
        news.loc[len(news)] = pd.Series(new)
    news = news.reset_index().rename(columns={'index':'article_id'})

    ## Select necessary columns
    processed_news = news[['article_id','content','topic','sub-topic','title','description']]

    ## Find null values and processing
    processed_news.fillna('', inplace=True)
    ## Merge columns into a single `tag` column
    processed_news['tag'] = processed_news['content'] + processed_news['title'] + processed_news['description']
    processed_news = processed_news.drop(columns=['content','description','title'])

    ## Tokenize the Vietnamese words
    processed_news['tag'] = processed_news['tag'].apply(lambda x: x.lower())
    processed_news['tag'] = processed_news['tag'].apply(lambda x: remove_punctuation(x))
    processed_news['tag'] = processed_news['tag'].apply(lambda x: ViTokenizer.tokenize(x))
    
    """Dump each tag to a text file
    """
    processed_news.to_csv(f'{ROOT_PATH}/data/scraped_data/csv/cleaned_vnexpress.csv')
    
    PROCESSED_FOLDER = f'{ROOT_PATH}/data/scraped_data/processed'
    for topic in tqdm(os.listdir(PROCESSED_FOLDER)):
        articles_ids, tags = get_info(topic, processed_news)
        # print(articles_ids)
        for id, tag in zip(articles_ids, tags):
            with open(f'{PROCESSED_FOLDER}/{topic}/{id}.txt', "w", encoding="utf-8") as file:
                file.write(tag)