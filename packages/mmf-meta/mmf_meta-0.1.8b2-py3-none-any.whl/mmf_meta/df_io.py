import functools

from .formats import DataFrameFormat
from ._imports import pandas


def read_excel(file, engine=None, **kwargs):
    if isinstance(file, str):
        return pandas.read_excel(file)
    else:
        return pandas.read_excel(file, engine=engine, **kwargs)


def write_excel(data: "pandas.DataFrame", file, engine=None, **kwargs):
    if isinstance(file, str):
        return data.to_excel(file, **kwargs)
    else:
        return data.to_excel(file, engine=engine, **kwargs)


if pandas:
    _df_map_to = {
        DataFrameFormat.XLSX: functools.partial(write_excel, engine="xlsxwriter"),
        DataFrameFormat.XLS: functools.partial(write_excel, engine="openpyxl"),
        DataFrameFormat.CSV: pandas.DataFrame.to_csv,
        DataFrameFormat.XML: pandas.DataFrame.to_xml,
        DataFrameFormat.JSON: pandas.DataFrame.to_json,
        DataFrameFormat.PARQUET: pandas.DataFrame.to_parquet,
    }
    _df_map_from = {
        DataFrameFormat.XLSX: functools.partial(read_excel, engine="openpyxl"),
        DataFrameFormat.XLS: functools.partial(read_excel, engine="xlrd"),
        DataFrameFormat.CSV: pandas.read_csv,
        DataFrameFormat.XML: pandas.read_xml,
        DataFrameFormat.JSON: pandas.read_json,
        DataFrameFormat.PARQUET: pandas.read_parquet,
    }
else:
    _df_map_to = {}
    _df_map_from = {}
