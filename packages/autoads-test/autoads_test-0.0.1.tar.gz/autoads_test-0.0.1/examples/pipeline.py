from sentence_transformers import SentenceTransformer
from autoads.keywords import get_keywords_from_api_and_url
from autoads.models import get_similarity_api,get_similarity_scrape

email = input("Email for dataforseo: ")
api_key = input("Api key for dataforseo: ")
seed_keywords = input("Enter Seed Keywords (comma after every keyword): ").split(',')
scrape = input("Do you want to scrape the data (y/n) ?: ").strip()

urls = []
exclude = ['twitter', 'google', 'facebook', 'linkedin', 'youtube']
df_api_path = 'df_api.csv'
df_scrape_path = 'df_scrape.csv'

if scrape == 'y' or scrape == 'Y':
    scrape = True
    depth = int(input("Depth for scraping (any no btwn 1 to 4): "))
    urls = input("Urls to scrape (comma after every url): ").split(',')
    exclude = input("sites to ignore (comma after every name): ").split(',')
elif scrape == 'n' or scrape == 'N':
    scrape = False

df_api,df_scrape = get_keywords_from_api_and_url(
        email= email, 
        api_key=api_key, 
        seed_keywords=seed_keywords, 
        df_api_path=df_api_path, 
        depth=depth, 
        scrape=scrape, 
        urls=urls, 
        exclude=exclude, 
        df_scrape_path=df_scrape_path
)

print(df_api.head(),df_scrape.head())

model_path = 'sentence-transformers/paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_path)

# keywords1 = df_api['Keywords'].tolist()
# keywords2 = df_api['Keywords2'].tolist()
# df_api['similarity'] = get_similarity_api(model,keywords1,keywords2)

scrape_keywords = df_scrape['Keywords'].tolist()
for keyword in seed_keywords:
    df_scrape[keyword] = get_similarity_scrape(model,scrape_keywords,keyword)

print(df_api.head(),df_scrape.head())
