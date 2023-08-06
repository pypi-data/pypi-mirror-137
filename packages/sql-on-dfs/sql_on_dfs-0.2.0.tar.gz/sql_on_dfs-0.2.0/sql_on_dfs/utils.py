from inspect import currentframe
import pandas as pd


def get_dfs_from_caller_scope(df_names: list[str]) -> dict[str, pd.DataFrame]:
    """Given a list of DF names, this returns a dict mapping df-name to df from original* scope
    
    *'original scope' in this function context meaning the caller's caller's scope
     """
    vars_in_orig_scope = currentframe().f_back.f_back.f_locals

    dfs_map = {}
    for k,v in vars_in_orig_scope.items():
        if k in df_names and isinstance(v, pd.DataFrame):
            dfs_map[k] = v

    return dfs_map