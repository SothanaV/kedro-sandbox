import json
from . import clean

def get_datadict(ddf):
    data = [{
        "name": str(k), 
        "dtype": str(v)
    } for k,v in dict(ddf.dtypes).items()]
    clean.clean_np(data)
    return data

def get_data_example(ddf):
    data = ddf.sample(frac=10/len(ddf), random_state=99).compute().to_dict('records')
    clean.clean_np(data)
    return data