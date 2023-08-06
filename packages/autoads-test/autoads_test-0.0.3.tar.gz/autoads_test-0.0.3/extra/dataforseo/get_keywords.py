from curses import keyname
import pandas as pd
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("jugnacospi@yevme.com", "21432bd735f5712b")
post_data = dict()

keyword = "coffee"
filename = 'coffee.csv'

post_data[len(post_data)] = dict(
    keyword=keyword,
    location_name="United States",
    language_name="English",
    depth=4,
)

def get_suggested_keywords(response):
    items = response['tasks'][0]['result'][0]['items']
    keywords = list()
    for item in items:
        if item['keyword'] is not None:
            keywords.append(item['keyword'])
    return keywords

def get_related_keywords(response):
    items = response['tasks'][0]['result'][0]['items']
    keywords = list()
    for item in items:
        if item['related_keywords'] is not None:
            keywords.extend(item['related_keywords'])
    return keywords

types_of_request = ['related_keywords','keyword_suggestions']

all_keywords = list()
for request_type in types_of_request:
    response = client.post(f"/v3/dataforseo_labs/{request_type}/live", post_data)
    # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
    if response["status_code"] == 20000:
        if request_type == 'related_keywords':
            print(response)
            all_keywords.append(get_related_keywords(response))
        elif request_type == 'keyowrd_suggestions':
            all_keywords.append(get_suggested_keywords(response))
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))


df = pd.DataFrame({"keyword":all_keywords})
df = df.drop_duplicates("keywords")
df.to_csv(filename,index=False)
