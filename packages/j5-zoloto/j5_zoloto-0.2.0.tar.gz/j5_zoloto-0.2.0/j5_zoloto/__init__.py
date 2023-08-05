"""Integration between j5 and zoloto."""
from .backends import ZolotoHardwareBackend
from .board import ZolotoCameraBoard

__version__ = "0.2.0"

__all__ = [
    "__version__",
    "ZolotoCameraBoard",
    "ZolotoHardwareBackend",
]
