import requests
from bs4 import BeautifulSoup

def get_content_url(url:str) -> str:
    """Example of Header:
    
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Accept-Encoding: gzip, deflate, sdch
        Accept-Language: en-US,en;q=0.8,vi;q=0.6
        Connection: keep-alive
        Cookie: __ltmc=225808911; __ltmb=225808911.202893004; __ltma=225808911.202893004.204252493; _gat=1; __RC=4; __R=1; _ga=GA1.3.938565844.1476219934; __IP=20217561; __UF=-1; __uif=__ui%3A-1%7C__uid%3A877575904920217840%7C__create%3A1475759049; __tb=0; _a3rd1467367343=0-9
        Host: dantri.com.vn
        Referer: http://dantri.com.vn/su-kien.htm
        Upgrade-Insecure-Requests: '1'
        User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
    """
    
    domain = None
    domains = url.split('/')
    if domains.__len__() >= 3:
        domain = domains[2]
    
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,vi;q=0.6',
        'Connection': 'keep-alive',
        'Host': domain,
        'Referer': url,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    rep = requests.get(url, headers=header)
    rep.encoding = 'utf-8'
    rep.close()
    return str(rep.text)

def get_content_from_article(url:str, image:str, subtopic:str, topic:str):
    """
    Example Args:
        url: 'https://vnexpress.net/brazil-nguy-co-thanh-lo-ap-bien-chung-ncov-4242061.html'

    Returns:
        a dictionary includes:
            - title
            - topic
            - description
            - contents
            - url
            - image*
            - sub-topic*
            - comments*
    """
    article = {}
    article['content'] = []
    raw_content = get_content_url(url)
    soup = BeautifulSoup(raw_content, 'html.parser')
    
    try: 
        article['url'] = url
        article['topic'] = topic
        article['sub-topic'] = subtopic
        article['image'] = image
        article['title'] = soup.find('h1').text
        article['description'] = soup.find('p', class_='description').text
        for content in soup.find('article', class_='fck_detail').find_all('p', class_='Normal'):
            article['content'].append(content.text)

        # comments = soup.find_all('div', class_='ykien_vne') #.find('div', class_='ykien_vne').find('h3')
        # article['comments'] = comments
    except Exception as ex:
        pass
    
    return article

def get_articles_links_from_subtopic(url:str, subtopic:str) -> list:
    """_summary_

    Args:
        url (str): the url of a sub-topic

    Returns:
        links (list): the list of all article links of that sub-topic
    """    
    links = []
    content = get_content_url(url)
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        try:
            url = article.find('h2', class_='title-news').find('a', href=True)
            image = article.find('picture').find('img', src=True)
            links.append({url['href']: [image['src'], subtopic]})
        except Exception as ex:
            # print(str(ex))
            pass
    
    return links

def get_page_links_from_subtopic(subtopic_link:str, pages=1):
    """_summary_: find all the page from each sub-topic

    Args:
        subtopic_link (str): name of the sub-topic
        pages (int, optional): the number of page wanting to crawl

    Returns:
        _type_: list (the list of link)
    """    
    urls = []
    urls.append(subtopic_link)
    for page in range(2, pages+1, 1):
        urls.append(subtopic_link + f'-p{page}')
        
    return urls

def get_links_from_subtopics(topics_links:dict, pages=1):
    """_summary_

    Args:
        topics_links (dict): {
            'Thoi su': ['https://vnexpress.net/thoi-su/chinh-tri', 'https://vnexpress.net/thoi-su/lao-dong-viec-lam', ...]
            'The thao': ['https://vnexpress.net/the-thao/bundesliga', 'https://vnexpress.net/the-thao/tennis', ...]
            ...
        }
        
    Return:
        topic_links (dict): {
            'thoi su': ['https://vnexpress.net/ong-nguyen-trong-nghia-tao-dieu-kien-de-nha-khoa-hoc-toan-tam-cong-hien-4721119.html', ...]
            ....
        }
    """
    topic_links = {}
    for topic, links in topics_links.items():
        # print(f'Topic {topic} - Number of Sub-topic: {len(links)}')
        urls = []
        for link in links:
            subtopic = link.split('/')[4]
            pages = get_page_links_from_subtopic(link, 2)
            for page in pages:
                url = get_articles_links_from_subtopic(page, subtopic)
                urls += url
        topic_links[f'{topic}'] = urls
        print(f'Scrape {topic}: Done...')
        
    return topic_links


'''IF MAIN RUNNING'''
if __name__ == '__main__':
    from utils import read_yaml
    # links = get_articles_links_from_subtopic('https://vnexpress.net/giao-duc/tin-tuc', 'ABC')
    # article = get_content_from_article('https://vnexpress.net/hien-trang-khu-cong-nghiep-lau-doi-nhat-viet-nam-truoc-di-doi-4720432.html', 'chinh-tri')
    # print(links)
    
    topics_links = read_yaml('./src/links.yaml')
    topics_links = get_links_from_subtopics(topics_links)
    for topic, links in topics_links.items():
        print(topic)
        print(len(links))
        print(links)
        print('--------------------------')
