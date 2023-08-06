from abc import ABCMeta, abstractmethod
import importlib
from typing import Iterable, Tuple

import sys
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

from remotezip.core.zip import EOCD, CDFileHeader

class RemoteZip(metaclass=ABCMeta):
    eocd: EOCD
    files: Tuple[CDFileHeader, ...] = tuple()

    def __init__(self, eocd: EOCD, records: Iterable[CDFileHeader]):
        self.eocd = eocd
        self.files = tuple(records)

    @abstractmethod
    def open(self, filename: CDFileHeader) -> bytes:
        return b'ee'

for entry in entry_points(group='remotezip.plugins'):
    setattr(RemoteZip, entry.name, getattr(importlib.import_module(entry.value), entry.name))
