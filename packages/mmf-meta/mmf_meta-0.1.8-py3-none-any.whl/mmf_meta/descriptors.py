import datetime
import enum
import functools
import io
import mmap
import os
import re
import typing
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib import parse

from .formats import DataFrameFormat, ColorMode, ImageFormat
from .autodoc import desc, autodoc_dc
from ._imports import *
from .df_io import _df_map_from, _df_map_to

ext_patt = re.compile(r"\.(\w+?)\?")


class DescriptorClass(str, enum.Enum):
    DataFrame = "DataFrame"
    Image = "Image"
    String = "String"
    Integer = "Integer"
    Float = "Float"
    Datetime = "Datetime"
    Bool = "Bool"
    Dict = "Dict"
    JsonFile = "JsonFile"
    DescriptorBase = "DescriptorBase"


@autodoc_dc
@dataclass
class DescriptorBase:
    """
    Базовый класс для описания дескрипторов
    """

    default: typing.Optional[typing.Any] = desc(
        None, description="Значение по-умолчанию"
    )
    description: str = desc(None, description="Описание для веб-интерфейса")
    name: str = desc(
        None,
        description="Читаемое имя для веб-интерфейса, если не указывать, будет использовано имя функции",
    )
    out_format: str = desc(
        "out",
        description="Формат файла на выходе, может быть переопределен пользователем",
    )
    is_file: bool = desc(
        False, description="Если True, ожидается бинарный файл на входе", init=False
    )
    class_name: DescriptorClass = desc(
        DescriptorClass.DescriptorBase, description="Название дескриптора", init=False
    )
    _proto_name = None
    _pydantic_type = None
    _input_formats = None
    _output_formats = None
    _fastapi_type = None

    def __post_init__(self):
        if self.is_file:
            self._pydantic_type = UploadFile
        self.class_name = DescriptorClass(self.__class__.__name__)

    @property
    def fastapi_descriptor(self) -> typing.Tuple[typing.Any, typing.Any]:
        if not self.is_file:
            b = fastapi.Body(self.default, description=self.description)
        else:
            if self._input_formats:
                types = ",".join(self._input_formats)
                types = f" ({types})"
            else:
                types = ""
            b = fastapi.File(
                ...,
                description=f"{self.description}{types}",
            )
        return (self._pydantic_type, b)

    def load_url(self, url: str, target_file: str = None):
        raise NotImplemented

    def load_file(self, file_path: typing.Union[os.PathLike, str], ext=None):
        raise NotImplemented

    def to_file(self, data, ext=None, target_file: str = None) -> io.BytesIO:
        raise NotImplemented


@autodoc_dc
@dataclass
class DataFrame(DescriptorBase):
    """
    Дескриптор, описание данных в формате `pandas.DataFrame`

    Поскольку этот дескриптор всегда представляет файл, он может сочетаться только с файловыми дескрипторами такими как
    [DataFrame][], [Image][], [JsonFile][]
    """

    out_format: DataFrameFormat = desc(
        DataFrameFormat.CSV,
        description="Формат, используемый по-умолчанию при выводе из модели. "
        "Пользователь сможет запросить и любой другой формат из поддерживаемых, но этот будет использован по-умолчанию.",
    )
    schema: dict = desc(
        None,
        description="Схема данных для валидации типов данных, схема записывается как "
        '`{"column_name_string": str, "column_name_int": int}` и тд',
    )
    pandas_params: dict = desc(
        ...,
        description="Параметры к методам pandas.read_*. Во время "
        "преобразовывания в DataFrame будет вызываться "
        "один из методов pandas.read_* в зависимости от "
        "типа файла. Например, read_csv, если был передан .csv "
        "файл. pandas_params будут переданы как дополнительные "
        "аргументы к этому методу.",
        default_factory=dict,
    )
    is_file: bool = desc(
        True, description="Если True, ожидается бинарный файл на входе", init=False
    )
    _input_formats = [
        "xlsx",
        "xls",
        "csv",
        "xml",
        "json",
        "parquet",
    ]
    _output_formats = _input_formats

    def load_url(self, url: str, target_file: str = None):
        try:
            ext = next(ext_patt.finditer(url)).group(1).lower()
        except StopIteration:
            raise ValueError(f"no extention in url {url}")
        return self.load_file(url, ext=ext)

    def load_file(self, file_path: typing.Union[str, os.PathLike], ext: str = None):
        if pandas is None:
            raise ImportError(f"pandas must be installed")
        if "dtype" not in self.pandas_params and self.schema:
            params = self.pandas_params.copy()
            params["dtype"] = self.schema
        else:
            params = self.pandas_params
        if not ext:
            *_, ext = file_path.lower().split(".")

        foo = _df_map_from.get(DataFrameFormat(ext))
        if not foo:
            raise ValueError(
                f"input extension {ext} is not supported with DataFrame writer"
            )
        return foo(file_path, **params)

    def to_file(self, data, ext=None, target_file: str = None):
        """
        Конвертирует DataFrame в BytesIO с использованием одного из поддерживаемых форматов

        :param data:
        :param ext:
        :return:
        """
        if pandas is None:
            raise ImportError(f"pandas must be installed")
        foo = _df_map_to.get(ext or self.out_format)
        if not foo:
            raise ValueError(
                f"output extension {ext} is not supported with DataFrame writer"
            )
        if not target_file:
            buf = io.BytesIO()
        else:
            buf = target_file
        foo(data, buf)
        if target_file:
            return target_file
        else:
            return buf


if jpeg and cv2:
    _img_map_to = {
        ImageFormat.JPG: jpeg.encode,
    }


@autodoc_dc
@dataclass
class Image(DescriptorBase):
    """
    Дескриптор, описание данных в формате изображения. При загрузке в модель будет использоваться по-умолчанию numpy-array в формате RGB,
    при выгрузке из модели - jpeg по-умолчанию

    Поскольку этот дескриптор всегда представляет файл, он может сочетаться тольк ос фаловыми дескрипторами такими как
    [DataFrame][], [Image][], [JsonFile][]
    """

    color: ColorMode = desc(
        ColorMode.RGB,
        description="Тип цвета, к которому будет приведен массив. Например opencv "
        "открывает изображения по-умолчанию в BGR-формате, а Pllow в RGB. "
        "Поскольку мы используем разлные библиотеки для открытия разных форматов "
        "все изображения приводятся к единому фомрату, по-умолчанию RGB.",
    )
    out_format: ImageFormat = desc(
        ImageFormat.JPG,
        description="Формат изображения, который по-умолчанию отдается пользователю, может быть переопределен "
        "пользователем",
    )
    is_file: bool = desc(
        True, description="Если True, ожидается бинарный файл на входе", init=False
    )
    _input_formats = [
        "bmp",
        "dib",
        "jpeg",
        "jpg",
        "jpe",
        "png",
        "pbm",
        "pgm",
        "ppm",
        "pxm",
        "pnm",
        "sr",
        "ras",
        "tiff",
        "tif",
        "exr",
        "hdr",
        "pic",
    ]
    _output_formats = ["jpg"]

    def load_url(self, url: str, target_file: str = None):
        if cv2 is None:
            raise ImportError("opencv-python must be installed")
        if jpeg is None:
            raise ImportError("PyTurboJPEG must be installed")
        file_name = Path(parse.urlparse(url).path).name
        *_, ext = file_name.lower().split(".")
        data = urllib.request.urlopen(url)
        if ext in ("jpg", "jpeg"):
            data = jpeg.decode(data.read())
            if self.color == ColorMode.BGR:
                data = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
        else:
            with mmap.mmap(-1, 0) as f:
                f[:] = data.read()
            data = np.asarray(memoryview(f), dtype="uint8")
            data = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if self.color == ColorMode.RGB:
                data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        return data

    def load_file(self, file_path: typing.Union[str, os.PathLike], ext: str = None):
        if cv2 is None:
            raise ImportError("opencv-python must be installed")
        if jpeg is None:
            raise ImportError("PyTurboJPEG must be installed")
        if file_path[:-3] == "jpg" or ext in ("jpg", "jpeg"):
            with open(file_path, "br") as f:
                ret = jpeg.decode(f)
                if self.color == ColorMode.BGR:
                    ret = cv2.cvtColor(ret, cv2.COLOR_RGB2BGR)
        else:
            ret = cv2.imread(file_path)
            if self.color == ColorMode.RGB:
                ret = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
        return ret

    def to_file(self, data, ext=None, target_file: str = None):
        foo = _df_map_to.get(ext or self.out_format)
        if not foo:
            raise ValueError(
                f"output extension {ext} is not supported with Image writer"
            )
        if target_file:
            with open(target_file, "bw") as f:
                f.write(foo(data))
                return target_file
        else:
            return io.BytesIO(foo(data))


@autodoc_dc
@dataclass
class String(DescriptorBase):
    """
    Дескриптор, описание данных в формате строки
    """

    _pydantic_type = str


@autodoc_dc
@dataclass
class Integer(DescriptorBase):
    """
    Дескриптор, описание данных в формате целых чисел
    """

    _pydantic_type = int


@autodoc_dc
@dataclass
class Float(DescriptorBase):
    """
    Дескриптор, описание данных в формате числа с плавающей точкой
    """

    _pydantic_type = float


@autodoc_dc
@dataclass
class Datetime(DescriptorBase):
    """
    Дескриптор, описание данных в формате даты/времени в строковом представлении согласно спецификации [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
    """

    _pydantic_type = datetime.datetime


@autodoc_dc
@dataclass
class Bool(DescriptorBase):
    """
    Дескриптор, описание данных в формате boolean
    """

    _pydantic_type = bool


@autodoc_dc
@dataclass
class Dict(DescriptorBase):
    """
    Дескриптор, описание данных в формате dict, если указать в качестве return будет преобразован в json или
    protobuf в зависимости от content-type в исходном запросе
    """

    _pydantic_type = dict


@autodoc_dc
@dataclass
class JsonFile(DescriptorBase):
    """
    Дескриптор, помечает аргумент как json-file, который будет преобразован в dict на входе или в json-file на выходе.

    С точки зрения клиента, поскольку такой файл обычно не занимает много места, то по-умолчанию его не требуется
    загружать в s3, вместо этого можно указать как аргумент непосредственно в payload. В таком случае он должен быть
    представлен либо в форме словаря `{}` или в форме масссива `[]`

    Если в payload будет передана строка, то она будет расцениваться как ссылка на хранилище с файлом.

    Поскольку этот дескриптор всегда представляет файл, он может сочетаться только с файловыми дескрипторами такими как
    [DataFrame][], [Image][], [JsonFile][]
    """

    is_file: bool = desc(
        True, description="Если True, ожидается бинарный файл на входе", init=False
    )
    to_s3: bool = desc(
        False,
        description="Если true, то на выходе будет сохраняться в s3-хранилище вместо обычного "
        "вывода в payload",
    )
    out_format: str = "json"
    _output_formats = ["json"]
    _input_formats = ["json"]

    def load_url(self, url: typing.Union[str, dict, list], target_file: str = None):
        if orjson is None:
            raise ImportError("orjson must be installed")
        if isinstance(url, (dict, list)):
            return url
        else:
            data = urllib.request.urlopen(url)
            return orjson.loads(data)

    def to_file(self, data, ext=None, target_file: str = None):
        if orjson is None:
            raise ImportError("orjson must be installed")
        if target_file:
            with open(target_file, "bw") as f:
                f.write(orjson.dumps(data))
                return target_file
        return io.BytesIO(orjson.dumps(data))
