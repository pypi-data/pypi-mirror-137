import requests
from io import StringIO
import pandas as pd
import sys
import os
from tqdm import tqdm
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from scipy import stats
import seaborn
import warnings
from pathlib import Path
import re


warnings.filterwarnings('ignore')
    
    
def zinc_drug(genes_list:list, zinc_type:str = 'all', species:str = 'all'):

    genes_list = [gen.upper() for gen in genes_list ]
    
    if not os.path.exists('results'):
        os.mkdir('results')
    
    genes_list = list(np.unique(genes_list))
    df_zinc = pd.DataFrame(columns = ['ortholog_name', 'zinc_id', 'gene_name', 'affinity','chembldocid', 'type'])
    
    zinc_type = zinc_type.lower()
    
    for gen in tqdm(genes_list):
        
        if zinc_type == 'all'or zinc_type == 'observations':
            requestURL = "https://zinc.docking.org/genes/"+gen+"/observations.csv?count=all"
            r = requests.get(requestURL)
            responseBody = r.text 
            if responseBody[0:7] == 'zinc_id':
                df = pd.read_csv(StringIO(responseBody), sep=',')
                df['type'] = 'observations'
                if True not in np.unique(df.columns == 'gene_name'):
                    df['gene_name'] = gen
                df_zinc = pd.concat([df_zinc, df], axis=0)
        
        if zinc_type == 'all'or zinc_type == 'substances':
            requestURL = "https://zinc.docking.org/genes/"+gen+"/substances.csv?count=all"
            r = requests.get(requestURL)
            responseBody = r.text 
            if responseBody[0:7] == 'zinc_id':
                df = pd.read_csv(StringIO(responseBody), sep=',')
                df['type'] = 'substances'
                if True not in np.unique(df.columns == 'gene_name'):
                    df['gene_name'] = gen
                df_zinc = pd.concat([df_zinc, df], axis=0)
            
        
        if zinc_type == 'all'or zinc_type == 'purchasable':
            requestURL = "https://zinc.docking.org/genes/"+gen+"/substances/subsets/for-sale.csv?count=all"
            r = requests.get(requestURL)
            responseBody = r.text 
            if responseBody[0:7] == 'zinc_id':
                df = pd.read_csv(StringIO(responseBody), sep=',')
                df['type'] = 'purchasable'
                if True not in np.unique(df.columns == 'gene_name'):
                    df['gene_name'] = gen
                df_zinc = pd.concat([df_zinc, df], axis=0)
    
    df_zinc['species'] = [re.sub('.*_', '', i) for i in df_zinc['ortholog_name']]
    
    if species == 'hs':
        df_zinc = df_zinc[df_zinc['species'] == 'HUMAN']
    elif species == 'ms':
        df_zinc = df_zinc[df_zinc['species'] == 'MOUSE']   
        
    return df_zinc 


def zinc_plot(res_zinc:pd.DataFrame, p_val, adj:str = 'None', dir:str = 'results', name:str = 'drugs'):

    adj = adj.upper()
    
    if not os.path.exists('results'):
        os.mkdir('results')

    df3 = res_zinc[['zinc_id', 'gene_name']]
    df3 = df3.drop_duplicates()
    list_path = df3['zinc_id'][pd.isna(df3['zinc_id']) == False]
    lp = list(df3['zinc_id'])



    values, counts = np.unique(lp, return_counts=True)    
    count = pd.DataFrame({'zinc_id':values, 'n':counts})
    count = count[count['zinc_id'] != 'None']
    count = count.sort_values('n', ascending=False)



    count['%'] = count['n']/sum(count['n'])*100
    count['p-val'] = None

    for n, p in enumerate(count['n']):   
        count['p-val'][n] = stats.binom_test(count['n'][n],len(df3['zinc_id']),1/len(df3['zinc_id']))

    count['p-adj[BF]'] = count['p-val'] * len(count['p-val'])
    count['p-adj[BF]'][count['p-adj[BF]'] >= 1] = 1
        
    
    if adj == 'BF':
        count = count[count['p-adj[BF]'] < p_val]
    else:
        count = count[count['p-val'] < p_val]

    if len(count[count['p-adj[BF]'] < p_val]) > 0:
        plt.figure(figsize=(10, len(count['zinc_id'])/3))
        seaborn.barplot(count['n'], count['zinc_id'])
        plt.xlabel('Drugs [n]')
        plt.ylabel(' ')
        plt.title('Zinc_drugs')
        plt.savefig(Path(dir, str(name + '.png')),  bbox_inches='tight',  dpi = 300)
        plt.savefig(Path(dir, str(name + '.svg')))
        plt.clf()
        plt.close()
    else:
        print('','No significient drugs found', sep='\n')
        
    return count