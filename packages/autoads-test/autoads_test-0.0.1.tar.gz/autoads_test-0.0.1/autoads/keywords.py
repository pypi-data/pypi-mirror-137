import os
import re
import nltk
import argparse
import numpy as np
import pandas as pd
from autoads.client import RestClient
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from urllib.request import urlopen
from base64 import urlsafe_b64decode
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def get_keywords_from_api_and_url(email, 
        api_key, 
        seed_keywords, 
        df_api_path, 
        depth, 
        scrape, 
        urls, 
        exclude, 
        df_scrape_path):
    
    client = RestClient(email, api_key)

    def get_keywords(keyword, depth=depth, location='United States'):
        post_data = dict()
        post_data[len(post_data)] = dict(
            keyword=keyword,
            location_name=location,
            language_name="English",
            depth=depth,
        )
        post_data2 = dict()
        post_data2[len(post_data2)] = dict(
            keywords=[keyword],
            location_name=location,
            language_name="English",
            depth=depth,
        )
        response = client.post(
            "/v3/dataforseo_labs/related_keywords/live", post_data)
        response2 = client.post(
            "/v3/dataforseo_labs/keyword_ideas/live", post_data2)
        response3 = client.post(
            "/v3/dataforseo_labs/keyword_suggestions/live", post_data)

        return {  
            'related': response,
            'ideas': response2,
            'suggestions': response3
        }
        
    def extract_keywords(responses):
        key_list = []
        sources = []

        print(responses)
        
        if responses['related']["status_code"] == 20000 and responses['related']['tasks'][0]['result'][0]['items']:
            for x in range(len(responses['related']['tasks'][0]['result'][0]['items'])):
                res = responses['related']['tasks'][0]['result'][0]['items'][x]['related_keywords']
                if res is not None:
                    key_list.extend(res)
            print(f"{len(key_list)} related")
            sources.extend(['related' for _ in range(len(key_list))])
            
        if responses['ideas']["status_code"] == 20000 and responses['ideas']['tasks'][0]['result'][0]['items']:
            # not good ideas
            print(f"{len(responses['ideas']['tasks'][0]['result'][0]['items'])} ideas")
            for x in range(len(responses['ideas']['tasks'][0]['result'][0]['items'])):
                res = responses['ideas']['tasks'][0]['result'][0]['items'][x]['keyword']
                if res is not None:
                    key_list.append(res)
            sources.extend(['ideas' for _ in range(
                len(responses['ideas']['tasks'][0]['result'][0]['items']))])
                    
        if responses['suggestions']["status_code"] == 20000 and responses['suggestions']['tasks'][0]['result'][0]['items']:
            print(f"{len(responses['suggestions']['tasks'][0]['result'][0]['items'])} suggestions")
            for x in range(len(responses['suggestions']['tasks'][0]['result'][0]['items'])):
                res = responses['suggestions']['tasks'][0]['result'][0]['items'][x]['keyword']
                if res is not None:
                    key_list.append(res)
            sources.extend(['suggestions' for _ in range(
                len(responses['suggestions']['tasks'][0]['result'][0]['items']))])
        # else:
        #     print("error. Code: %d Message: %s" %
        #           (responses['all]["status_code"], responses['all']["status_message"]))
        temp = {
            'Keywords' : key_list,
            'Sources' : sources
        }
        df = pd.DataFrame.from_dict(temp)
        return df
    
    def add_spaces(text, thresh = 3, clean_n = False):
        cleaned = ''
        temp = [l.isupper() for l in text]
        chk = 0
        for i, s in enumerate(temp):
            if s and i != 0 and (i - chk) > thresh:
                cleaned += ' ' + ext[chk : i]
                chk = i
        for i, w in enumerate(cleaned):
            if w != ' ':
                cleaned = cleaned[i:]
                break
            else:
                i+=1
        if clean_n:
            cleaned = cleaned.replace('\n', ' ')
        return cleaned.replace('  ', ' ')
    
    def clean(text):
        text = text.replace('*', '')
        text = text.replace('\ufeff', '')
        text = text.replace('\n', '')
        text = text.replace('.', '')
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('"', '')
        text = text.replace('/', ' ')
        text = text.replace('%', ' ')
        text = text.replace('-', '')
        text = text.replace('”', '')
        text = text.replace('“', '')
        text = text.replace('\'', '')
        text = text.replace('!', '')
        text = text.replace('?', '')
        text = text.replace('&', '')
        text = text.replace('+', '')
        text = text.replace('$', '')
        text = text.replace(',', '')
        return text
    
    def _extract_(urls, depth = 1, return_urls = True, return_redirects = True, exclude = exclude):
        print(urls)
        exclude = exclude
        scrape_urls = urls
        resp = []
        resp_urls = []
        full_text = ''
        depth = depth
        for _ in range(depth):
            temp_urls = []
            for url in scrape_urls:
                try:
                    chk = 0
                    for exc in exclude:
                        if exc in url:
                            print(url)
                            chk = 1
                    
                    if chk == 0:
                        html = urlopen(url).read()
                        # print(html)
                        soup = BeautifulSoup(html, features="html.parser")
                        
                        for link in soup.find_all('a', attrs = {'href':re.compile('^/')}):
                            uri = link.get('href')
                            temp_urls.append(url + uri)
                            # print(uri)
                        
                        for link in soup.find_all('a', attrs={'href': re.compile('^https://')}):
                            uri = link.get('href')
                            temp_urls.append(uri)
                        
                        for script in soup(['script', 'style']):
                            script.extract()
                        
                        text = soup.get_text()
                        
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = '\n'.join(chunk for chunk in chunks if chunk)
                        full_text += ' ' + text
                        resp_urls.append(url)
                        resp.append(1)
                except:
                    resp_urls.append(url)
                    resp.append(0)
                    continue
        
            scrape_urls = list(set(temp_urls))
            
        if return_urls:
            if return_redirects:
                return full_text, resp_urls, (resp_urls, resp)
            else:
                return full_text, resp_urls
        elif return_redirects:
            return full_text, (resp_urls, resp)
        else:
            return full_text
    
    os.makedirs('data',exist_ok=True)
    keyword_list = seed_keywords
    df_api = pd.DataFrame(columns=['Keywords', 'Keywords2', 'Sources'])
    # for keyword in keyword_list:
    #     print(f'keyword : {keyword}')
    #     keywords = get_keywords(keyword, depth=depth)
    #     extracted = extract_keywords(keywords)
    #     keywords2 = [keyword for _ in range(extracted.shape[0])]
    #     extracted['Keywords2'] = keywords2
    #     df_api = pd.concat([df_api, extracted])
    
    fin_ngrams = []
    if scrape:
        new_urls = []
        for url in urls:
            if not 'http' in url:
                if not 'www' in url:
                    new_urls.append(f'https://www.{url}')
                else:
                    new_urls.append(f'https://{url}')
        urls = new_urls
        fin_ngrams = []
        ext, _, _ = _extract_(urls, depth=depth)
        # print(ext)
        ext = add_spaces(ext, clean_n=True)
        text_path = os.path.join(os.getcwd(),'data/text.txt')
        with open(text_path, 'w', encoding="utf-8") as f:
            f.write(ext)
            
        nltk.download('stopwords')
        stop = set(stopwords.words('english'))
        text = clean(ext)
        splt_text = text.split(' ')
        nw_list = []
        for t in splt_text:
            if t not in stop and not t == '' and not t.isdigit() and len(t) > 1:
                nw_list.append(t)
                
        ngrams = []
        ngrams.extend(nltk.ngrams(nw_list, 3))
        ngrams.extend(nltk.ngrams(nw_list, 4))
        
        # print(fin_ngrams)
        for ngram in ngrams:
            fin_ngrams.append(' '.join([ng for ng in ngram]))
        
    #saving api data
    df_api_path = os.path.join(os.getcwd(),"data/"+df_api_path)
    df_api.to_csv(df_api_path, index=False)

    #saving scraped keywords
    df_scrape = pd.DataFrame(columns=['Keywords'], data=fin_ngrams)
    df_scrape_path = os.path.join(os.getcwd(),"data/"+df_scrape_path)
    df_scrape.to_csv(df_scrape_path, index=False)

    return df_api,df_scrape
        
# if __name__ == "__main__":

#     df_api,df_scrape = get_keywords_from_api_and_url()
  
#     email = input("Email for dataforseo: ")
#     api_key = input("Api key for dataforseo: ")
#     seed_keywords = input("Enter Seed Keywords (comma after every keyword): ").split(',')
#     scrap = input("Do you want to scrap the data (y/n) ?: ").strip()

#     scrape = False
#     urls = []
#     exclude = ['twitter', 'google', 'facebook', 'linkedin', 'youtube']
#     df_api_path = 'df_api.csv'
#     df_scrape_path = 'df_scrape.csv'

#     if scrap == 'y' or scrap == 'Y':
#         depth = int(input("Depth for scraping (any no btwn 1 to 4): "))
#         urls = input("Urls to scrape (comma after every url): ").split(',')
#         exclude = input("sites to ignore (comma after every name): ").split(',')

#     df_api,df_scrape = get_keywords(
#         email = email,
#         api_key = api_key,
#         seed_keywords = seed_keywords,
#         depth = depth,
#         df_api_path= df_api_path,
#         df_scrape_path=df_scrape_path,
#         scrape=scrap,
#         urls = urls,
#         exclude=exclude)