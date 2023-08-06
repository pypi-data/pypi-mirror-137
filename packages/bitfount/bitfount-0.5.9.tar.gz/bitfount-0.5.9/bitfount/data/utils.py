"""Utility functions concerning data."""
from dataclasses import dataclass
import hashlib
from typing import List, Optional, Union, cast

from bitfount.types import _DataFrameType, _SeriesType


@dataclass
class DatabaseConnection:
    """Arguments that correspond to those of {pd, ks}.read_sql_table().

    Args:
        table_name: Name of SQL table in database.
        con: A database URI could be provided as str.
        schema: The name of SQL schema in database to query (if database
            flavor supports this). Defaults to None.
        index_col: Column(s) to set as index(MultiIndex). Defaults to None.
        columns: List of column names to select from SQL table. Defaults to None.
    """

    table_name: str
    con: str
    schema: Optional[str] = None
    index_col: Optional[Union[str, List[str]]] = None
    columns: Optional[List[str]] = None


def _generate_dataframe_hash(df: _DataFrameType) -> str:
    """Generates a hash of a DataFrame.

    Uses column names and column dtypes to generate the hash. DataFrame contents
    is NOT used.

    SHA256 is used for hash generation.

    Args:
        df: The DataFrame to hash.

    Returns:
        The hexdigest of the DataFrame hash.
    """
    # DataFrame.dtypes contains column names and their dtypes as a Series
    df_columns_and_types: _SeriesType = df.dtypes
    # Series.to_string() returns str if buf=None (the default)
    str_rep: str = cast(str, df_columns_and_types.to_string())
    return _hash_str(str_rep)


def _hash_str(to_hash: str) -> str:
    """Generates a sha256 hash of a given string.

    Uses UTF-8 to encode the string before hashing.
    """
    return hashlib.sha256(to_hash.encode("utf-8")).hexdigest()
