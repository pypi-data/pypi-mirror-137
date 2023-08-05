try:
    import orjson
except ImportError:
    orjson = None

try:
    import fastapi
    from fastapi import UploadFile
except ImportError:
    fastapi = None
    UploadFile = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import pandas
    import numpy as np
except ImportError:
    pandas = None
    np = None


try:
    from turbojpeg import TurboJPEG

    jpeg = TurboJPEG()
except Exception:
    jpeg = None