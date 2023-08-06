import os
import torch
import random
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics.pairwise import cosine_similarity
from transformers import (AutoTokenizer,AutoModelForSequenceClassification)

def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONASSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

def get_similarity_api(model,keywords1,keywords2):
    keywords1_embed = model.encode(keywords1)
    keywords2_embed = model.encode(keywords2)
    
    results = list()
    for embed1,embed2 in zip(keywords1_embed,keywords2_embed):
        result = cosine_similarity([embed1],[embed2])
        results.append(result)
    return np.array(results).ravel()

def get_similarity_scrape(model,all_keywords,main_keyword):
    
    all_embeddings = model.encode(all_keywords)
    main_embedding = model.encode([main_keyword])

    results = cosine_similarity(
        all_embeddings,
        main_embedding,)
    return np.array(results)


group_map = {
    "LF":0,
    "MF":1,
    "UF":2,
    "competitor":3,
    "brand":4}

map_group = {
    0:"LF",
    1:"MF",
    2:"UF",
    3:"competitor",
    4:"brand"}

config = {
    'batch_size':8,
    'num_workers':4,
    'max_len':10,
    'nfolds':5,
    'seed':1000,
    'model_path':'roberta-large'
}

class GadsTestDataset(Dataset):
    def __init__(self,df,tokenizer):
        self.keywords = df['Keywords'].to_numpy()
        self.tokenizer = tokenizer
    
    def __getitem__(self,idx):
        encode = self.tokenizer(self.keywords[idx],return_tensors='pt',
                                max_length=config['max_len'],
                                padding='max_length',truncation=True)
        return encode
    
    def __len__(self):
        return len(self.keywords)


def get_prediction(df,config,path,model_path,device='cuda'):        
    model = AutoModelForSequenceClassification.from_pretrained('model_path',num_labels = 3)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    predictions = list()
    
    for f in range(config['nfolds']):
        model.load_state_dict(torch.load(path.format(f),map_location=device))
        model.to(device)
        model.eval()

        test_ds = GadsTestDataset(df,tokenizer)
        test_dl = DataLoader(test_ds,
                            batch_size = config["batch_size"],
                            shuffle=False,
                            drop_last=False,
                            num_workers = 4,
                            pin_memory=True)

        with torch.no_grad():
            pred = list()
            for i, (inputs) in enumerate(test_dl):
                inputs = {key:val.reshape(val.shape[0],-1).to(device) for key,val in inputs.items()}
                outputs = model(**inputs)
                outputs = outputs['logits'].cpu().detach().numpy().tolist()
                pred.extend(outputs)
            predictions.append(pred)
            
    torch.cuda.empty_cache()
    predictions = torch.softmax(predictions,axis=1)
    return np.mean(predictions,axis=0)

