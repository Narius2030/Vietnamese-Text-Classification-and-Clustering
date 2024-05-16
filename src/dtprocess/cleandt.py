import ast

def stopwords_vi(stopword_path) -> list:
    # './src/vietnamese-stopwords.txt'
    with open(stopword_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        words = [line.split('\n')[0] for line in lines]

    return words

def remove_stopword(text:str, stopword_path:str) -> str:
  stop_words = stopwords_vi(stopword_path)
  filtered = [word for word in text.split(' ') if word not in stop_words]

  return ' '.join(filtered)

def convert_dict(news:list, content) -> list:
    lst = []
    for new in news:
        new_dict = ast.literal_eval(new)
        new_dict[content] = ' '.join(new_dict[content])
        lst.append(new_dict)

    return lst