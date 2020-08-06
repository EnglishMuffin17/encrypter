from typing import Protocol, overload, Text, Sequence
from types import FunctionType


class knitpattern(Protocol):
    @overload
    def __init__(self, string: Text, base: int, func: FunctionType, *args, **kwargs): ...
    @overload
    def __init__(self, string: Text, base: hex, func: FunctionType, *args, **kwargs): ...
    @overload
    def __init__(self, string: Text, base: oct, func: FunctionType, *args, **kwargs): ...
    def prefix(self): - str
    def sequence(self): - __Sequence
    class __Sequence(Protocol):
        def from_keys(self): - dict
        def from_values(self): - dict
class knitcrypt(Protocol):
    def __init__(self, path: Text, pattern: knitpattern, encoding: Text): ...
class _File_Struct(Protocol):
    def __init__(self, path: Text, pattern: knitpattern, encoding: Text): ...
    def stitch(self): _Stitch_Struct
    def unknit(self): _Unknit_Struct
    def contents(self): - [str]
    def close(self): ...
