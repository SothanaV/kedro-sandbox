"""
This is a boilerplate pipeline 'landing'
generated using Kedro 0.19.5
"""
from typing import Any, Dict, Tuple, List
import dask.dataframe as dd

def pass_data(ddf: dd.DataFrame) -> Tuple[dd.DataFrame, int]:
    return ddf, []