from base64 import urlsafe_b64decode
from nltk.corpus import stopwords
import nltk
import pandas as pd
from client import RestClient
import re
import argparse
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup


def main(email, 
        api_key, 
        seed_keywords, 
        df_file, depth, 
        scrape, 
        urls, 
        exclude, 
        df_ngram):
    
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
                        print(html)
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

        
    keyword_list = seed_keywords
    full_df = pd.DataFrame(columns=['Keywords', 'Keywords2', 'Sources'])
    for keyword in keyword_list:
        print(f'keyword : {keyword}')
        keywords = get_keywords(keyword, depth=depth)
        extracted = extract_keywords(keywords)
        keywords2 = [keyword for _ in range(extracted.shape[0])]
        extracted['Keywords2'] = keywords2
        full_df = pd.concat([full_df, extracted])

    full_df.to_csv(df_file, index=False)
    
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
        print(ext)
        ext = add_spaces(ext, clean_n=True)
        with open('text.txt', 'w', encoding="utf-8") as f:
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
        
        print(fin_ngrams)
        for ngram in ngrams:
            fin_ngrams.append(' '.join([ng for ng in ngram]))
        
    df = pd.DataFrame(columns=['Keywords'], data=fin_ngrams)
    df.to_csv(df_ngram, index=False)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Something"
        ),
    )
    parser.add_argument(
        "--email",
        required=True,
        type=str,
        help=(
            "email for dataforseo"
        ),
    )
    parser.add_argument(
        "--api_key",
        default=None,
        required=True,
        type=str,
        help="api_key for dataforseo",
    )
    parser.add_argument(
        "--seed_keywords",
        default=None,
        required=True,
        type=str,
        action='append',
        help="usage --seed_keywords a1 --seed_keywords a2 --seed_keywords a3 ...",
    )
    parser.add_argument(
        "--depth",
        default=1,
        type=int,
        help="choose between 1 and 4",
    )
    parser.add_argument(
        "--df_file",
        default='df.csv',
        type=str,
        help="save final csv as",
    )
    
    parser.add_argument(
        "--scrape",
        default=False,
        type=bool,
        help="scrape the urls?",
    )
    parser.add_argument(
        "--urls",
        required=True,
        type=str,
        action='append',
        help="usage --urls a1 --urls a2 --urls a3 ...",
    )
    parser.add_argument(
        "--exclude",
        default=['twitter', 'google', 'facebook', 'linkedin', 'youtube'],
        type=str,
        action='append',
        help="usage --exclude a1 --exclude a2 --exclude a3 ...",
    )
    parser.add_argument(
        "--df_url",
        default='df_ngrams.csv',
        type=str,
        help="save final csv as",
    )
    
    args = parser.parse_args()
    main(
        email = args.email,
        api_key = args.api_key,
        seed_keywords = args.seed_keywords,
        depth = args.depth,
        df_file = args.df_file,
        scrape=args.scrape,
        urls = args.urls,
        exclude=args.exclude,
        df_ngram=args.df_url)
    
    # Simple_Pipeline_1.py --email dsvgftohagalkefbon@nthrw.com --api_key 958edef660ede9ec --seed_keywords newton --depth 1 --scrape True --urls capchase.com
