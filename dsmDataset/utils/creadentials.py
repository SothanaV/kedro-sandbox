def check_creadentials(creadentials):
    _require_key = ['bucket_name', 'project', 'access_key', 'secret_key', 'uri']
    out = []
    for k,v in creadentials.items():
        if k not in _require_key:
            out.append(k)
    if out != []:
        raise Exception(f"Expect keys {_require_key}, but got {list(creadentials.keys())}")