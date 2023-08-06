from importlib.metadata import version
from .am2320 import AM2320


try:
    __version__ = version(__name__)
except:
    pass


__all__ = ["AM2320"]
