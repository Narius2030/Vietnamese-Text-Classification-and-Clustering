import ast
import re
import string

def stopwords_vi(stopword_path) -> list:
    # './src/vietnamese-stopwords.txt'
    with open(stopword_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        words = [line.split('\n')[0] for line in lines]

    return words

def remove_stopword(text:str, stopword_path=None) -> str:
    if stopword_path is not None:
        stop_words = stopwords_vi(stopword_path)
        filtered = [word for word in text.split(' ') if word not in stop_words]
        result = ' '.join(filtered)
    else:
        return text
    
    return result

def convert_dict(news:list, content) -> list:
    lst = []
    for new in news:
        new_dict = ast.literal_eval(new)
        new_dict[content] = ' '.join(new_dict[content])
        lst.append(new_dict)

    return lst

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