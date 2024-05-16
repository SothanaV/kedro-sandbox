import pandas as pd
import numpy as np

def np2primative(obj):
    if isinstance(obj, np.generic):
        return obj.item() if pd.isnull(obj.item()) == False else 0
    elif isinstance(obj, list):
        return [np2primative(elm) for elm in obj]
    elif isinstance(obj, dict):
        return {k: np2primative(v) for k,v in obj.items()}
    return obj if pd.isnull(obj) == False else 0

def clean_np(objs):
    for obj in objs:
        for k, v in obj.items():
            obj[k] = np2primative(v)