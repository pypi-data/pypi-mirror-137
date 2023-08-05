# MMF-meta
Эта библиотека - часть проекта Model Management Framework.

Отвечает за оформление пользовательских функций

### Пример использования

```python
import mmf_meta.formats
import pickle
import time
import pandas
import mmf_meta as mmf


@mmf.target(
    description="Супер-функция",
    returns=mmf.DataFrame(out_format=mmf_meta.formats.DataFrameFormat.CSV),
)
def score(
        df: pandas.DataFrame = mmf.DataFrame(description="Описание df"),
        # other: dict = mmf.JsonFile(description="Описание other"),
):
    return df


@mmf.target(
    description="Другая супер-функция",
    returns=mmf.String(),
)
def other(
        inp=mmf.String(description="важный параметр"),
        another=mmf.Integer(description="еще один важный параметр"),
):
    time.sleep(30)
    return inp


mmf.artifact("some_file")


@mmf.artifact("other")
def model():
    with open("other", "br") as f:
        return pickle.load(f)

```

[Подробная документация](https://mm-framework.github.io/docs/)
