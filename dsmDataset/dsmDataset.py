from typing import Any, Dict, Tuple, List
from kedro.io import AbstractDataset

import json
import datetime

import dask.dataframe as dd
from dask.diagnostics import ProgressBar

from . import utils, customS3filesystem

class DaskDataset(AbstractDataset[dd.DataFrame, None]):
    def __init__(self, credentials: Dict[str, Any], name: str, directory: str, mode:str="overwrite",save_args: dict = {}, read_args:dict = {}):
        utils.creadentials.check_creadentials(creadentials=credentials)
        self.name = name
        self.path = f"{credentials.get('bucket_name')}/{credentials.get('project')}@project/{directory}/{name}@parquet"
        self._save_args = save_args
        self._read_args = read_args
        self._mode = mode

        self._bucket = customS3filesystem.CustomS3filesystem(
            endpoint_url=credentials.get('uri'), 
            key=credentials.get('access_key'), 
            secret=credentials.get('secret_key'),
            use_listings_cache=False,
            default_fill_cache=False,
        )
        self._save_args.update({
            'name_function': lambda x: f"part-{datetime.datetime.now().isoformat()}.parquet",
            'ignore_divisions': True,
            'overwrite': True
        })

    def _describe(self) -> Dict[str, Any]:
        pass

    def _load(self) -> Dict[dd.DataFrame, Any]:
        return dd.read_parquet(path=self.path, filesystem=self._bucket, **self._read_args)

    def _save(self, data: Tuple[dd.DataFrame, List[int]]) -> None:
        ddf, meta_list = data
        if self._mode == 'append' and self._bucket.exists(self.path):
            self._save_args.update({'append': True})
            if 'overwrite' in self._save_args:
                self._save_args.pop('overwrite')
        with ProgressBar():
            ddf.to_parquet(
                path=self.path,
                filesystem=self._bucket, 
                engine="pyarrow",
                **self._save_args,
            )
        meta = {
            'datadict': utils.handler.handle_timeout(function=utils.dataframe.get_datadict, args={'ddf': ddf}, default_value=[]),
            'example': utils.handler.handle_timeout(function=utils.dataframe.get_data_example, args={'ddf': ddf}, default_value=[])
        }
        with self._bucket.open(f"{self.path}.metadata.json", 'w') as f:
            json.dump(obj=meta, fp=f)