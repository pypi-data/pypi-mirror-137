from enum import Enum


class DataFrameFormat(str, Enum):
    """
    Тип файла DataFrame.
    """

    XLSX = "xlsx"
    XLS = "xls"
    CSV = "csv"
    XML = "xml"
    JSON = "json"
    PARQUET = "parquet"


class ColorMode(str, Enum):
    """
    Цветовая схема изображения
    """

    RGB = "rgb"
    BGR = "bgr"


class ImageFormat(str, Enum):
    """
    Формат исходящего файла
    """

    JPG = "jpg"
