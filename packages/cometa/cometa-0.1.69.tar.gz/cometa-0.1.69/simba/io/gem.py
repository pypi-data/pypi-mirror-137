import os
import pandas as pd
import difflib
import json
import requests
import networkx as nx
from rdkit.Chem import MolFromInchi,MolToInchiKey
import simba.constants as cs
import pkg_resources

def allowed_models():
    curl = 'http://bigg.ucsd.edu/api/v2/models'
    resp = requests.get(curl)
    lmodels = resp.json()
    bigg_ids = [x["bigg_id"] for x in lmodels["results"]]
    return bigg_ids

def get_bigg_id(name:str):
    all_bigg = allowed_models()
    #We first test equlity
    if name in all_bigg:
        true_name = name
    else:
        matches = difflib.get_close_matches(name, all_bigg)
        if len(matches)>1:
            raise ValueError("Multiples matches found for Bigg ID:"+str(matches))
        elif len(matches)==0:
            raise ValueError("Invalid Bigg ID: "+name)
        else:
            true_name = matches[0]
    return true_name

def build_bigg_url(bid:str):
    return "http://bigg.ucsd.edu/api/v2/models/"+bid+"/download"

# Recon3D case
def build_alternative_bigg_url(bid:str):
    return 'http://bigg.ucsd.edu/static/models/'+bid+'.json'


def get_bigg_model_from_web(bid:str):
    url_request = build_bigg_url(bid)
    try:
        model = requests.get(url_request).json()
    except Exception as e:
        url_request = build_alternative_bigg_url(bid)
        model = requests.get(url_request).json()
    return model

def get_bigg_model_from_file(fname:str):
    with open(fname,"r") as f:
        model = json.load(f)
    return model

def build_gem_graph(bigg_id:str):
    print("BiGG_ID:",bigg_id)
    if os.path.isfile(bigg_id):
        model = get_bigg_model_from_file(bigg_id)
    else:
        rbigg_id =  get_bigg_id(bigg_id)
        model = get_bigg_model_from_web(rbigg_id)
    stream = pkg_resources.resource_stream("simba", "data/chebi.csv")
    tchebi = pd.read_csv(stream)
    chebi_inchi ={hid:hinchi for hid,hinchi in zip(tchebi.chebi_id,tchebi.inchi) if isinstance(hinchi,str)}
    bigg_chebi_ids = {mm['id']:mm['annotation']['chebi'] for mm in model['metabolites'] if 'chebi' in mm['annotation']}

    def get_inchi_from_biggid(bid:str):
        if bid not in bigg_chebi_ids:
            return None
        vids = bigg_chebi_ids[bid]
        for vid in vids:
            if vid in chebi_inchi:
                return chebi_inchi[vid]
        return None

    dic_biggid_inchi = {bid:get_inchi_from_biggid(bid) for bid in bigg_chebi_ids if get_inchi_from_biggid(bid) is not None}

    def edges_from_reactions(vreacs,d_id_inchi):
        bigg_index = {key:idx for idx,key in enumerate(d_id_inchi.keys())}
        all_edges = []
        for reac in vreacs:
            neg_val = [key for key,val in reac['metabolites'].items() if val==-1.0 and key in d_id_inchi]
            pos_val = [key for key,val in reac['metabolites'].items() if val==1.0 and key in d_id_inchi]
            if len(neg_val)==0 or len(pos_val)==0:
                continue
            #WE get the position
            edges = [(bigg_index[nn],bigg_index[pp]) for nn in neg_val for pp in pos_val]
            all_edges.append(edges)
        return bigg_index,all_edges

    bigg_index,all_edges = edges_from_reactions(model['reactions'],dic_biggid_inchi)
    G = nx.Graph()
    G.add_nodes_from(list(range(len(bigg_index))))
    G.add_edges_from([e for x in all_edges for e in x])
    inchikey_nodes = [None]*G.number_of_nodes()
    invalid_nodes = []
    for bid,index in bigg_index.items():
        if isinstance(dic_biggid_inchi[bid],str):
            inchikey_nodes[index] = MolToInchiKey(MolFromInchi(dic_biggid_inchi[bid]))[0:14]
        else:
            invalid_nodes.append(bid)
            continue
    return inchikey_nodes,G
