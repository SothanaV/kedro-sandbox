# kedro-sandbox
- create virtualenv
```
python3 -m venv env
```

- activate env
```
source env/bin/activate
```

- start project
```
kedro new -n etl-pipeline --tools viz --example=n
```

- install more dependencies
```
pip install "dask[dataframe]" kedro-airflow
```

- create pipeline
```
kedro pipeline create <pipeline name>
```