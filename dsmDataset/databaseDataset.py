from typing import Any, Dict, Tuple, List
from kedro.io import AbstractDataset

import dask.dataframe as dd
from dask.diagnostics import ProgressBar

class DatabaseDataset(AbstractDataset[dd.DataFrame, None]):
    def __init__(self, credentials: Dict[str, Any], table_name: str, save_args: dict={}, index_col: str = "-", divisions: list = None):
        self._con = credentials.get('con')
        self._table_name = table_name
        self._save_args = save_args
        self._index_col = index_col
        self._divisions = divisions
    
    def _describe(self) -> Dict[str, Any]:
        pass
    
    def _load(self):
        return dd.read_sql_table(table_name=self._table_name, con=self._con, index_col=self._index_col, divisions=self._divisions)

    
    def _save(self, data: Tuple[dd.DataFrame, List[int]]) -> None:
        ddf, meta_list = data
        if self._is_validate_col:
            self._validate_col(ddf)
        with ProgressBar():
            ddf.to_sql(name=self._table_name, uri=self._con, **self._save_args)

