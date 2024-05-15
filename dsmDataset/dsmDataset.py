from typing import Any, Dict, Tuple, List
from kedro.io import AbstractDataset

import dask.dataframe as dd
from dask.diagnostics import ProgressBar

from . import utils

import json

class DaskDataset(AbstractDataset[dd.DataFrame, None]):
    def __init__(self, credentials: Dict[str, Any], name: str, directory: str, save_args: dict = {}, read_args:dict = {}):
        utils.creadentials.check_creadentials(creadentials=credentials)
        self._storage_options = {
            'key': credentials.get('access_key'),
            'secret': credentials.get('secret_key'),
            'client_kwargs':{
                'endpoint_url': credentials.get('uri')
            },
            'use_listings_cache': False,
            'default_fill_cache': False,
        }
        self.name = name
        self.path = f"s3://{credentials.get('bucket_name')}/{credentials.get('project')}/{directory}/{name}"
        self._save_args = save_args
        self._read_args = read_args

    def _describe(self) -> Dict[str, Any]:
        pass

    def _load(self) -> Dict[dd.DataFrame, Any]:
        return dd.read_parquet(path=self.path, storage_options=self._storage_options, **self._read_args)

    def _save(self, data: Tuple[dd.DataFrame, List[int]]) -> None:
        ddf, meta_list = data
        meta = {
            'datadict': json.dumps({str(k):str(v) for k,v in dict(ddf.dtypes).items()})
        }
        with ProgressBar():
            ddf.to_parquet(
                path=self.path, 
                storage_options=self._storage_options, 
                engine="pyarrow",
                custom_metadata=meta,
                **self._save_args,
            )