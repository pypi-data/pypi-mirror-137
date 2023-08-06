import requests
import json
import sys
from bioservices import KEGG
import pandas as pd
import numpy as np
from datetime import datetime
import collections
from tqdm import tqdm
import os
import seaborn
import matplotlib.pyplot as plt
from scipy import stats
import networkx as nx
from pyvis.network import Network
import warnings
from pathlib import Path


warnings.filterwarnings('ignore')

ms hs

def gopa_enrichment(genes_list:list, str:species): 
    if species == 'hs':
        tax_id = '9606'
        tax = 'hsa:'
    elif species == 'ms':
        tax_id = '10090 '
        tax = 'mmu:'
        
    genes_list = [gen.upper() for gen in genes_list ]
    
    name_dict = {
         "GO:0008150":"biological_process",
         "GO:0003674":"molecular_function",
         "GO:0005575":"cellular_component",
         "ANNOT_TYPE_ID_PANTHER_GO_SLIM_MF":"molecular_function",
         "ANNOT_TYPE_ID_PANTHER_GO_SLIM_BP":"biological_process",
         "ANNOT_TYPE_ID_PANTHER_GO_SLIM_CC":"cellular_component",
         "ANNOT_TYPE_ID_PANTHER_PC":"protein_class",
         "ANNOT_TYPE_ID_PANTHER_PATHWAY":"pathway",
         "ANNOT_TYPE_ID_REACTOME_PATHWAY":"pathway"}
    
    df = {'gen':[],'type':[],'GOPa':[]}
    for gen in tqdm(genes_list):
    
        #KEGG path download
        k = KEGG(verbose=False)
        tmp = k.get(str(tax) + str(gen))
        if tmp != 404:
            dict_data = k.parse(tmp)
            if 'PATHWAY' in dict_data.keys():
                path = dict_data['PATHWAY']
                path_list = []
                keys = path.keys()
                for key in keys:
                    path_list.append(path.get(key))
                df['gen'].append(gen)   
                df['GOPa'].append(path_list)
                df['type'].append('pathway')
        #GOPanther 
        requestURL = "http://pantherdb.org/services/oai/pantherdb/geneinfo?geneInputList="+gen+"&organism="+tax_id
        r = requests.get(requestURL, headers={ "Accept" : "application/json"})
        if not r.ok:
          r.raise_for_status()
          sys.exit() 
        responseBody = r.text 
        json_data = json.loads(responseBody)
        if 'unmapped_list' in json_data['search']:
            df['gen'].append(gen)
            df['type'].append(None)
            df['GOPa'].append(None)
        elif type(json_data['search']['mapped_genes']['gene']) != list and 'annotation_type_list' not in json_data['search']['mapped_genes']['gene'].keys():
            df['gen'].append(gen)
            df['type'].append(None)
            df['GOPa'].append(None)
        else:
            if type(json_data['search']['mapped_genes']['gene']) == dict:               
                dict_list = json_data['search']['mapped_genes']['gene']['annotation_type_list']['annotation_data_type']
                if [p in ['annotation_list'] for p in dict_list][0] == True:
                    fun = name_dict.get(dict_list['content'])
                    path = dict_list['annotation_list']['annotation']
                    if type(path) == 'list' or [p in ['name', 'id'] for p in path][0] == True:
                        path_list = [path['name']]
                        df['gen'].append(gen)
                        df['type'].append(fun)
                        df['GOPa'].append(path_list)
                    else:
                        path_list = []
                        for p in path:
                            path_list.append(p['name'])
                        df['gen'].append(gen)
                        df['type'].append(fun)
                        df['GOPa'].append(path_list)
                else:
                    db_n = len(dict_list)
                    for num in range(0,db_n):
                        fun = name_dict.get(dict_list[num]['content'])
                        path = dict_list[num]['annotation_list']['annotation']
                        if str(type(path)) == 'list' or [p in ['name', 'id'] for p in path][0] == True:
                            path_list = [path['name']]
                            df['gen'].append(gen)
                            df['type'].append(fun)
                            df['GOPa'].append(path_list)
                        else:
                            path_list = []
                            for p in path:
                                path_list.append(p['name'])
                            df['gen'].append(gen)
                            df['type'].append(fun)
                            df['GOPa'].append(path_list)
            else:
                for g in range(0, len(json_data['search']['mapped_genes']['gene'])):
                   dict_list = json_data['search']['mapped_genes']['gene'][g]['annotation_type_list']['annotation_data_type']
                   if type(dict_list) == dict and [p in 'name' for p in dict_list['annotation_list']['annotation']][0]:
                        fun = name_dict.get(dict_list['content'])
                        path = dict_list['annotation_list']['annotation']
                        if type(path) == 'list' or [p in ['name', 'id'] for p in path][0] == True:
                            path_list = [path['name']]
                            df['gen'].append(gen)
                            df['type'].append(fun)
                            df['GOPa'].append(path_list)
                        else:
                            path_list = []
                            for p in path:
                                path_list.append(p['name'])
                            df['gen'].append(gen)
                            df['type'].append(fun)
                            df['GOPa'].append(path_list) 
                   else:        
                       db_n = len(dict_list)
                       for num in range(0,db_n):
                           fun = name_dict.get(dict_list[num]['content'])
                           path = dict_list[num]['annotation_list']['annotation']
                           if type(path) == 'list' or [p in ['name', 'id'] for p in path][0] == True:
                               path_list = [path['name']]
                               df['gen'].append(gen)
                               df['type'].append(fun)
                               df['GOPa'].append(path_list)
                           else:
                               path_list = []
                               for p in path:
                                   path_list.append(p['name'])
                               df['gen'].append(gen)
                               df['type'].append(fun)
                               df['GOPa'].append(path_list) 
        
        
    df2 = pd.DataFrame.from_dict(df)
    df2 = df2[pd.isna(df2['GOPa']) == False]
    df2 = df2.reset_index(drop=True)
    
    df3 = {'gen':[],'type':[],'GOPa':[]}

    for i in range(0,len(df2['gen'])):
        for n in df2['GOPa'][i]:
            df3['gen'].append(df2['gen'][i])
            df3['type'].append(df2['type'][i])
            df3['GOPa'].append(n)
        
    df3 = pd.DataFrame.from_dict(df3)
    df3 = df3.drop_duplicates()
    
  
    
    return df3


def gopa_stat(gopa_df, p_val:float = 0.05, adj:str = 'None', dir:str = 'results', name:str = 'GOPa'):
    
    adj = adj.upper()
    
    if not os.path.exists(dir):
        os.mkdir(dir)
        
    df3 = gopa_df
    df4 = pd.DataFrame()     
    for typ in tqdm(set(df3['type'])):
        tmp = df3[df3['type'] == str(typ)]
        list_path = tmp['GOPa'][pd.isna(tmp['GOPa']) == False]
        lp = list(tmp['GOPa'])
    
        
        
        values, counts = np.unique(lp, return_counts=True)    
        count = pd.DataFrame({'GOPa':values, 'n':counts})
        count = count[count['GOPa'] != 'None']
        count = count.sort_values('n', ascending=False)
    
    
    
    

        count['%'] = count['n']/sum(count['n'])*100
        count['p-val'] = None
    
        for n, p in enumerate(count['n']):   
            count['p-val'][n] = stats.binom_test(count['n'][n],len(tmp['GOPa']),1/len(tmp['GOPa']))

       
            count['p-adj[BF]'] = count['p-val'] * len(count['p-val'])
            count['p-adj[BF]'][count['p-adj[BF]'] >= 1] = 1
         
        if adj == 'BF':
            count = count[count['p-adj[BF]'] < p_val]
        else:
            count = count[count['p-val'] < p_val]

    

    
        if len(count[count['p-adj[BF]'] < p_val]) > 0:
            plt.figure(figsize=(10, len(count['GOPa'])/3))
            seaborn.barplot(count['%'], count['GOPa'])
            plt.xlabel('Percent of enrichment [%]')
            plt.ylabel(' ')
            plt.title(typ.capitalize())
            plt.savefig(Path(dir, str(name + '_' + typ + '.png')),  bbox_inches='tight',  dpi = 300)
            plt.savefig(Path(dir, str(name + '_' + typ + '.svg')))
            plt.clf()
            plt.close()
        else:
            print('','No significient results for ' + str(typ), sep='\n')
    
        if len(df4) == 0:
            df4 = count
        else:
            df4 = pd.concat([df4, count])

        df4 = df4[['GOPa', 'n', 'p-val', 'p-adj[BF]', '%']]
        df5 = df3.loc[df3['GOPa'].isin(df4['GOPa'])]
        df6 = df5.merge(df4, on =  'GOPa', how = 'left')
        df6 = df6.drop_duplicates()
    
    return df6

#Network genes

def gene_network(gopa_df:pd.DataFrame, p_val:float = 0.05, adj:str = 'None', dir:str = 'results' , name:str = 'gene_relation'):
    
    adj = adj.upper()
    
    if not os.path.exists(dir):
        os.mkdir(dir)
    
    df7 = gopa_df.pivot_table(index = "GOPa", columns = 'gen', values = 'n',  fill_value = 0)
               
    df7[df7 > 0] = 1
    
    net_df = {'Gen1':[],'Gen2':[]}
    duplicated = []
    for n1, col1 in enumerate(tqdm(df7.columns)): 
        for n2, col2 in enumerate(df7.columns): 
            if (col1 != col2 and df7.columns[n1] + df7.columns[n2] not in duplicated):
                tmp = pd.concat([df7.loc[:, col1], df7.loc[:, col2]], axis=1, join="inner")
                tmp['sum'] = tmp.iloc[:,0] + tmp.iloc[:,1]
                duplicated.append(tmp.columns[1] + tmp.columns[0])
                for i in range(0,int(sum(tmp['sum'] == 2))):
                    net_df['Gen1'].append(col1)
                    net_df['Gen2'].append(col2)
    
    net_df = pd.DataFrame.from_dict(net_df)
    net_df['inter'] = net_df['Gen1'] + ' + ' + net_df['Gen2']
    net_df['weight'] = net_df.groupby('inter')['inter'].transform('count')
    net_df = net_df.drop_duplicates()
    net_df = net_df.reset_index(drop=True)
    
    net_df['p-val'] = None
    
    for n, p in enumerate(tqdm(net_df['weight'])):   
        net_df['p-val'][n] = stats.binom_test(net_df['weight'][n],sum(net_df['weight']),1/sum(net_df['weight']))    
     
    net_df['p-adj[BF]'] = net_df['p-val']*len(net_df['p-val'])
    
    if adj == 'BF':
        net_df = net_df[net_df['p-adj[BF]'] < p_val]
    else:
        net_df = net_df[net_df['p-val'] < p_val]
        
    net_df['weight'] = np.log(net_df['weight'])*10
      
    G = nx.Graph() 
    
    nodes = list(net_df['Gen1'])+list(net_df['Gen2'])
    values, counts = np.unique(nodes, return_counts=True)    
    nodes_df = pd.DataFrame({'node':values, 'n':counts})
    nodes_df = nodes_df[nodes_df['node'] != 'None']
    nodes_df = nodes_df.sort_values('n', ascending=False)
    nodes_df['n'] = np.log(nodes_df['n'] + 1) * 10

    for i in range(0,len(nodes_df['node'])):
        G.add_node(nodes_df.iloc[i,0], size = nodes_df.iloc[i,1], color = 'red')
        
    for i in range(0,len(net_df['Gen1'])):
        G.add_edge(net_df.iloc[i,0], net_df.iloc[i,1], weight = net_df.iloc[i,3])
    
    net = Network(notebook=True, height = '1000px', width = '1200px')
    net.from_nx(G)
    net.repulsion(node_distance=120, spring_length=220)
    net.show_buttons(filter_=['nodes', 'physics'])
    net.show(Path(dir, str(name + '.html')))

    
    return net_df


#Network_GOPa

def gopa_network(gopa_df:pd.DataFrame, p_val:float = 0.05, adj:str = 'None', dir:str = 'results', name:str = 'gopa_network'):
  
    adj = adj.upper()
    
    if not os.path.exists('results'):
        os.mkdir('results')
        
    df6 = gopa_df
    pathways = df6[df6['type'] == 'pathway']
    
    
    df7 = pathways.pivot_table(index = "gen", columns = 'GOPa', values = 'n',  fill_value = 0)
    df7[df7 > 0] = 1
    
    net_df = {'Path1':[],'Path2':[]}
    duplicated = []
    for n1, col1 in enumerate(tqdm(df7.columns)): 
        
        for n2, col2 in enumerate(df7.columns): 
            if (col1 != col2 and df7.columns[n1] + df7.columns[n2] not in duplicated):
                tmp = pd.concat([df7.loc[:, col1], df7.loc[:, col2]], axis=1, join="inner")
                tmp['sum'] = tmp.iloc[:,0] + tmp.iloc[:,1]
                duplicated.append(tmp.columns[1] + tmp.columns[0])
                for i in range(0,int(sum(tmp['sum'] == 2))):
                    net_df['Path1'].append(col1)
                    net_df['Path2'].append(col2)
    
                
    if len(net_df['Path1']) != 0:
        
        net_df = pd.DataFrame.from_dict(net_df)
        net_df['inter'] = net_df['Path1'] + ' + ' + net_df['Path2']
        net_df['weight'] = net_df.groupby('inter')['inter'].transform('count')
        net_df = net_df.drop_duplicates()
        net_df = net_df.reset_index(drop=True)
        
        net_df['p-val'] = None
        
        for n, p in enumerate(net_df['weight']):   
            net_df['p-val'][n] = stats.binom_test(net_df['weight'][n],sum(net_df['weight']),1/sum(net_df['weight']))
        
        net_df['p-adj[BF]'] = net_df['p-val']*len(net_df['p-val'])
        
        if adj == 'BF':
            net_df = net_df[net_df['p-adj[BF]'] < p_val]
        else:
            net_df = net_df[net_df['p-val'] < p_val]
            
        net_df['weight'] = np.log(net_df['weight'])*10
        
        return_df = net_df
        
        pathways_nx = nx.Graph() 
        
        nodes = list(net_df['Path1'])+list(net_df['Path2'])
        values, counts = np.unique(nodes, return_counts=True)    
        nodes_df = pd.DataFrame({'node':values, 'n':counts})
        nodes_df = nodes_df[nodes_df['node'] != 'None']
        nodes_df = nodes_df.sort_values('n', ascending=False)
        nodes_df['n'] = np.log(nodes_df['n'] + 1) * 10
        
        for i in range(0,len(nodes_df['node'])):
            pathways_nx.add_node(nodes_df.iloc[i,0], size = nodes_df.iloc[i,1], color = 'red')
            
        for i in range(0,len(net_df['Path1'])):
            pathways_nx.add_edge(net_df.iloc[i,0], net_df.iloc[i,1], weight = net_df.iloc[i,3])
            
    
    
    else:
        pathways_nx = []
        
    protein_class = df6[df6['type'] == 'protein_class']
    
    
    df7 = protein_class.pivot_table(index = "gen", columns = 'GOPa', values = 'n',  fill_value = 0)
    df7[df7 > 0] = 1
    
    net_df = {'Path1':[],'Path2':[]}
    duplicated = []
    for n1, col1 in enumerate(tqdm(df7.columns)): 
        for n2, col2 in enumerate(df7.columns): 
            if (col1 != col2 and df7.columns[n1] + df7.columns[n2] not in duplicated):
                tmp = pd.concat([df7.loc[:, col1], df7.loc[:, col2]], axis=1, join="inner")
                tmp['sum'] = tmp.iloc[:,0] + tmp.iloc[:,1]
                duplicated.append(tmp.columns[1] + tmp.columns[0])
                for i in range(0,int(sum(tmp['sum'] == 2))):
                    net_df['Path1'].append(col1)
                    net_df['Path2'].append(col2)
       
    
    if len(net_df['Path1']) != 0:
        
        net_df = pd.DataFrame.from_dict(net_df)
        net_df['inter'] = net_df['Path1'] + ' + ' + net_df['Path2']
        net_df['weight'] = net_df.groupby('inter')['inter'].transform('count')
        net_df = net_df.drop_duplicates()
        net_df = net_df.reset_index(drop=True)
        
        net_df['p-val'] = None
        
        for n, p in enumerate(net_df['weight']):   
            net_df['p-val'][n] = stats.binom_test(net_df['weight'][n],sum(net_df['weight']),1/sum(net_df['weight']))
        
        net_df['p-adj[BF]'] = net_df['p-val']*len(net_df['p-val'])
        
        if adj == 'BF':
            net_df = net_df[net_df['p-adj[BF]'] < p_val]
        else:
            net_df = net_df[net_df['p-val'] < p_val]
            
        net_df['weight'] = np.log(net_df['weight'])*10
        
        return_df = pd.concat([return_df, net_df])
        
        protein_class_nx = nx.Graph() 
        
        nodes = list(net_df['Path1'])+list(net_df['Path2'])
        values, counts = np.unique(nodes, return_counts=True)    
        nodes_df = pd.DataFrame({'node':values, 'n':counts})
        nodes_df = nodes_df[nodes_df['node'] != 'None']
        nodes_df = nodes_df.sort_values('n', ascending=False)
        nodes_df['n'] = np.log(nodes_df['n'] + 1) * 10
        
        for i in range(0,len(nodes_df['node'])):
            protein_class_nx.add_node(nodes_df.iloc[i,0], size = nodes_df.iloc[i,1], color = 'yellow')
            
        for i in range(0,len(net_df['Path1'])):
            protein_class_nx.add_edge(net_df.iloc[i,0], net_df.iloc[i,1], weight = net_df.iloc[i,3])
            
        
    
    else:
        protein_class_nx = []
    
    biological_process = df6[df6['type'] == 'biological_process']
    
    
    
    df7 = biological_process.pivot_table(index = "gen", columns = 'GOPa', values = 'n',  fill_value = 0)
    df7[df7 > 0] = 1
    
    net_df = {'Path1':[],'Path2':[]}
    duplicated = []
    for n1, col1 in enumerate(tqdm(df7.columns)): 
        for n2, col2 in enumerate(df7.columns): 
            if (col1 != col2 and df7.columns[n1] + df7.columns[n2] not in duplicated):
                tmp = pd.concat([df7.loc[:, col1], df7.loc[:, col2]], axis=1, join="inner")
                tmp['sum'] = tmp.iloc[:,0] + tmp.iloc[:,1]
                duplicated.append(tmp.columns[1] + tmp.columns[0])
                for i in range(0,int(sum(tmp['sum'] == 2))):
                    net_df['Path1'].append(col1)
                    net_df['Path2'].append(col2)
                
    
    if len(net_df['Path1']) != 0:
        
        net_df = pd.DataFrame.from_dict(net_df)
        net_df['inter'] = net_df['Path1'] + ' + ' + net_df['Path2']
        net_df['weight'] = net_df.groupby('inter')['inter'].transform('count')
        net_df = net_df.drop_duplicates()
        net_df = net_df.reset_index(drop=True)
        
        net_df['p-val'] = None
        
        for n, p in enumerate(net_df['weight']):   
            net_df['p-val'][n] = stats.binom_test(net_df['weight'][n],sum(net_df['weight']),1/sum(net_df['weight']))
        
        net_df['p-adj[BF]'] = net_df['p-val']*len(net_df['p-val'])
        
        if adj == 'BF':
            net_df = net_df[net_df['p-adj[BF]'] < p_val]
        else:
            net_df = net_df[net_df['p-val'] < p_val]
            
        net_df['weight'] = np.log(net_df['weight'])*10
        
        return_df = pd.concat([return_df, net_df])
        
        biological_process_nx = nx.Graph() 
        
        
        nodes = list(net_df['Path1'])+list(net_df['Path2'])
        values, counts = np.unique(nodes, return_counts=True)    
        nodes_df = pd.DataFrame({'node':values, 'n':counts})
        nodes_df = nodes_df[nodes_df['node'] != 'None']
        nodes_df = nodes_df.sort_values('n', ascending=False)
        nodes_df['n'] = np.log(nodes_df['n'] + 1) * 10

        for i in range(0,len(nodes_df['node'])):
            biological_process_nx.add_node(nodes_df.iloc[i,0], size = nodes_df.iloc[i,1], color = 'green')
            
        for i in range(0,len(net_df['Path1'])):
            biological_process_nx.add_edge(net_df.iloc[i,0], net_df.iloc[i,1], weight = net_df.iloc[i,3])
            

    
                
    else:
        biological_process_nx = []
    
    cellular_component = df6[df6['type'] == 'cellular_component']
    
    
    
    df7 = cellular_component.pivot_table(index = "gen", columns = 'GOPa', values = 'n',  fill_value = 0)
    df7[df7 > 0] = 1
    
    net_df = {'Path1':[],'Path2':[]}
    duplicated = []
    for n1, col1 in enumerate(tqdm(df7.columns)):
        for n2, col2 in enumerate(df7.columns): 
            if (col1 != col2 and df7.columns[n1] + df7.columns[n2] not in duplicated):
                tmp = pd.concat([df7.loc[:, col1], df7.loc[:, col2]], axis=1, join="inner")
                tmp['sum'] = tmp.iloc[:,0] + tmp.iloc[:,1]
                duplicated.append(tmp.columns[1] + tmp.columns[0])
                for i in range(0,int(sum(tmp['sum'] == 2))):
                    net_df['Path1'].append(col1)
                    net_df['Path2'].append(col2)
     
    
    if len(net_df['Path1']) != 0:
        
        net_df = pd.DataFrame.from_dict(net_df)
        net_df['inter'] = net_df['Path1'] + ' + ' + net_df['Path2']
        net_df['weight'] = net_df.groupby('inter')['inter'].transform('count')
        net_df = net_df.drop_duplicates()
        net_df = net_df.reset_index(drop=True)
        
        net_df['p-val'] = None
        
        for n, p in enumerate(net_df['weight']):   
            net_df['p-val'][n] = stats.binom_test(net_df['weight'][n],sum(net_df['weight']),1/sum(net_df['weight']))
        
        net_df['p-adj[BF]'] = net_df['p-val']*len(net_df['p-val'])
       
        if adj == 'BF':
            net_df = net_df[net_df['p-adj[BF]'] < p_val]
        else:
            net_df = net_df[net_df['p-val'] < p_val]
            
        net_df['weight'] = np.log(net_df['weight'])*10
        
        return_df = pd.concat([return_df, net_df])
        
        cellular_component_nx = nx.Graph() 
        
        
        nodes = list(net_df['Path1'])+list(net_df['Path2'])
        values, counts = np.unique(nodes, return_counts=True)    
        nodes_df = pd.DataFrame({'node':values, 'n':counts})
        nodes_df = nodes_df[nodes_df['node'] != 'None']
        nodes_df = nodes_df.sort_values('n', ascending=False)
        nodes_df['n'] = np.log(nodes_df['n'] + 1) * 10

        for i in range(0,len(nodes_df['node'])):
            cellular_component_nx.add_node(nodes_df.iloc[i,0], size = nodes_df.iloc[i,1], color = 'blue')
            
        for i in range(0,len(net_df['Path1'])):
            cellular_component_nx.add_edge(net_df.iloc[i,0], net_df.iloc[i,1], weight = net_df.iloc[i,3])
            

    else:
        cellular_component_nx = []
    
    molecular_function = df6[df6['type'] == 'molecular_function']
    
    
    df7 = molecular_function.pivot_table(index = "gen", columns = 'GOPa', values = 'n',  fill_value = 0)
    df7[df7 > 0] = 1
    
    net_df = {'Path1':[],'Path2':[]}
    duplicated = []
    for n1, col1 in enumerate(tqdm(df7.columns)): 
        for n2, col2 in enumerate(df7.columns): 
            if (col1 != col2 and df7.columns[n1] + df7.columns[n2] not in duplicated):
                tmp = pd.concat([df7.loc[:, col1], df7.loc[:, col2]], axis=1, join="inner")
                tmp['sum'] = tmp.iloc[:,0] + tmp.iloc[:,1]
                duplicated.append(tmp.columns[1] + tmp.columns[0])
                for i in range(0,int(sum(tmp['sum'] == 2))):
                    net_df['Path1'].append(col1)
                    net_df['Path2'].append(col2)
                   
    
    if len(net_df['Path1']) != 0:
        
        net_df = pd.DataFrame.from_dict(net_df)
        net_df['inter'] = net_df['Path1'] + ' + ' + net_df['Path2']
        net_df['weight'] = net_df.groupby('inter')['inter'].transform('count')
        net_df = net_df.drop_duplicates()
        net_df = net_df.reset_index(drop=True)
        
        net_df['p-val'] = None
        
        for n, p in enumerate(net_df['weight']):   
            net_df['p-val'][n] = stats.binom_test(net_df['weight'][n],sum(net_df['weight']),1/sum(net_df['weight']))
        
        net_df['p-adj[BF]'] = net_df['p-val']*len(net_df['p-val'])
        
        if adj == 'BF':
            net_df = net_df[net_df['p-adj[BF]'] < p_val]
        else:
            net_df = net_df[net_df['p-val'] < p_val]
            
        net_df['weight'] = np.log(net_df['weight'])*10
        
        return_df = pd.concat([return_df, net_df])
        
        molecular_function_nx = nx.Graph() 
        
        
        nodes = list(net_df['Path1'])+list(net_df['Path2'])
        values, counts = np.unique(nodes, return_counts=True)    
        nodes_df = pd.DataFrame({'node':values, 'n':counts})
        nodes_df = nodes_df[nodes_df['node'] != 'None']
        nodes_df = nodes_df.sort_values('n', ascending=False)
        nodes_df['n'] = np.log(nodes_df['n'] + 1) * 10

        for i in range(0,len(nodes_df['node'])):
            molecular_function_nx.add_node(nodes_df.iloc[i,0], size = nodes_df.iloc[i,1], color = 'purple')
            
        for i in range(0,len(net_df['Path1'])):
            molecular_function_nx.add_edge(net_df.iloc[i,0], net_df.iloc[i,1], weight = net_df.iloc[i,3])
            
    
        
    else:
        molecular_function_nx = []
        
    combine_nx = nx.Graph() 
    
    
    if len(molecular_function_nx) != 0: 
        combine_nx = nx.compose(combine_nx, 
                                molecular_function_nx)
        
    if len(cellular_component_nx) != 0: 
        combine_nx = nx.compose(combine_nx, 
                                cellular_component_nx)
            
    if len(biological_process_nx) != 0: 
        combine_nx = nx.compose(combine_nx, 
                                biological_process_nx)
        
    
    if len(protein_class_nx) != 0: 
        combine_nx = nx.compose(combine_nx, 
                                protein_class_nx)
        
    if len(pathways_nx) != 0: 
        combine_nx = nx.compose(combine_nx, 
                                pathways_nx)                  
                            
    
    
    net = Network(notebook=True, height = '1000px', width = '1200px')
    net.from_nx(combine_nx)
    net.repulsion(node_distance=120, spring_length=220)
    net.show_buttons(filter_=['nodes', 'physics'])
    net.show(Path(dir, str(name + '.html')))

    return return_df