import pandas as pd 
import sqlite3
from sql_metadata import Parser
from sql_on_dfs.utils import get_dfs_from_caller_scope
from loguru import logger
import sys

def execute(query:str, inmemory:bool=True, debug:bool = False)->pd.DataFrame:
    """convenience function to write sql on arbitrary DFs
        ...execute in a temp sqlite db and return results as DF
    """
    if debug:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    # get table-names referenced by query, which should correspond to dataframes in caller's scope
    tablenames = Parser(query).tables
    logger.debug(f"tablenames parsed from query: {tablenames}")

    # get a mapping of those tablenames in query to the actual corresponding DataFrame objects from caller's scope 
    tablenames_and_assoc_dfs = get_dfs_from_caller_scope(tablenames)
    logger.debug(f"DFs found: {tablenames_and_assoc_dfs.keys()}")

    # if no temp.db exists here, sqlite3 will create one
    connstr = ":memory:" if inmemory else "temp.db"
    sql3conn = sqlite3.connect(connstr)
    
    # write dfs to sqlite3 db to perform sql query on them there
    for df_name,df in tablenames_and_assoc_dfs.items():
        logger.debug(f"writing df: {df_name} to database")
        df.to_sql(df_name, sql3conn, index=False, if_exists='replace')
    
    result = pd.read_sql_query(query, sql3conn)
    return result